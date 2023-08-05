"""
Utility functions for data smashing including quantization and loading data
from the D3M format.
"""
import os
import json
import csv
import warnings
import tempfile
import subprocess as sp
from shutil import copytree, ignore_patterns, rmtree
import numpy as np
import pandas as pd
from imageio import imread, imwrite
from datasmash.config import BIN_PATH


def quantize_inplace(filename, partition, *, detrending=None):
    """

    """
    unquantized = pd.read_csv(filename, delimiter=' ', dtype='float',
                              header=None)
    if detrending:
        length = len(unquantized.columns)
        shifted_dfs = []
        for i in range(detrending+1):
            end = length - detrending + i
            next_ = unquantized.iloc[:, i:end]
            next_.columns = range(next_.shape[1])
            shifted_dfs = [next_] + shifted_dfs
        unquantized = shifted_dfs[0] - sum(shifted_dfs[1:])

    quantized = np.digitize(unquantized, bins=partition)
    np.savetxt(filename, quantized, fmt='%d', delimiter=' ')


def quantizer(data_dir, *, problem_type,
              num_streams=-1,
              sample_size=0.2,
              bin_path=BIN_PATH,
              detrending=None,
              pooled=True,
              epsilon=-1,
              min_alphabet_size=2,
              max_alphabet_size=3,
              inplace=True,
              use_genesess=True,
              gen_epsilon=0.02,
              num_steps=1000,
              num_models=1):
    """

    """
    if use_genesess and not inplace:
        warnings.warn(("cannot run genesess on un-quantized data; data must be"
                       "quantized in place"), UserWarning)

    quantizer_binary = [os.path.abspath(os.path.join(bin_path, 'Quantizer'))]
    _data_dir = ['-D', data_dir]

    _problem_type = ['-t']
    _num_streams = ['-T']
    if problem_type == 2 or problem_type == 'supervised':
        _problem_type.append("2")
        _num_streams.append("-1")
    else:
        assert num_streams > 0, ("a positive number must be specified for "
                                 "total number of streams")
        _num_streams.append(str(num_streams))
        if problem_type == 1 or problem_type == 'unsupervised_with_targets':
            _problem_type.append("1")
        elif problem_type == 0 or problem_type == 'unsupervised':
            _problem_type.append("0")
    _sample_size = ['-x', str(sample_size)]

    _detrending = ['-d']
    if detrending:
        _detrending.append(str(detrending))
    else:
        _detrending.append("0")

    _pooled = ['-w']
    if pooled:
        _pooled.append("1")
    else:
        _pooled.append("0")

    _epsilon = ['-e', str(epsilon)]

    _min_alphabet_size = ['-a', str(min_alphabet_size)]
    _max_alphabet_size = ['-A', str(max_alphabet_size)]

    command_list = (quantizer_binary +
                    _data_dir +
                    _problem_type +
                    _num_streams +
                    _sample_size +
                    _detrending +
                    _pooled +
                    _epsilon +
                    _min_alphabet_size +
                    _max_alphabet_size)
    raw_partition = sp.check_output(command_list, encoding='utf-8')
    partition = [str(p) for p in eval(raw_partition)]

    if inplace:
        lib_list_path = os.path.join(data_dir, 'library_list')
        lib_list = []
        with open(lib_list_path, 'r') as infile:
            for line in infile:
                train_metadata = line.strip().split(' ')
                lib_file = train_metadata[0]
                lib_list.append(lib_file)
        for lib_file in lib_list:
            lib_file_path = os.path.join(data_dir, lib_file)
            quantize_inplace(lib_file_path, partition)
            if use_genesess:
                genesess(lib_file_path,
                         gen_epsilon=gen_epsilon,
                         num_steps=num_steps,
                         num_models=num_models)
    return partition


def genesess(data_file, *,
             out_file='result.txt',
             data_type='symbolic',
             data_direction='row',
             gen_epsilon=0.02,
             timer=False,
             num_steps=1000,
             num_models=1,
             verbose=False,
             bin_path=BIN_PATH):
    """

    """
    gen_binary = [os.path.abspath(os.path.join(bin_path, 'genESeSS'))]

    _data_file = ['-f', data_file]
    _out_file = ['-o', out_file]
    run_file = ['-R', data_file]

    _max_stream_length = ['-x']
    length = len(pd.read_csv(data_file, sep=' ', header=None).columns)
    _max_stream_length.append(str(length))

    _data_type = ['-T', data_type]

    _data_direction = ['-D', data_direction]

    _gen_epsilon = ['-e', str(gen_epsilon)]

    _timer = ['-t', str(timer).lower()]

    _num_steps = ['-r', str(num_steps)]

    _num_models = ['-N', str(num_models)]

    _verbose = ['-v']
    if verbose:
        _verbose.append("1")
    else:
        _verbose.append("0")

    command_list = (gen_binary
                    + _data_file
                    + _out_file
                    + run_file
                    + _max_stream_length
                    + _data_type
                    + _data_direction
                    + _gen_epsilon
                    + _timer
                    + _num_steps
                    + _num_models
                    + _verbose)

    output = sp.check_output(command_list, encoding='utf-8')
    return output


def serializer(bmp_filenames, *, outfile, bin_path=BIN_PATH, seq_len=1000,
               num_seqs=1, power_coeff=1.0, channel='R', size=16384,
               serializer_verbose=False):
    """

    """
    serializer_binary = [os.path.abspath(os.path.join(bin_path, 'serializer'))]
    _bmp_filenames = ['-f', bmp_filenames]
    _outfile = ['-o', outfile]
    _seq_len = ['-L', str(seq_len)]
    _num_seqs = ['-n', str(num_seqs)]
    _power_coeff = ['-w', str(power_coeff)]
    _channel = ['-c', channel]
    _size = ['-s', str(size)]
    _verbose = ['-v']
    if serializer_verbose:
        _verbose.append("1")
    else:
        _verbose.append("0")

    command_list = (serializer_binary
                    + _bmp_filenames
                    + _outfile
                    + _seq_len
                    + _num_seqs
                    + _power_coeff
                    + _channel
                    + _size
                    + _verbose)
    return sp.check_output(command_list, encoding='utf-8')


class DatasetLoader(object):
    """

    """
    def __init__(self):
        self._train_dir = ''
        self._test_dir = ''

        train_json_path = ''
        test_json_path = ''
        self._train_doc = {}
        self._test_doc = {}

        self._is_raw_images = None
        self.tmp_dir = ''
        self.dataset_name = ''
        self.time_series_cols = []
        self.channel_dirs = []
        self.channel_problems = {}

        self.bmp_dirs = {}
        self.bmp_ser_dirs = {}

    @staticmethod
    def _mkdir(directory):
        """

        """
        if os.path.isdir(directory):
            rmtree(directory)
        os.mkdir(directory)

    @staticmethod
    def _load_table(*, json_path):
        """

        """
        if not os.path.isfile(json_path):
            raise FileNotFoundError(json_path + ' does not exist')
        else:
            with open(json_path, 'r') as infile:
                dataset_doc = json.load(infile)
                infile.close()
            return dataset_doc

    def _save_img_array_as_bmp(self, img_array, original_image_name, *,
                               train_or_test):
        """
        create directory of .bmp files in our temporary directory,
        save converted image in this new directory
        """
        train_or_test_dir = os.path.join(self.tmp_dir, train_or_test)
        self._mkdir(train_or_test_dir)
        train_or_test_ts_dir = os.path.join(train_or_test_dir, 'timeseries')
        self._mkdir(train_or_test_ts_dir)
        self.bmp_ser_dirs[train_or_test] = train_or_test_ts_dir
        bmp_dir = (os.path.join(train_or_test_dir, 'bmp') + '_' +
            train_or_test)
        self._mkdir(bmp_dir)
        self.bmp_dirs[train_or_test] = bmp_dir

        bmp_outfile = original_image_name.split('.')[0] + '.bmp'
        bmp_outfile_path = os.path.join(bmp_dir, bmp_outfile)
        imwrite(bmp_outfile_path, img_array)

    def _convert_to_bmp(self, image_dir, *, train_or_test, axis=2):
        """
        iterate over non-.bmp images in raw image directory
        """
        if self.tmp_dir == '':
            prefix = self.dataset_name + '-'
            self.tmp_dir = tempfile.mkdtemp(prefix=prefix, dir='./')
        for image in os.listdir(image_dir):
            image_path = os.path.join(image_dir, image)
            img_array = imread(image_path)
            img_dim = img_array.shape
            if np.product(img_array.shape) > 16384:
                warnings.warn("image larger than 16384", UserWarning)

            # TODO: perhaps add RGB+ later as a multichannel problem
            #elif len(img_dim) == 3:
            #    for channel, img_array_ in enumerate(img_array[:,:,]):
            #        self._save_img_array_as_bmp(img_array_, image,
            #                                    str(channel),
            #                                    train_or_test=train_or_test)
            #if len(img_dim) == 2:
            self._save_img_array_as_bmp(img_array, image,
                                        train_or_test=train_or_test)

    def _serialize_bmp_dir(self, *, train_or_test, **kwargs):
        """
        iterate over .bmp files in and serialize each,
        save the result in a csv
        """
        bmp_dir = self.bmp_dirs[train_or_test]
        csv_dir = self.bmp_ser_dirs[train_or_test]
        for bmp_file in os.listdir(bmp_dir):
            csv_outfile = os.path.join(csv_dir, (bmp_file.split('.')[0] +
                                                 '.csv'))
            bmp_file_path = os.path.join(bmp_dir, bmp_file)
            serializer(bmp_file_path, outfile=csv_outfile, **kwargs)
            d3m_ts_format = pd.read_csv(csv_outfile, delimiter=' ',
                                        header=None, lineterminator=' ',
                                        comment='\n', names=['val'])
            d3m_ts_format.to_csv(csv_outfile, index_label='time')

    @staticmethod
    def _detect_if_images(doc):
        """

        """
        resTypes = set()
        for dR in doc["dataResources"]:
            resTypes.add(dR["resType"])
        if "image" in resTypes:
            return True
        else:
            return False

    def load_dataset(self, *, data_dir, doc_json='datasetDoc.json',
                     train_or_test, verbose=False, **kwargs):
        """

        """
        json_path = os.path.join(data_dir, doc_json)
        doc = self._load_table(json_path=json_path)
        self.dataset_name = doc['about']['datasetName'].replace(' ',
                                                                '_').replace('/',
                                                                             '-')

        if self._is_raw_images is None:
            self._is_raw_images = self._detect_if_images(doc)

        if verbose:
            options = ["'timeseries'", "'image'"]
            print("Dataset of type", options[int(self._is_raw_images)],
                  "detected.")

        if self._is_raw_images:
            image_resource = next(dR for dR in doc["dataResources"] if dR["resType"] ==
                                  "image")
            image_dir = image_resource["resPath"]
            image_dir_path = os.path.join(data_dir, image_dir)
            self._convert_to_bmp(image_dir_path, train_or_test=train_or_test)
            self._serialize_bmp_dir(train_or_test=train_or_test, **kwargs)
            for dR in doc["dataResources"]:
                if dR["resType"] == "image":
                    index = doc["dataResources"].index(dR)
                    doc["dataResources"][index]["resPath"] = 'timeseries/'
                    doc["dataResources"][index]["resType"] = 'timeseries'
                    doc["dataResources"][index]["resFormat"] = ['text/csv']
                    columns = [
                        {
                            "colIndex": 0,
                            "colName": "time",
                            "colType": "integer",
                            "role": ["timeIndicator"]
                        },
                        {
                            "colIndex": 1,
                            "colName": "val",
                            "colType": "real",
                            "role": ["attribute"]
                        }
                    ]
                    doc["dataResources"][index]["columns"] = columns
                    #dR["resPath"] = 'timeseries'
            mock_dir = os.path.join(self.tmp_dir, train_or_test)
            json_outfile = os.path.join(mock_dir, 'datasetDoc.json')
            with open(json_outfile, 'w+') as outfile:
                json.dump(doc, outfile, indent=4)
            table = next(dR for dR in doc["dataResources"] if dR["resType"] ==
                         "table")
            table_dir = table["resPath"]
            table_path = table_dir.split('/')[0]
            old_table_loc = os.path.join(data_dir, table_path)
            new_table_loc = os.path.join(mock_dir, table_path)
            copytree(old_table_loc, new_table_loc,
                     ignore=ignore_patterns('*.csv'))

            learningData_path = os.path.join(data_dir, table_dir)
            file_df = pd.read_csv(learningData_path)
            for dR in doc["dataResources"]:
                if dR["resType"] == "table":
                    attribute_col = self._role_col_name('attribute', dR)[0]
            file_df[attribute_col] = file_df[attribute_col].apply(lambda x:
                                                                      x.split('.')[0] + '.csv')
            new_learningData_path = os.path.join(mock_dir, table_dir)
            file_df.to_csv(new_learningData_path, index=False)
            data_dir = mock_dir

        if train_or_test.lower() == "train":
            self._train_dir = data_dir
            self._train_doc = doc
        elif train_or_test.lower() == "test":
            self._test_dir = data_dir
            self._test_doc = doc

    @property
    def train_dir(self):
        return self._train_dir

    @train_dir.setter
    def train_dir(self, root_dir):
        self._train_dir = root_dir

    @property
    def test_dir(self):
        return self._test_dir

    @test_dir.setter
    def test_dir(self, root_dir):
        self._test_dir = root_dir

    @staticmethod
    def _role_col_name(role, json_dict):
        """

        """
        column = []
        if "columns" in json_dict:
            column = [column["colName"] for column in json_dict["columns"] if role in
                    column["role"]]
        # temporary fix for incorrectly documented uu1_datasmash dataset
        else:
            column = ["val"]
        return column

    def _get_timeseries_col(self):
        """

        """
        time_series_doc = next(dR for dR in self._train_doc["dataResources"]
                               if dR["resType"] == 'timeseries')
        self.time_series_cols = self._role_col_name('attribute', time_series_doc)

    def _write_time_series(self, file_df, file_col, colName, resPath, lib_path):
        """
        file_df : dataframe with column that contains filenames of the
        timeseries
        file_col : name of the column of filenames
        colName : name of column that contains timeseries values
        resPath : name of directory that contains the files
        lib_path : name of the output library files
        """
        for file_ in file_df[file_col]:
            file_path = os.path.join(resPath, file_)

            time_series = pd.read_csv(file_path)[colName].dropna().tolist()
            if time_series != []:
                with open(lib_path, 'a') as outfile:
                    wr = csv.writer(outfile, delimiter=' ', quoting=csv.QUOTE_NONE)
                    wr.writerow(time_series)

    def write_libs(self, *, problem_type):
        """

        """
        self._get_timeseries_col()
        if self.tmp_dir == '':
            prefix = self.dataset_name + '-'
            self.tmp_dir = tempfile.mkdtemp(prefix=prefix, dir='./')
        table = next(dR for dR in self._train_doc["dataResources"]
                     if dR["resType"] == "table")
        timeseries_path = next(dR for dR in self._train_doc["dataResources"]
                               if dR["resType"] == "timeseries")["resPath"]
        columns = [column["colName"] for column in table["columns"]]
        index_col = self._role_col_name("index", table)
        ts_col = self._role_col_name("attribute", table)[0]  # "time_series_file"
        class_col = self._role_col_name("suggestedTarget", table)

        table_path = table["resPath"]
        file_df = pd.read_csv(os.path.join(self._train_dir, table_path))
        if problem_type.lower() == 'supervised':
            # currently does not support multilabel (i.e., assumes class_col has
            # only one element)
            class_col = class_col[0]
            class_list = file_df[class_col].unique().tolist()

        # TODO - assumes "timeseries" as name of directory (could be images)
        timeseries_dir = os.path.join(self._train_dir, timeseries_path)

        for channel_num, time_series_col in enumerate(self.time_series_cols):
            lib_names = []
            channel_dir = 'channel_' + str(channel_num)
            channel_path = os.path.join(self.tmp_dir, channel_dir)
            os.mkdir(channel_path)
            self.channel_dirs.append(channel_dir)
            if problem_type.lower() == 'supervised':
                file_list = os.path.join(channel_path, 'library_list')
                for class_ in class_list:
                    lib_name = 'train_class_' + str(class_)
                    lib_path = os.path.join(channel_path, lib_name)
                    class_df = file_df[file_df[class_col] == class_]
                    num_time_series = len(class_df)

                    # TODO - hardcoded path
                    self._write_time_series(class_df, ts_col,
                                            time_series_col, timeseries_dir,
                                            lib_path)
                    with open(file_list, 'a') as outfile:
                        writer = csv.writer(outfile, delimiter=' ',
                                            quoting=csv.QUOTE_NONE)
                        writer.writerow([lib_name, class_, num_time_series])
                    lib_names.append(lib_path)
            elif problem_type.lower() == 'unsupervised':
                dataset_path = os.path.join(channel_path, 'dataset')
                self._write_time_series(file_df, ts_col,
                                        time_series_col, timeseries_dir,
                                        dataset_path)
                lib_names.append(dataset_path)
            self.channel_problems[channel_dir] = [None, lib_names]
        return self.tmp_dir, self.channel_dirs, len(file_df)

    def write_test(self):
        """

        """
        test_dir = os.path.join(self.tmp_dir, 'test')
        self._mkdir(test_dir)
        table = next(dR for dR in self._test_doc["dataResources"] if dR["resType"] ==
                     "table")
        table_path = table["resPath"]
        timeseries_path = next(dR for dR in self._test_doc["dataResources"]
                               if dR["resType"] == "timeseries")["resPath"]
        ts_col = self._role_col_name("attribute", table)[0]  # "time_series_file"
        file_df = pd.read_csv(os.path.join(self._test_dir, table_path))
        timeseries_dir = os.path.join(self._test_dir, timeseries_path)
        for time_series_col, channel_dir in zip(self.time_series_cols,
                                                self.channel_dirs):
            test_channel_dir = os.path.join(test_dir, channel_dir)
            os.mkdir(test_channel_dir)
            test_channel_file = os.path.join(test_channel_dir, 'test')
            self._write_time_series(file_df, ts_col,
                                    time_series_col, timeseries_dir,
                                    test_channel_file)
            self.channel_problems[channel_dir][0] = test_channel_file
        return self.channel_problems


def argmax_prod_matrix_list(matrix_list, *, axis=1):
    """

    """
    start = np.ones(matrix_list[0].shape)
    for matrix in matrix_list:
        start *= matrix
    return np.argmax(start, axis=axis)


def matrix_list_p_norm(matrix_list, *, p=2):
    """

    """
    matrix_list_power = np.array([np.power(matrix, p) for matrix in
                                  matrix_list])
    sum_ = np.sum(matrix_list_power, axis=0)
    norm = np.power(sum_, 1/p)
    return norm


def pprint_dict(dictionary):
    """

    """
    for k, v in dictionary.items():
        print(k + ':', v)
    print('\n')


