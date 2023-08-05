# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep
import subprocess
import logging


SERVICE_CMD = 'journalctl -u ethminer --since "{} seconds ago"'
SERVICE_STOP = 'systemctl stop ethminer'
SERVICE_START = 'systemctl start ethminer'


logger = logging.getLogger(__name__)


def check(delta_seconds=3*60):
    """ Check if the service has a recent active time (within 3 minutes) """
    has_recent = False
    for line in get_ethminer_service_output(delta_seconds):
        time = parse_time(line)
        if time:
            if is_old_time(time, delta_seconds):
                logger.debug('Found old time {}'.format(time))
            else:
                logger.debug('Found recent time {}'.format(time))
                has_recent = True
    if not has_recent:
        logger.info("No recent times found for ethminer!")
    else:
        logger.info("Ethminer recent status time found :)")
    return has_recent


def restart():
    """ Restart ethminer service - stop, one 1 second, start """
    logger.info('Restarting ethminer...')
    subprocess.Popen([SERVICE_STOP, ], shell=True)
    sleep(1)
    subprocess.Popen([SERVICE_START, ], shell=True)
    logger.info('Ethminer restarted')


def get_ethminer_service_output(delta_seconds):
    """ Get output line by line, including date, time, and output """
    command = SERVICE_CMD.format(delta_seconds)
    proc = subprocess.Popen([command, ], stdout=subprocess.PIPE, shell=True)
    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        else:
            break


def parse_time(line):
    """ Parse systemd time format to python date """
    line_segments = line.split()
    if len(line_segments) > 3:
        try:
            line_date = b' '.join(line_segments[:3]).decode()
            parsed_time = datetime.strptime(line_date, "%b %d %H:%M:%S")
            parsed_time = parsed_time.replace(year=datetime.now().year)
            return parsed_time
        except ValueError:
            logger.debug('Line doesnt have a valid time, skipping')
    return None


def is_old_time(time, delta_seconds):
    """ Check if time is greater than some delta, default 3 minutes """
    return (datetime.now() - time).total_seconds() > delta_seconds


def configure_logging(path="ethminer_supervisor.log", level=logging.INFO):
    logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=level,
            filename=path,
    )
