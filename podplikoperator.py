import argparse
import random
import csv
import json
from pathlib import Path

def prepare_data():
    """Prepare model data and return dictionary containing it.

    Returns:
        dict[str, str | int]: resulting model data
    """

    data = {}
    data['Model'] = random.choice(('A', 'B', 'C'))
    data['Wynik'] = random.randint(0, 1000)
    data['Czas'] = random.randint(0, 1000)
    return data

def csv_write(file_name, data):
    """Write data from dictionary to file in csv format.

    Args:
        file_name (string): name of file in which to record data
        data (dict): dictionary containing data in format {name : value}
    """

    with open(file_name, 'w', newline='', encoding="UTF8") as csv_file:
        writer = csv.DictWriter(csv_file, ['Model', 'Wynik', 'Czas'], delimiter=';', lineterminator='\r\n')
        writer.writeheader()
        writer.writerow(data)

def csv_read(file_name):
    """Read data from csv file to a dictionary.

    Args:
        file_name (string): name of file containing data with following formatting:
            name1;name2;name3;...;
            value1;value2;value3;...;

    Returns:
        dict: dictionary containing data from file
    """

    with open(file_name, 'r', newline='', encoding="UTF8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        data = next(reader)
        return data

def json_write(file_name, data):
    """Write data from dictionary to file in json format.

    Args:
        file_name (string): name of file in which to record data
        data (dict): dictionary containing data in format {name : value}
    """

    with open(file_name, 'w', newline='', encoding="UTF8") as json_file:
        json.dump(data, json_file)

def json_read(file_name):
    """Read data from json file to a dictionary.

    Args:
        file_name (string): name of file containing data with following formatting:
            {name1 : value1; name2 : value2; name3 : value3; ...}

    Returns:
        dict: dictionary containing data from file
    """

    with open(file_name, 'r', newline='', encoding="UTF8") as json_file:
        data = json.load(json_file)
        return data

def parse_arguments():
    months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
    day_ranges = ('mon', 'mon-tue', 'mon-wed', 'mon-thu', 'mon-fri', 'mon-sat', 'mon-sun',
                'tue', 'tue-wed', 'tue-thu', 'tue-fri', 'tue-sat', 'tue-sun',
                'wed', 'wed-thu', 'wed-fri', 'wed-sat', 'wed-sun',
                'thu', 'thu-fri', 'thu-sat', 'thu-sun',
                'fri', 'fri-sat', 'fri-sun',
                'sat', 'sat-sun',
                'sun',)

    parser = argparse.ArgumentParser(description="This script creates and reads files containing example data in sub-folders according to a hierarchy: /month/day/time/.")

    parser.add_argument('-m', '--months', choices=months, nargs="+", metavar='MONTH', required=True,
                        help='list of months, for which files should be accessed')
    parser.add_argument('-d', '--days', choices=day_ranges, nargs="+", metavar='DAYS_RANGE', required=True,
                        help='list of weekday ranges `start`-`end`, for which files should be accessed. One for each month')
    parser.add_argument('-t', '--time', choices=('am', 'pm'), nargs="*", metavar='TIME',
                        help='list of times of day (am/pm), for which files should be accessed. One for each month-day combination (`am` if not specified)')

    operation = parser.add_argument_group('operation', 'Select which operation you want to perform on files (these options are mutually exclusive).')
    exclusive_operation = operation.add_mutually_exclusive_group(required=True)
    exclusive_operation.add_argument('-r', '--read', action='store_true')
    exclusive_operation.add_argument('-w', '--write', action='store_true')

    file_type = parser.add_argument_group('file type', 'Specify file extensions for which operations should be performed.')
    file_type.add_argument('-c', '--csv', action='store_true')
    file_type.add_argument('-j', '--json', action='store_true')

    args = parser.parse_args()

    if not (args.csv or args.json):
        parser.error('no file type specified, add -c or -j')

    if len(args.months) != len(args.days):
        parser.error('the number of provided day ranges doesn\'t match the number of months')

    return args

def read(path, file_name):
    path = path / file_name
    if path.exists():
        if file_name[4:] == '.csv':
            data = csv_read(path)
        else:
            data = json_read(path)

        if data['Model'] == 'A':
            return int(data['Czas'])
    return 0

def write(path, file_name):
    path.mkdir(parents= True, exist_ok= True)
    if file_name[4:] == '.csv':
        csv_write(path / file_name, prepare_data())
    else:
        json_write(path / file_name, prepare_data())

def paths_constructor(args):
    # Returns a list containing tuples in format (month, day, time) to help reaching needed paths
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    time_counter = 0
    if args.time is None:
        times = []
    else:
        times = args.time
    paths = []

    for i, month in enumerate(args.months):
        d_range = []
        if len(args.days[i]) == 3:
            d_range.append(args.days[i])
        else:
            start = days.index(args.days[i][:3])
            end = days.index(args.days[i][4:])
            d_range = days[start:end + 1]

        for day in d_range:
            if time_counter < len(times):
                time = times[time_counter]
                time_counter += 1
            else:
                time = 'am'
            paths.append((month, day, time))

    return paths

def run(args):
    paths = paths_constructor(args)
    data = 0

    for p in paths:
        path = Path(f'{p[0]}/{p[1]}/{p[2]}')
        files = []
        if args.csv:
            files.append('Dane.csv')
        if args.json:
            files.append('Dane.json')

        if args.read:
            for file in files:
                data += read(path, file)
        else:
            for file in files:
                write(path, file)

    if args.read:
        print(f'Odczytany czas: {data}')

if __name__ == "__main__":
    args = parse_arguments()
    run(args)
