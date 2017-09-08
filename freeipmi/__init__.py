import os
import subprocess
import re


class IPMIError(Exception):
    pass


class FreeIPMI(object):
    def __init__(self, sensors_cli_path=None):
        """
        Construct a new 'FreeIPMI' object

        :param sensors_cli_path: path to ipmi-sensors executable
        :type sensors_cli_path: string
        :return: nothing
        """

        if sensors_cli_path:
            self.sensors_cli_path = sensors_cli_path

            if not os.path.exists(sensors_cli_path):
                raise RuntimeError('{0} not found'.format(sensors_cli_path))

        else:
            self.sensors_cli_path = 'ipmi-sensors'

    def _execute(self, cmd):
        """
        Execute a IPMI command

        :param cmd: command to execute
        :type cmd: string
        :return: command output
        :rtype: int
        """
        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if isinstance(out, bytes):
            out = out.decode()
        if isinstance(err, bytes):
            err = err.decode()

        if proc.returncode:
            ex = IPMIError(err.rstrip())
            ex.exitcode = proc.returncode
            raise ex
        else:
            return out

    def sensors(self):
        """
        Get all available IPMI sensors

        :return: IPMI sensors
        :rtype: list
        """

        header = None
        sensors = []

        raw = self._execute(
            cmd="{} -Q --sdr-cache-recreate".format(self.sensors_cli_path))
        for row in [re.sub('\s+\|\s+', '|', line).split('|') for line in filter(None, raw.rstrip().split("\n"))]:
            if header:
                sensor = {}
                for index, value in enumerate(row):
                    # try figuring out the value type
                    v = None

                    try:
                        v = int(value)
                    except ValueError:
                        try:
                            v = float(value)
                        except ValueError:
                            v = re.sub("['\"]$", '', re.sub(
                                "^['\"]", '', value))

                    sensor[header[index]] = v
                sensors.append(sensor)
            else:
                # the first line is the header
                header = [col.lower() for col in row]

        return sensors
