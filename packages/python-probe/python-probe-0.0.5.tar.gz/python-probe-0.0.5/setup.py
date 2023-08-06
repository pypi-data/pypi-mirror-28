
from setuptools import setup
from setuptools import find_packages
from glob import glob

data_files =[
        # ("/etc/probe", glob('conf/*.conf.*')),
        ("/etc/probe", ['conf/probe.conf']),
        ("/etc/init.d", ['bin/init.d/probe']),
        ("/var/log/probe", [])
        ]

install_requires = ['configobj', 'setproctitle', ]
version = "0.0.5"

setup(
        name='python-probe',
        version=version,
        url='http://null.com',
        author='Yankun Li',
        author_email="lioveni99@gmail.com",
        license='MIT Licence',
        description='Probe ceph cluster status',
        package_dir={'':'src'},
        # packages=['probe', 'probe.common'],
        packages=find_packages(exclude=['docs']),
        # scripts=['bin/probe'],
        entry_points = {
            'console_scripts': [
                'probe = probe.probe_entry:main'
                ]
            },
        package_data={
            '': ['*.txt', '*.md'],
            'docs':['*.*'],
            'conf':['*.conf'],
            },
        data_files=data_files,
        install_requires=install_requires,
        include_package_data = True,
        classifiers=[
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ]
)

