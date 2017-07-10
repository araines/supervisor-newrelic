.. image:: https://codeship.com/projects/aba10710-9dfd-0134-7e83-328bd15b6072/status?branch=master
    :target: https://codeship.com/projects/188837
.. image:: https://badge.fury.io/py/supervisor_newrelic.svg
    :target: https://badge.fury.io/py/supervisor_newrelic
.. image:: https://img.shields.io/badge/language-Python-blue.svg
.. image:: https://img.shields.io/badge/license-MIT-blue.svg

supervisor_newrelic
===================

Collection of `Supervisor <http://supervisord.org>`_ plugins to provide metrics
and monitoring within `New Relic <https://newrelic.com/>`_.

status plugin
-------------

This plugin should be subscribed to the ``PROCESS_STATE`` events.  It sends
an event to New Relic every time a process changes state.

Installation
************

`Register an Insights API Insert Key
<https://docs.newrelic.com/docs/insights/new-relic-insights/custom-events/insert-custom-events-insights-api#register>`_

Install via pip::

    pip install supervisor_newrelic

Configuration for Supervisor Status Monitoring
**********************************************

Create a new configuration file: ``/etc/supervisor.d/newrelic.conf`` with contents::

    [eventlistener:newrelic_status]
    command = supervisor_newrelic_status --account <NEWRELIC_ACCOUNT_NO> --key <NEWRELIC_KEY>
    events = PROCESS_STATE

Where:

- NEWRELIC_ACCOUNT_NO gets replaced with your NewRelic account number (e.g. 1121234)
- NEWRELIC_KEY gets replaced with the Insights API Insert Key (as registered earlier - e.g. VkiYX90CZxxPl7FuQAxrQXNv5gZnx80e)

Reload the supervisord configuration::

    supervisorctl reread

You should now start to see events in New Relic Insights in the Custom Events
section named ``Supervisor:Status``.  Each event will have the following
attributes:

- processName: The name of the process which changed status
- groupName: The name of the group which changed status
- status: The status it changed to

Configuration for Worker Monitoring
***********************************

Create a new configuration file: ``/etc/supervisor.d/conf.d/newrelic.conf`` with contents::

	[program:worker_monitor]
command = supervisor_newrelic_worker_monitor --account <NEWRELIC_ACCOUNT_NO> --key <NEWRELIC_KEY> --event_type <EVENT_NAME_FOR_APPLICATION_IN_NEW_RELIC> --supervisor_conf <SUPERVISOR_CONFIGURATION_FILE_FOR_THE_WORKER>

Where:

- NEWRELIC_ACCOUNT_NO gets replaced with your NewRelic account number (e.g. 1121234)
- NEWRELIC_KEY gets replaced with the Insights API Insert Key (as registered earlier - e.g. VkiYX90CZxxPl7FuQAxrQXNv5gZnx80e)
- EVENT_NAME_FOR_APPLICATION_IN_NEW_RELIC eg. WorkerMonitor
- SUPERVISOR_CONFIGURATION_FILE_FOR_THE_WORKER gets replaced by the your wokrer configuration present in /etc/supervisor.d/conf.d/ - e.g. my_app.conf

Reload the supervisord configuration::

    supervisorctl reread

You should now start to see events in New Relic Insights in the Custom Events
section named ``Worker:Monitor``.  Each event will have the following
attributes:


- commandName: The name of the worker/command to be monitored
- cpuPercentage: CPU% consumption of the command
- memory: RSS (real memory size in Kb) for the command

Currently this supports parsing of symfony(php) commands with syntax : ``xxx api:service_name yy``
eg : ``app/console api:service_name http://subdoman.domain.com``

 To support parsing for other frameworks kindly override the ``parse_phpsymfony_command`` method in worker_manager.py
