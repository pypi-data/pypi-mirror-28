from setuptools import setup, find_packages

setup(
    name='seaborn-meta',
    version='0.0.2',
    description='SeabornMeta allows for simple changing'
                'of names between conventions, as well'
                'as auto-generating init files',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/meta',
    download_url='https://github.com/SeabornGames/meta'
                 '/tarball/download',
    keywords=['meta'],
    install_requires=[
    ],
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
