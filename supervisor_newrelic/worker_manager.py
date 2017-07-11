import argparse
from supervisor_newrelic.status import Status
import time
import os
import subprocess


def push_monitoring_data(command_list, status, event_type):
    '''
    headers of ps_aux_row_data
    ['USER',
     'PID',
     '%CPU',
     '%MEM',
     'VSZ',
     'RSS',
     'TTY',
     'STAT',
     'START',
     'TIME',
     'COMMAND']
    '''
    ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
    processes = ps.split('\n')
    nfields = len(processes[0].split()) - 1
    for row in processes[1:]:
        ps_aux_row_data = row.split(None, nfields)
        for command in command_list:
            if len(ps_aux_row_data) and command in ps_aux_row_data[-1]:
                status.send_worker_monitoring_data(
                    command,
                    ps_aux_row_data[2], #cpu_percentage
                    ps_aux_row_data[5], #RSS -> RAM  consumption
                    event_type
                )
                break


def parse_phpsymfony_command(command_list, command):
    '''specific to application. Write your own logic to make command_name
    eg -
        command = 'app/console command_name host'
    '''
    command_name = command.split(" ",2)[1]
    command_list.append(command_name)
    return command_list


def parse_supervisor_command(
        command_list, supervisor_command_line, parsing_function=None):
    ''' supervisor_command_line format assumption: 'command = php7 command_name'
        if application/framework specific parsing pass the function as argument.
    '''
    command = supervisor_command_line.split(" ", 3)[-1]
    if parsing_function:
        command_list = parsing_function(command_list, command)
    else:
        command_list.append(command)


def process_command_monitoring_details(
        supervisor_file_name, status, event_type, time_seconds):
    if supervisor_file_name:
        while True:
            supervisor_conf = os.path.join(
                '/etc/supervisor/conf.d',
                supervisor_file_name
            )
            command_list = []
            with open(supervisor_conf) as f:
                for line in f.readlines():
                    if len(line) and line.startswith('command'):
                        parse_supervisor_command(
                            command_list,
                            line,
                            parse_phpsymfony_command
                        )
            push_monitoring_data(command_list, status, event_type)
            time.sleep(time_seconds)



def main():
    parser = argparse.ArgumentParser(description='Supervisor command monitor')
    parser.add_argument('--account', '-a', help='New Relic account number')
    parser.add_argument('--key', '-k', help='New Relic Insights insert key')
    parser.add_argument(
        '--event_type',
        '-e',
        help='Application Event Name to appear in new relic dashboard'
    )
    parser.add_argument('--supervisor_conf', '-s', help='supervisor_file_name')
    parser.add_argument('--time_seconds', '-s', help='time_interval')
    args = parser.parse_args()

    status = Status(args.account, args.key)
    process_command_monitoring_details(
        args.supervisor_conf,
        status,
        args.event_type,
        args.time_seconds
    )


if __name__ == '__main__':
    main()
