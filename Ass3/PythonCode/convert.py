import csv
import datetime

data_path = '../Ass3_Inputfiles/'

def _format_timestamp(timestamp_string):
    # Seconds since epoch: 1560795566 -> 10 digits
    # SensorLog produces milliseconds since epoch: 1562724303708 -> 13 digits
    # CrowdSignals expects nanoseconds since epoch: 1454956105993627709 -> 19 digits
    d = datetime.datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S.%f").strftime('%s.%f')
    d_in_ms = int(float(d) * 1000) * 1000000

    return d_in_ms

def _timestamp_as_float(timestamp_string):
    d = datetime.datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S.%f").strftime('%s.%f')
    return float(d)

def _to_datetime(datetimestring):
    return datetime.datetime.strptime(datetimestring, "%Y-%m-%d %H:%M:%S.%f")

def tweak_times(file_name):
    rows = []

    file_handle = open(data_path+'data_new_fixed.csv', 'wb')
    writer = csv.writer(file_handle, delimiter=',')

    with open(file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        headers = next(reader, None)[0].split(',')  # skip the headers when reading the SensorLog file

        rows.append(headers)

        for reading in reader:
            reading = reading[0].split(',')
            ts = reading[0][0:-6]
            ts_datetime = _to_datetime(ts)

            if len(str(ts_datetime)) < 26:
                ts_datetime_str = str(ts_datetime) + '.000000'
            else:
                ts_datetime_str = str(ts_datetime)

            rows.append([_format_timestamp(ts_datetime_str)] + reading[1:])

            # start = datetime.datetime(2019, 06, 21, 11, 30, 46, 797000)
            #
            # if ts_datetime >= start:
            #     current = datetime.datetime.fromtimestamp(_timestamp_as_float(ts))
            #     previous = current - datetime.timedelta(minutes=17)
            #
            #     if len(str(previous)) < 26:
            #         previous = str(previous) + '.000000'
            #
            #     rows.append([previous] + reading[1:])

    writer.writerows(rows)
    file_handle.close()

tweak_times(data_path+'my_iOS_data.csv')