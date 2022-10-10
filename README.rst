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

Installation & Configuration
****************************

`Register an Insights API Insert Key
<https://docs.newrelic.com/docs/insights/new-relic-insights/custom-events/insert-custom-events-insights-api#register>`_

Install via pip::

    pip install supervisor_newrelic

Create a new configuration file: ``/etc/supervisor.d/newrelic.conf`` with contents::

    [eventlistener:newrelic_status]
    command = supervisor_newrelic_status --account <NEWRELIC_ACCOUNT_NO> --key <NEWRELIC_KEY> --param <PARAM_KEY> <PARAM_VALUE>
    events = PROCESS_STATE

Where:

- NEWRELIC_ACCOUNT_NO gets replaced with your NewRelic account number (e.g. 1121234)
- NEWRELIC_KEY gets replaced with the Insights API Insert Key (as registered earlier - e.g. VkiYX90CZxxPl7FuQAxrQXNv5gZnx80e)
- `--param` is optional param which can be set and send to New Relic with `key` set to `PARAM_KEY` and `value` set to `PARAM_VALUE`. Hint: multiple params can be set at the same time.

Reload the supervisord configuration::

    supervisorctl reread

You should now start to see events in New Relic Insights in the Custom Events
section named ``Supervisor:Status``.  Each event will have the following
attributes:

- processName: The name of the process which changed status
- groupName: The name of the group which changed status
- status: The status it changed to
- additional params (if added)
