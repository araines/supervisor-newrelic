import mock
import unittest

from StringIO import StringIO
from supervisor_newrelic.status import Status

def mock_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if (args[0] == 'https://insights-collector.newrelic.com/v1/accounts/123/events' and
            kwargs.get('headers').get('X-Insert-Key') == 'abc'):
        return MockResponse({'foo': 'bar'}, 200)

    return MockResponse({}, 404)

class StatusTests(unittest.TestCase):

    def _get_mock(self, account='123', key='abc'):
        prog = Status(account, key)
        prog.stdin = StringIO()
        prog.stdout = StringIO()

        return prog

    def test_run_not_process_state_fatal(self):
        prog = self._get_mock()
        prog.stdin.write('eventname:PROCESS_STATE len:0\n')
        prog.stdin.seek(0)
        prog.run(runonce=True)
        self.assertEqual(prog.stdout.getvalue(), 'READY\nRESULT 2\nOK')

    @mock.patch('supervisor_newrelic.status.requests.post', side_effect=mock_request)
    def test_run_successful_fatal_state_report(self, m):
        payload = 'processname:foo groupname:bar from_state:BACKOFF'
        prog = self._get_mock()
        prog.stdin.write('eventname:PROCESS_STATE_FATAL len:%d\n' % len(payload))
        prog.stdin.write(payload)
        prog.stdin.seek(0)
        prog.run(runonce=True)
        self.assertEqual(prog.stdout.getvalue(), 'READY\nRESULT 2\nOK')

    @mock.patch('supervisor_newrelic.status.requests.post', side_effect=mock_request)
    def test_run_unsuccessful_fatal_state_report(self, m):
        payload = 'processname:foo groupname:bar from_state:BACKOFF'
        prog = self._get_mock('234')
        prog.stdin.write('eventname:PROCESS_STATE_FATAL len:%d\n' % len(payload))
        prog.stdin.write(payload)
        prog.stdin.seek(0)
        prog.run(runonce=True)
        self.assertEqual(prog.stdout.getvalue(), 'READY\nRESULT 4\nFAIL')
