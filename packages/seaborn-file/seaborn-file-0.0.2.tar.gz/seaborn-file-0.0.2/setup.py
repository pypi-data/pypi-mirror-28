from setuptools import setup, find_packages

setup(
    name='seaborn-file',
    version='0.0.2',
    description='SeabornFile enables the manipulation of the'
                'directories of a computer within a program.',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/File',
    download_url='https://github.com/SeabornGames/File'
                 '/tarball/download',
    keywords=['os'],
    install_requires=[],
    extras_require={
    },
    packages=['seaborn'] + ['seaborn.' + i
                            for i in find_packages(where='./seaborn')],
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
)
