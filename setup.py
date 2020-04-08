from setuptools import setup, find_packages


with open('requirements.txt') as fp:
    requirements = fp.read()

setup(
    name="corona-bg",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'dev': ['ipython', 'ipdb'],
    },
)
