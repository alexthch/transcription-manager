from setuptools import setup, find_packages

setup(
    name="transcribe-project",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'transcribe=package.cli:main',
        ],
    },
)
