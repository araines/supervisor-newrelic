from distutils.core import setup

version = 'v1.0.9'

setup(
    name = 'supervisor_newrelic',
    version = version,
    description = 'Collection of Supervisor plugins to provide metrics and monitoring within New Relic',
    author = 'Sportlobster',
    author_email = 'info@sportlobster.com',
    license = 'MIT',
    url = 'https://github.com/sportlobster/supervisor-newrelic',
    download_url = 'https://github.com/sportlobster/supervisor-newrelic/tarball/%s' % version,
    long_description = open('README.rst').read(),
    keywords = ['supervisor', 'supervisord', 'newrelic', 'monitoring'],
    classifiers = [],

    install_requires = ['requests', 'supervisor'],
    tests_require = ['nose', 'mock'],
    test_suite = 'nose.collector',

    packages = ['supervisor_newrelic'],
    entry_points = {
        'console_scripts': {
            'supervisor_newrelic_status = supervisor_newrelic.status:main',
            'supervisor_newrelic_worker_monitor = supervisor_newrelic.worker_manager:main',
        },
    },
)
