from setuptools import setup  # type: ignore

setup(
    name='edpanalyst',
    packages=['edpanalyst'],
    scripts=['bin/edp_predict_probabilities'],
    version='0.1.10',
    description='The python API to the Empirical Data Platform.',
    license='Apache License 2.0',
    install_requires=[
        'configparser', 'future', 'natsort', 'pandas', 'requests', 'tqdm',
        'typing', 'enum34'
    ]
)  # yapf: disable
