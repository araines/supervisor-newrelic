from distutils.core import setup

version = '1.0.9'

setup(
    name = 'supervisor_newrelic_displate',
    version = version,
    description = 'Collection of Supervisor plugins to provide metrics and monitoring within New Relic',
    author = 'Displate',
    author_email = '',
    license = 'MIT',
    url = 'https://github.com/displate/supervisor-newrelic',
    download_url = 'https://github.com/displate/supervisor-newrelic/tarball/%s' % version,
    long_description = open('README.rst').read(),
    keywords = ['supervisor', 'supervisord', 'newrelic', 'monitoring'],
    classifiers = [],

    install_requires = [
        'requests>=2.4.2',
        'setuptools>=38.0.0',
        'supervisor>=3.3.3',
    ],
    tests_require = ['nose', 'mock'],
    test_suite = 'nose.collector',

    packages = ['supervisor_newrelic_displate'],
    entry_points = {
        'console_scripts': {
            'supervisor_newrelic_status = supervisor_newrelic.status:main',
        },
    },
)
