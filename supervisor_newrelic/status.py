#!/usr/bin/env python
"""
Event listener which should be subscribed to PROCESS_STATE events.
Sends state to New Relic when processes transition.

Supervisor configuration would look something like this:
[eventlistener:status]
command = /usr/bin/status --account <NEWRELIC_ACCOUNT_NO> --key <NEWRELIC_KEY>
events = PROCESS_STATE
"""

import argparse
import requests
import sys

from supervisor import childutils

class Status(object):

    def __init__(self, account, key):
        self.account = account
        self.key = key
        self.stdin = sys.stdin
        self.stdout = sys.stdout

    def run(self, runonce=False):
        while True:
            headers, payload = childutils.listener.wait(
                    self.stdin, self.stdout)

            if not headers['eventname'].startswith('PROCESS_STATE_'):
                # Ignore other state changes
                childutils.listener.ok(self.stdout)
                if runonce:
                    break
                continue

            pheaders, pdata = childutils.eventdata(payload+'\n')

            if self.send(pheaders['processname'], pheaders['groupname'],
                    headers['eventname']):
                childutils.listener.ok(self.stdout)
            else:
                childutils.listener.fail(self.stdout)

            if runonce:
                break


    def send(self, name, group, status):
        data = [{
                'eventType': 'Supervisor:Status',
                'processName': name,
                'groupName': group,
                'status': status,
        }]
        url = ('https://insights-collector.newrelic.com/'
                'v1/accounts/%s/events' % self.account)
        headers = {'X-Insert-Key': self.key}
        response = requests.post(url, json=data, headers=headers)

        return response.status_code == requests.codes.ok

def main():
    parser = argparse.ArgumentParser(description='Supervisor event listener')
    parser.add_argument('--account', '-a', help='New Relic account number')
    parser.add_argument('--key', '-k', help='New Relic Insights insert key')
    args = parser.parse_args()

    status = Status(args.account, args.key)
    status.run()

if __name__ == '__main__':
    main()
