from setuptools import setup, find_packages

setup(
    name="transcribe-manager",
    version="1.0a",
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'transcribe=package.cli:main',
        ],
    },
)
