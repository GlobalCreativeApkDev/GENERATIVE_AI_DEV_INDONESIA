from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='gemini_cli_tactics',
    version='1',
    packages=['gemini_cli_tactics'],
    url='https://github.com/GlobalCreativeApkDev/GENERATIVE_AI_DEV_INDONESIA/tree/gcapkdev/gemini_cli_tactics',
    license='MIT',
    author='GlobalCreativeApkDev',
    author_email='globalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of a turn-based strategy RPG on command-line interface '
                'with Google Gemini AI integrated into it.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "gemini_cli_tactics=gemini_cli_tactics.gemini_cli_tactics:main",
        ]
    }
)