from setuptools import setup, find_packages

try:
    from pypandoc import convert
    def read_md(f):
        return convert(f, 'rst')
except ImportError:
    import sys
    print("WARNING: pypandoc module not found.\nCould not convert Markdown to RST", file=sys.stderr)
    def read_md(f): return open(f, 'r').read()


version = '0.1'
setup(
    name='emg_analyzer',
    version=version,
    maintainer='Bertrand Neron',
    maintainer_email='freeh4cker@gmail.com',
    author='Bertrand Neron',
    author_email='freeh4cker@gmail.com',
    long_description=read_md('README.md'),
    keywords=['EMG', 'data science', 'data normalization'],
    description='parse emg recording and normalize the voltage',
    license='BSD3',
    platforms=['Unix', 'Linux', 'MacOsX'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers ',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    zip_safe=False,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=open("requirements.txt").read().split(),

    entry_points={
        'console_scripts': [
           'emg_norm=emg_analyzer.scripts.emg_norm:main',
           'emg_group_tracks=emg_analyzer.scripts.emg_group_tracks:main',
        ]
    }

)
