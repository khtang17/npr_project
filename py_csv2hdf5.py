#! /usr/bin/python
from __future__ import print_function
import os
import h5py
import sys
import numpy



csv_file = open(sys.argv[1])
h5file = h5py.File("{}.hdf5".format(os.path.basename(sys.argv[1])), "w")

h5columns = h5file.create_group("data") # vaex reads all datasets in the columns group

# first count the lines, start at -1 since the first line is assumed to contain the column names
line_count = -1
for line in csv_file:
	line_count += 1

print("file contains ", line_count , " rows")

csv_file.seek(0) # start from the beginning of the file again
lines = iter(csv_file) # explicitly create an iterator over the lines

# first line should contain the column names

# header = lines.next()
header = next(lines)
print(type(header))
columns = header.strip().split(" ")
print("columns" ,columns)


Nbatch = 10000
h5_datasets = []
numpy_arrays = []
for column_name in columns:
	dataset = h5columns.create_dataset(column_name, (line_count, ), dtype='f8')
	h5_datasets.append(dataset)
	numpy_arrays.append(numpy.zeros((Nbatch, ), dtype='f8'))

row = 0
# we read in Nbatch lines at a time, and then write them out
for line in lines:
	# convert line to a series of float values
	try:
		values = map(float, line.split(" "))
		for i in range(len(columns)):
			#h5_datasets[i][row] = values[i]
			index = row-int(row/Nbatch)*Nbatch
			numpy_arrays[i][index] = values[i]
		if ((row % 10000) == 0) and row > 0:
			print("at " ,row ,  " of " ,line_count)
			# write out the array to disk
			for i in range(len(columns)):
				start = (int(row/Nbatch)-1)*Nbatch
				end = (int(row/Nbatch))*Nbatch
				h5_datasets[i][start:end] = numpy_arrays[i][:]
		row += 1
	except Exception as err:
		pass
	
if (row % 10000) > 0:
	print("writing out last part")
	for i in range(len(columns)):
		start = (int(row/Nbatch))*Nbatch
		end = line_count
		h5_datasets[i][start:end] = numpy_arrays[i][:end-start]

