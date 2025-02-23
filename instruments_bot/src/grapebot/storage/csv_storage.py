import csv
import logging

logger = logging.getLogger(__name__)


def store(path: str, data_fields: tuple, data: list):
    try:

        with open(path, "w+") as file:

            writer = csv.writer(file)
            writer.writerow(data_fields)

            for entry in data:
                writer.writerow([entry.get(field, 'nan') for field in data_fields])
    except Exception as exception:
        logger.error("failed storing data file: %s" % path, exception)
        raise exception


def load(path: str):
    fields = []
    data = []
    line_count = 0
    try:
        with open(path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if line_count == 0:
                    fields = row
                    line_count += 1
                    continue
                entry = {}
                for i in range(len(fields)):
                    entry[fields[i]] = row[i]
                line_count += 1
                data.append(entry)
        return data
    except Exception as exception:
        logger.error("failed loading data file: %s" % path, exception)
        raise exception
