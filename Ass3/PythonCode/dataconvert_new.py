import csv
import pandas as pd

input_Data_path = '../Ass3-DataFiles/'
output_Data_path = '../Ass3_new_DataOutputfiles/'

with open(input_Data_path + 'log.txt', "rb") as file_pipe:
    reader_pipe = csv.reader(file_pipe, delimiter='|')
    with open(output_Data_path + "MT.csv", 'wb') as file_comma:
        writer_comma = csv.writer(file_comma, delimiter=',')
        for row in reader_pipe:
            writer_comma.writerow(row)


df_csv = pd.read_csv(output_Data_path+ 'MT.csv', error_bad_lines=False)
for i, g in df_csv.groupby('sensorName'):
    print (g['value'])
    g.to_csv('../Ass3-DataOutputfiles/{}.csv'.format(i), index=False)


# cleaning and separating values for Accelerometer
df_csv = pd.read_csv(output_Data_path+ 'accelerometer-kx023.csv', index_col=[0])
df_csv['value'] = df_csv['value'].str.replace(']', '')
df_csv['value'] = df_csv['value'].str.replace('[', '')
df_csv[['x','y','z']] = df_csv.value.str.split(',', expand=True)
df_csv = df_csv.drop('value',axis = 1)
df_csv['timestamp'] = df_csv['timestamp']*1000000
df_csv['timestamp'] = df_csv['timestamp']+1435068000000
df_csv.to_csv(output_Data_path + 'final_new_accelerometer.csv')

# cleaning and separating values for Magnetometer
df_csv = pd.read_csv(output_Data_path+ 'mag-akm09918.csv',index_col=[0])
df_csv['value'] = df_csv['value'].str.replace(']', '')
df_csv['value'] = df_csv['value'].str.replace('[', '')
df_csv[['x','y','z']] = df_csv.value.str.split(',', expand=True)
df_csv = df_csv.drop('value',axis = 1)
df_csv['timestamp'] = df_csv['timestamp']*1000000
df_csv['timestamp'] = df_csv['timestamp']+1435068000000
df_csv.to_csv(output_Data_path + 'final_magnetometer.csv')

# cleaning and separating values for Gyroscope (Orientation for now)
df_csv = pd.read_csv(output_Data_path + 'orientation.csv', index_col=[0])
df_csv['value'] = df_csv['value'].str.replace(']', '')
df_csv['value'] = df_csv['value'].str.replace('[', '')
df_csv[['x','y','z']] = df_csv.value.str.split(',', expand=True)
df_csv = df_csv.drop('value',axis = 1)
df_csv['timestamp'] = df_csv['timestamp']*1000000
df_csv['timestamp'] = df_csv['timestamp']+1435068000000
df_csv.to_csv(output_Data_path + 'final_orientation.csv')

