from setuptools import setup

setup(
    name='dync',
    version='1.0',
    packages=['dync'],
    license='GPL2+',
    description='A tcp-based client for data transfer.',
    url='https://github.com/qbicsoftware/dync',
    author='Adrian Seyboldt',
    author_email='adrian.seyboldt@gmail.com',
    maintainer='Sven Fillinger',
    install_requires=['pyzmq', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'dync = dync.client:main',
            'dync-server = dync.server:main'
        ]
    }
)
