import re
import os


class VehicleNumberLoader:

    PREFIX_PATTERM = re.compile(r'^[0-9]{2,3}:$')
    MISSING_PATTERN = re.compile(r'^[0-9]{2}$')
    ZERO_PATTERN = re.compile(r'^\*$')
    IMPROVEMENT_PATTERN = re.compile(r'^\[[0-9]{2}\]$')
    LARGER_OR_EQUAL_TO_PATTERN = re.compile(r'^\{[0-9]{2}\}$')
    SMALLER_THAN_PATTERN = re.compile(r'^\{.[0-9]{2}\}$')
    INTERVAL_PATTERN = re.compile(r'^[0-9]{2}\-[0-9]{2}$')

    def __init__(self):
        pass

    def load(self, only_missing=True, from_file=os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'vehicle', 'missing.txt'))):
        """
            Load the missing vehicle numbers and return a set that contains all vehicles that need to be captured.
        :param cmd_str:
        :param from_file:
        :return:
        """
        tracking_vehicles = set()
        with open(from_file, 'r') as missing_file:
            for line in missing_file.readlines():
                tracking_vehicles = tracking_vehicles.union(self.__process_file_line(line, only_missing=only_missing))
        return tracking_vehicles

    def __process_file_line(self, line, only_missing=True):
        line = line.strip()
        if not line or line.startswith('#'):
            return set()
        res = set()
        tokens = line.split()
        prefix = tokens[0]
        missings = tokens[1:]
        if not self.PREFIX_PATTERM.match(prefix):
            return res
        series = prefix[:-1]
        for missing in missings:
            if self.MISSING_PATTERN.match(missing):
                res.add(series + missing)
            elif self.ZERO_PATTERN.match(missing):
                res.add(series + '00')
            elif self.LARGER_OR_EQUAL_TO_PATTERN.match(missing):
                res.union([series + ('0' if suffix < 10 else '') + str(suffix) for suffix in range(int(missing[1:3]), 100)])
            elif self.SMALLER_THAN_PATTERN.match(missing):
                res.union([series + ('0' if suffix < 10 else '') + str(suffix) for suffix in range(0, int(missing[2:4]) + 1)])
            elif self.INTERVAL_PATTERN.match(missing):
                res.union([series + ('0' if suffix < 10 else '') + str(suffix) for suffix in range(
                    int(missing[:2]), int(missing[3:]) + 1
                )])
            elif not only_missing and self.IMPROVEMENT_PATTERN.match(missing):
                res.add(series + missing[1:3])
        return res
