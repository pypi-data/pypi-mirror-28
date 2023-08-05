import time
import os
import numpy as np
import subprocess as sp
from datasmash.utils import quantize_inplace, quantizer, DatasetLoader
from datasmash.utils import pprint_dict, argmax_prod_matrix_list
from datasmash.primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase
from datasmash.config import CWD, BIN_PATH


class SmashClassification(SupervisedLearnerPrimitiveBase):
    """

    """
    def __init__(self, *, bin_path=BIN_PATH):
        assert os.path.isfile(os.path.join(bin_path, 'smashmatch')), "invalid bin path."
        self.bin_path = os.path.abspath(os.path.join(bin_path, 'smashmatch'))
        self.channel_partition_map = {}
        self.cwd = os.getcwd()
        self.d3m_reader = DatasetLoader()
        self.tmp_dir = ''
        self.channel_dirs = []
        self._selected_channels = set()
        self.detrending = False
        self.inplace = True
        self.channel_probabilities = {}
        self._channel_predictions = {}

    @property
    def selected_channels(self):
        return self._selected_channels

    @selected_channels.setter
    def selected_channels(self, channels):
        if not isinstance(channels, list):
            channels_ = [channels]
        else:
            channels_ = channels
        channels_ = ['channel_' + str(c) for c in channels_]
        self._selected_channels = set(channels_)

    def set_training_data(self, training_data_dir, *,
                          dataset_doc_json='datasetDoc.json',
                          verbose=False, **kwargs):
        """

        """
        self.d3m_reader.load_dataset(data_dir=training_data_dir,
                                     doc_json=dataset_doc_json,
                                     train_or_test='train',
                                     verbose=verbose, **kwargs)
        self.tmp_dir, self.channel_dirs, _ = (
            self.d3m_reader.write_libs(problem_type='supervised'))

    def _fit_one_channel(self, directory, *, detrending=False, inplace=True,
                         **kwargs):
        """

        """
        self.detrending = detrending
        self.inplace = inplace
        partition = quantizer(directory,
                              bin_path=BIN_PATH,
                              problem_type='supervised',
                              detrending=detrending,
                              inplace=inplace,
                              **kwargs)
        return partition

    def fit(self, *, verbose=False, channels=None, **kwargs):
        """

        """
        if channels is not None:
            if channels == -1:
                pass
            elif not isinstance(channels, list):
                channels = [channels]
            selected_channels = ['channel_' + str(c) for c in channels]
            self._selected_channels = set(selected_channels)
        elif bool(self._selected_channels):
            selected_channels = self.selected_channels
        else:
            selected_channels = self.channel_dirs

        for channel_dir in selected_channels:
            directory = os.path.join(self.tmp_dir, channel_dir)
            partition = self._fit_one_channel(directory, **kwargs)
            self.channel_partition_map[channel_dir] = partition

        if verbose:
            print('Quantizing in place:', self.inplace)
            print('Chosen partition:')
            pprint_dict(self.channel_partition_map)

    @staticmethod
    def _argmax_prod_matrix_list(matrix_list, *, axis=1):
        """

        """
        start = np.ones(matrix_list[0].shape)
        for matrix in matrix_list:
            start *= matrix
        return np.argmax(start, axis=axis)

    def produce(self, test_dir, *,
                data_type=None,
                dataset_doc_json='datasetDoc.json',
                partition=None,
                num_reruns=50,
                channels=None,
                verbose=False):
        """

        """
        partition_check = bool(self.channel_partition_map) or (partition is not None)
        assert partition_check, "partition must be found via 'fit()' or inputted"
        if partition is not None:
            current_partition = partition
        elif self.channel_partition_map is not None:
            current_partition = self.channel_partition_map
        self.d3m_reader.load_dataset(data_dir=test_dir,
                                     doc_json=dataset_doc_json,
                                     train_or_test='test')

        if channels is not None:
            if not isinstance(channels, list):
                channels = [channels]
            if bool(self._selected_channels):
                for channel in channels:
                    if channel not in self._selected_channels:
                        raise ValueError("The partition was not found for this "
                                         "channel. Re-run 'fit()' with this "
                                         "channel included before running "
                                         "'produce()' with this channel.")

        channel_problems = self.d3m_reader.write_test()

        smashmatch = [self.bin_path]
        nr = str(num_reruns)
        for channel, problem in channel_problems.items():
            if channels is not None:
                channels_ = ['channel_' + str(c) for c in channels]
                if channel not in channels_:
                    if verbose:
                        print('Excluding', channel, '...')
                    continue
            elif bool(self._selected_channels) and (channel not in
                self._selected_channels):
                if verbose:
                    print('Excluding', channel, '...')
                continue

            if verbose:
                start = time.time()
            test_file = problem[0]
            if self.inplace:
                quantize_inplace(test_file, current_partition[channel])
                partition = []
                dtype = ['-T', 'symbolic']
            else:
                error_msg = ("keyword-only argument 'data_type' must be set if"
                             "'inplace' keyword-only argument of 'fit()'"
                             "method was set to False")
                assert data_type is not None, error_msg
                partition = ['-P'] + current_partition[channel]
                dtype = ['-T', data_type]
            lib_files = problem[1]
            file_in = ['-f', test_file, '-F'] + lib_files
            output_prefix = os.path.join(self.tmp_dir, 'test', channel, 'out')
            file_out = ['-o', output_prefix]
            constants = dtype + ['-D', 'row']
            _num_reruns = ['-n', nr]
            detrending = ['-u', str(int(self.detrending))]
            command_list = (smashmatch + file_in + file_out + constants + partition
                           + _num_reruns + detrending)

            sp.check_output(command_list)
            out_prob = np.loadtxt(output_prefix + '_prob')
            out_class = np.loadtxt(output_prefix + '_class')
            self.channel_probabilities[channel] = out_prob
            self._channel_predictions[channel] = out_class
            if verbose:
                print('CHANNEL ' + channel.split('_')[-1] + ' DONE')
                print(out_class)
                end = time.time()
                print('TIME:', end - start, '\n')
        prob_list = list(self.channel_probabilities.values())
        return argmax_prod_matrix_list(prob_list)

    @property
    def channel_predictions(self):
        return self._channel_predictions


    def get_params(self):
        """
        A noop
        """
        return None

    def set_params(self):
        """
        A noop
        """
        return None

