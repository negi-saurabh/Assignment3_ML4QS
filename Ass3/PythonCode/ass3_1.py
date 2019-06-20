###############################################################
#                                                             #
#  Chapter 2 coding exercise.                                 #
#  Sdapted from Mark Hoogendoorn's                            #
#  crowdsignals_ch2.py                                        #
#                                                             #
###############################################################

from __future__ import print_function
from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
from util import util
import copy
import os
import glob
import pandas as pd
import time

dataset_path = '../Ass3_processed_datafiles/'
result_dataset_path = './Ass3inter_files/'

if not os.path.exists(result_dataset_path):
    print('Creating result directory: ' + result_dataset_path)
    os.makedirs(result_dataset_path)

datasets = []

# Convert seconds with unknown start to epoch value with arbitrary start
def convert_seconds_to_epoch(sec):
    epoch_offset = int(time.mktime(time.strptime('08.06.2018 12:00:00', '%d.%m.%Y %H:%M:%S')))
    return (epoch_offset * 1000000000 + int(round(float(sec) * 1000000000)))  # *billion for sec -> nanosec

# Read all files csv files, convert time (s) to epoch timestamp, delete old csv and write new matrix to csv
def reformat_csv_files(dataset_path):
    allFiles = glob.glob(dataset_path + "/*.csv")

    for filename in allFiles:
    # Just skip files without 'Time (s)' column
        try:
            df = pd.read_csv(filename, sep=',', index_col=None, header=0)
            timestamps = [convert_seconds_to_epoch(val) for val in df['Time (s)']]
            df.insert(0, 'timestamps', timestamps)
            df = df.drop('Time (s)', axis=1)
            os.remove(filename)
            df.to_csv(filename, sep=',', index=False)
        # Only skip if it's the 'Time (s)' column that's missing
        except KeyError as error:
            if error.args[0] != "Time (s)":
                raise error

#=====
# MAIN
#=====
if __name__ == "__main__":
    # Reformat csv files so that Mark's code works on them (time in s to epoch time in ms)
    #reformat_csv_files(dataset_path)

    # Granularity in milliseconds
    dt = 250

    # # Load csv data into DataSet
    DataSet = CreateDataset(dataset_path, dt)
    DataSet.add_numerical_dataset('final_accelerometer.csv', 'timestamp', ['x','y','z'], 'avg', 'acc_')
    DataSet.add_numerical_dataset('final_orientation.csv', 'timestamp', ['x', 'y', 'z'], 'avg', 'ori_')
    DataSet.add_numerical_dataset('final_magnetometer.csv', 'timestamp', ['x', 'y', 'z'], 'avg', 'mag_')
    DataSet.add_event_dataset('labels.csv', 'label_start', 'label_end', 'label', 'binary')
    #DataSet.add_numerical_dataset('gyro_act.csv', 'timestamps', ['x', 'y', 'z'], 'avg', 'gyr_')
    #DataSet.add_numerical_dataset('inclination_act.csv', 'timestamps', ['ang', 'rot'], 'avg', 'inc_')
    #DataSet.add_numerical_dataset('Light.csv', 'timestamps', ['lx'], 'avg', 'light_')
    #DataSet.add_numerical_dataset('gps_act.csv', 'timestamps', ['Lat', 'Long', 'Height', 'Veloc', 'Dir', 'Hor_acc',
                                                                 #'Ver_acc'], 'avg', 'loc_')

    # Get the resulting pandas data table
    dataset = DataSet.data_table

    print(dataset)

    # Plot the data
    DataViz = VisualizeDataset()

    # Boxplot
    DataViz.plot_dataset_boxplot(dataset, ['acc_x', 'acc_y', 'acc_z'])

    # Plot all data
    DataViz.plot_dataset(dataset, ['acc_', 'ori_', 'mag_', 'label'],
                         ['like', 'like', 'like','like'],
                         ['line', 'line', 'line', 'points'])

    # And print a summary of the dataset
    util.print_statistics(dataset)
    datasets.append(copy.deepcopy(dataset))

    #datasets.append(copy.deepcopy(dataset))

    # Just passing single dataset twice to Mark's function that prints two datasets
    util.print_latex_table_statistics_two_datasets(dataset, dataset)

    dataset.to_csv(result_dataset_path + 'Ass3_chapter2_result.csv')
