from setuptools import setup

setup(name='datasmash',
      version='0.1.2',
      packages=['datasmash.bin', 'datasmash',
                'datasmash.primitive_interfaces',
                'datasmash.primitive_interfaces.types'],
      install_requires=['pandas', 'numpy', 'scikit-learn', 'imageio'],
      include_package_data=True,
        package_data={
            'bin':
                ['bin/smash',
                 'bin/embed',
                 'bin/smashmatch',
                 'bin/Quantizer',
                 'bin/serializer',
                 'bin/genESeSS'
                ]
        },

      # metadata for PyPI upload
      url='https://gitlab.datadrivendiscovery.org/uchicago/datasmash',
      download_url='https://gitlab.datadrivendiscovery.org/uchicago/datasmash/archive/0.1.2.tar.gz',

      maintainer_email='wmowkm@gmail.com',
      maintainer='Warren Mo',

      description='Quantifier of universal similarity amongst arbitrary data streams without a priori knowledge, features, or training.',

      classifiers=[
          "Programming Language :: Python :: 3"
      ]
)
