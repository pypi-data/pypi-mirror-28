
from setuptools import setup
from setuptools import find_packages
from glob import glob

data_files =[
        # ("/etc/probe", glob('conf/*.conf.*')),
        ("/etc/probe", ['conf/probe.conf']),
        ("/etc/init.d", ['bin/init.d/probe'])
        ]

install_requires = ['configobj', 'setproctitle', ]
version = "0.0.2"

setup(
        name='python-probe',
        version=version,
        url='http://null.com',
        author='Yankun Li',
        author_email="lioveni99@gmail.com",
        license='MIT',
        description='probe ceph cluster status',
        package_dir={'':'src'},
        packages=['probe', 'probe.common'],
        # packages=find_packages(exclude=['probe', 'probe.common']),
        scripts=['bin/probe'],
        package_data={
            '': ['*.txt', '*.rst'],
            'doc':['*.*'],
            'conf':['*.conf'],
            },
        data_files=data_files,
        install_requires=install_requires,
        classifiers=[
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ]
)

