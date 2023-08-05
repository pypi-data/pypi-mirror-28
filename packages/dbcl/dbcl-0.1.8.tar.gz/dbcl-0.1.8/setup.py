from setuptools import setup

setup(
    name='dbcl',
    version='0.1.8',
    description='A database command line interface that is engine-agnostic.',
    author='Kris Steinhoff',
    url='https://github.com/ksofa2/dbcl',
    download_url='https://github.com/ksofa2/dbcl/archive/0.1.8.tar.gz',

    keywords=['db', 'command-line-tool'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages=['dbcl'],
    entry_points={
        'console_scripts': ['dbcl=dbcl.command_line:command_loop'],
    },
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
        'prompt_toolkit',
        'pygments',
        'terminaltables',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
    ],
)
