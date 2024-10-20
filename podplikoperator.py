import argparse
import sys
import random
import csv

def prepare_data():
    """Prepare model data and retrun dictionary containing is.

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

    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['Model', 'Wynik', 'Czas'], delimiter=';', lineterminator=';\r\n')
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

    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = next(reader)

        # DictReader does not allow us to specify custom line delimiter. This
        # leads to data containing an empty record being a result of semicolon
        # ending lines in specified file formatting, which must be removed.
        if '' in data.keys():
            del data['']

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

    parser = argparse.ArgumentParser(description="This script creates and reads files containing example data in subfolders according to a hierarchy: /month/day/time/.")

    parser.add_argument('-m', '--months', choices=months, nargs="+", metavar='MONTH', required=True,
                        help='list of months, for which files should be accessed')
    parser.add_argument('-d', '--days', choices=day_ranges, nargs="+", metavar='DAYS_RANGE', required=True,
                        help='list of weekday ranges `start`-`end`, for which files should be accessed. One for each month')
    parser.add_argument('-t', '--time', choices=('am', 'pm'), nargs="*", metavar='TIME',
                        help='list of times of day (am/pm), for which files should be accessed. One for each month-day combination (`am` if not specified)')

    operation = parser.add_argument_group('operation', 'select which operation you want to perform on files (these options are mutually exclusive)')
    excluseive_operation = operation.add_mutually_exclusive_group(required=True)
    excluseive_operation.add_argument('-r', '--read', action='store_true')
    excluseive_operation.add_argument('-w', '--write', action='store_true')

    file_type = parser.add_argument_group('file type', 'specify file extensions for which operatins should be performed')
    file_type.add_argument('-c', '--csv', action='store_true')
    file_type.add_argument('-j', '--json', action='store_true')

    args = parser.parse_args(sys.argv[1:])

    if not (args.csv or args.json):
        parser.error('no file type specified, add -c or -j')

    if len(args.months) != len(args.days):
        parser.error('the number of provided day ranges doesn\'t match the number of months')

    return args

if __name__ == "__main__":
    args = parse_arguments()
    print(args)