##############################################################
#                                                            #
#  Song Yang                                                 #
#  Chapter 3                                                 #
#  Largely adapted from Mark Hoogendoorn's                   #
#                                                            #
##############################################################

from util.VisualizeDataset import VisualizeDataset
from Chapter3.OutlierDetection import DistributionBasedOutlierDetection
from Chapter3.OutlierDetection import DistanceBasedOutlierDetection
import copy
import pandas as pd
import numpy as np
from matplotlib import pyplot

# Let is create our visualization class again.
DataViz = VisualizeDataset()

# Read the result from the previous chapter, and make sture the index is of the type datetime.
dataset_path = '../Ass3_processed_outputfiles/'
try:
    dataset = pd.read_csv(dataset_path + 'initial_result.csv', index_col=0)
except IOError as e:
    print('File not found, try to run previous crowdsignals scripts first!')
    raise e

dataset.index = dataset.index.to_datetime()

y1 = np.var(dataset, axis=0)[0]
y2 = np.var(dataset, axis=0)[1]
y3 = np.var(dataset, axis=0)[2]
y4 = np.var(dataset, axis=0)[3]
y5 = np.var(dataset, axis=0)[4]
y6 = np.var(dataset, axis=0)[5]
y7 = np.var(dataset, axis=0)[6]
y8 = np.var(dataset, axis=0)[7]
y9 = np.var(dataset, axis=0)[8]

# print(int(y1))
# print(int(y2))
# print(int(y3))
# print(int(y4))
# print(int(y5))
# print(int(y6))
# print(int(y7))
# print(int(y8))
# print(int(y9))

# Compute the number of milliseconds covered by an instance based on the first two rows
milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000

# Step 1: Let us see whether we have some outliers we would prefer to remove.

# Determine the columns we want to experiment on.
outlier_columns = ['mag_phone_x','mag_phone_x','mag_phone_z']

#for chauvenet
# pyplot.hist(dataset['acc_x'].dropna(), alpha=0.4, color='blue', label='acc_x' )
# pyplot.hist(dataset['acc_y'].dropna(), alpha=0.8, color='green', label='acc_y' )
# pyplot.hist(dataset['acc_z'].dropna(), alpha=0.7, color='blue', label='acc_z' )
# pyplot.hist(dataset['ori_x'].dropna(), alpha=0.6, color='blue', label='ori_x' )
# pyplot.hist(dataset['ori_y'].dropna(), alpha=0.3, color='blue', label='ori_y' )
# pyplot.hist(dataset['ori_z'].dropna(), alpha=0.4, color='blue', label='ori_z' )
pyplot.hist(dataset['mag_phone_x'].dropna(), alpha=0.9, color='blue', label='mag_x' )
pyplot.hist(dataset['mag_phone_y'].dropna(), alpha=0.9, color='blue', label='mag_y' )
pyplot.hist(dataset['mag_phone_z'].dropna(), alpha=0.9, color='blue', label='mag_z' )


#for local outlier

# pyplot.scatter(x, y, s=area, c=colors, alpha=0.5)

# Create the outlier classes.
OutlierDistr = DistributionBasedOutlierDetection()
OutlierDist = DistanceBasedOutlierDetection()

#And investigate the approaches for all relevant attributes.
for col in outlier_columns:
    # And try out all different approaches. Note that we have done some optimization
    # of the parameter values for each of the approaches by visual inspection.
    # dataset = OutlierDistr.chauvenet(dataset, col)
    # DataViz.plot_binary_outliers(dataset, col, col + '_outlier')
    # dataset = OutlierDistr.mixture_model(dataset, col)
    # DataViz.plot_dataset(dataset, [col, col + '_mixture'], ['exact','exact'], ['line', 'points'])
    # This requires:
    # n_data_points * n_data_points * point_size =
    # 31839 * 31839 * 64 bits = ~8GB available memory
    try:
        dataset = OutlierDist.simple_distance_based(dataset, [col], 'euclidean', 0.10, 0.99)
        DataViz.plot_binary_outliers(dataset, col, 'simple_dist_outlier')
    except MemoryError as e:
        print('Not enough memory available for simple distance-based outlier detection...')
        print('Skipping.')
    
    try:
        dataset = OutlierDist.local_outlier_factor(dataset, [col], 'euclidean', 5)
        DataViz.plot_dataset(dataset, [col, 'lof'], ['exact','exact'], ['line', 'points'])
    except MemoryError as e:
        print('Not enough memory available for lof...')
        print('Skipping.')

    # Remove all the stuff from the dataset again.
    cols_to_remove = [col + '_outlier', col + '_mixture', 'simple_dist_outlier', 'lof']
    for to_remove in cols_to_remove:
        if to_remove in dataset:
            del dataset[to_remove]

# We take Chauvent's criterion and apply it to all but the label data...

for col in [c for c in dataset.columns if not 'label' in c]:
    print 'Measurement is now: ' , col
    dataset = OutlierDistr.chauvenet(dataset, col)
    dataset.loc[dataset[col + '_outlier'] == True, col] = np.nan
    del dataset[col + '_outlier']

dataset.to_csv(dataset_path + 'Ass3_result_outliers.csv')
