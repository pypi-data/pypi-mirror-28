# Copyright 2015-2017 The MathWorks, Inc.

from setuptools import setup

if __name__ == '__main__':

    setup(
        name="rpi_feature_selection_toolbox",
        version="2.0.2",
        description='January Evaluation second submission',
        author='Keyi Liu, Zijun Cui, Qiang Ji',
        author_email="liuk7@rpi.edu",
        url='https://www.ecse.rpi.edu/~cvrl/',
        platforms=['Linux', 'Windows', 'MacOS'],
        packages=[
            'rpi_feature_selection_toolbox'
        ],
        package_data={'rpi_feature_selection_toolbox': ['*.ctf']},
    )


