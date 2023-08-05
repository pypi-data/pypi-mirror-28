import setuptools

setuptools.setup(
    name='pycmdtools',
    version='0.0.55',
    description='pycmdtools is set of useful command line tools written in python',
    long_description='pycmdtools is set of useful command line tools written in python',
    url='https://veltzer.github.io/pycmdtools',
    download_url='https://github.com/veltzer/pycmdtools',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python command line shell utilities',
    packages=setuptools.find_packages(),
    install_requires=[
        'click',  # for command line parsing
        'tqdm',  # for progress report
        'requests',  # for google drive download
        'pylogconf',  # for logging
        'numpy',  # for sampling
        'pandas',  # for sampling
        'unidecode',  # for sampling
        'pyyaml',  # for yaml
    ],
    entry_points={
        # order of console_scripts is the same order of files in the 'scripts' folder
        'console_scripts': [
            'pycmdtools_change_first_line=pycmdtools.scripts.change_first_line:main',
            'pycmdtools_count=pycmdtools.scripts.count:main',
            'pycmdtools_find_bad_symlinks=pycmdtools.scripts.find_bad_symlinks:main',
            'pycmdtools_google_drive_download=pycmdtools.scripts.google_drive_download:main',
            'pycmdtools_mcmp=pycmdtools.scripts.mcmp:main',
            'pycmdtools_print_all_args=pycmdtools.scripts.print_all_args:main',
            'pycmdtools_remove_bad_symlinks=pycmdtools.scripts.remove_bad_symlinks:main',
            'pycmdtools_stats=pycmdtools.scripts.stats:main',
            'pycmdtools_uniq=pycmdtools.scripts.uniq:main',
            'pycmdtools_validate_json=pycmdtools.scripts.validate_json:main',
            'pycmdtools_validate_yaml=pycmdtools.scripts.validate_yaml:main',
            'pycmdtools_progress=pycmdtools.scripts.progress:main',
            'pycmdtools_sample_weighted=pycmdtools.scripts.sample_weighted:main',
        ],
    },
)
