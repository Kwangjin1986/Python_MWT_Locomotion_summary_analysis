#!/usr/bin/python

##Kwangjin Park 20150827
##Analyzing data obtained from Multi Worm Tracker
##python code for generating figures of worm bodyzise, bodylength and speed decay.  

##arguments:
#1. input_file = the file after you run Choreography (file is easy to read)
#2. out_file_table = after regular experession (table format and more readable)
#3. figure_directory = absolute directory path that you want save your all figures
#4. time_start = beggining experiment time you want to get data
#5. time_end = end experiment time you want to get data

## input at command line 
# python locomotion.py (input_file) (out_file_table) (figure_directory_path) 
# eg)  python locomotion.py merged.file newmerged.file "c:Desktop/bin/"


##--Future-- : you can set experiment times that you want get data
#python locomotion.py input_file out_file_table figure_directory_path time_start time_end
# eg)  python locomotion.py merged.file newmerged.file "c:Desktop/bin/" 530 590 

def main(): 
	
	##sys library is required for arguments 
	import sys
	import matplotlib.pyplot as plt
	import pandas as pd
	import numpy as np
	
	#read in command arguments
	input_file = sys.argv[1]
	out_file_table = sys.argv[2]
	figure_directory = sys.argv[3]
	#time_start = sys.argv[4]
	#time_end = sys.argv[5]
	
	##data regular expression
	ttable = regularexpression(input_file)

	## export revised table to newfile
	ttable.to_csv(out_file_table, sep='\t')
	
	##cut table from time_start - time_end
	modified_table = cuttable(ttable)
	#modified_table = cuttable(ttable, time_start, time_end) 
	
	#if you want to save this modified table, please run this command.
	#modified_table.to_csv("cuttable.file", sep='\t')
	
	
	#bodysize_Box_Figure
	plot_bodysize = bodysize_box(modified_table)
	plt.savefig(figure_directory+'/bodysize_box.png', bbox_inches='tight')
	
	#bodylength_Box_Figure
	plot_bodylength = bodylength_box(modified_table)
	plt.savefig(figure_directory+'/bodylength_box.png', bbox_inches='tight')
	#Figure_length
	#bodylength_bar(modified_table)
	#Figures_bodysize
	#bodysize_bar(modified_table)
	
	## make dataframe consisting of plate, strain, time, and speed
	st_dataframe = ttable[['PLATE', 'STRAIN', 'TIME', 'SPEED']]
	st_dataframe.columns = ['plate', 'strain', 'time', 'speed']
	st_dataframe.head(n=2)

	## call function that will eventually create a plot object for speed versus 
	## time. Currently it only successfully bins time and aggregates over speed.
	plot_speed = plot_speed_vs_time(st_dataframe)
	plt.savefig(figure_directory+'/speed_box.png', bbox_inches='tight')
	
# regularexpression function
def regularexpression(data):
	
	#import re and pandas(dataframe) library
	import re
	import pandas as pd
	
	## read a file as table
	datatable = pd.read_table(data, sep="\s+", names = ['v1', "FRAME", "ID", "PERSISTANCE", "AREA", "SPEED", "ANGULARSPEED", "LENGTH", "RELLENGTH", "WIDTH", "RELWIDTH", "ASPECT", "RELASPECT", "MIDLINE", "MORPHWIDTH", "KINK", "BIAS", "PATHLEN", "CURVE", "DIR", "loc_x", "loc_y", "vel_x", "vel_y", "ORIENT", "CRAB", "TAP", "PUFF", "STIM3", "STIM4"])
	
	
	## delete columns(v1, TAP, PUFF, STIM3, STIM4) from the table
	revised_datatable = datatable.drop(['v1',"TAP", "PUFF", "STIM3", "STIM4"], axis=1)
	
	## compile a regular expression pattern. It will speed up the ""findall"" function up to 100 times.
	## open a file as strings: This process is necessary for the ""regex.findall"" function.
	lines = []
	lines = open(data).read()
	
	comDATE = re.compile('./([0-9]{8})_')
	comPLATE = re.compile('./([0-9]{8}_[0-9]{6})/')
	comSTRAIN = re.compile('/([A-Za-z]+[-]?[0-9]+)')
	comTIME = re.compile(':([0-9]+[.][0-9]+)')
	Date = comDATE.findall(lines)
	Plate = comPLATE.findall(lines)
	Strain = comSTRAIN.findall(lines)
	Time = comTIME.findall(lines)
	table = {'DATE' : Date, 'PLATE' : Plate, 'TIME' : Time, 'STRAIN' : Strain}
	df = pd.DataFrame(table)
	df = df[['DATE', 'PLATE', 'TIME', 'STRAIN']]
	
	## To save memory, delete variables
	del lines
	del datatable
	
	## merge two tables to one table
	Newdata = pd.merge(df, revised_datatable, left_index=True, right_index=True, how='outer')
	return Newdata
	
	
def cuttable(info):
    
	import pandas as pd
	import numpy as np
	#newtable = pd.read_table(info, index_col=0)
	#a_newtable = newtable[newtable.TIME <= 590]
	info['TIME'] = info['TIME'].astype('float64')
	a_newtable = info[info.TIME <= 590]
	b_newtable = a_newtable[a_newtable.TIME >= 530]
	sort_table = b_newtable.sort(["STRAIN", "PLATE", "ID"])
	return sort_table
	
def bodysize_bar(dataset):
	import matplotlib.pyplot as plt
	import numpy as np
	
	sizetable = dataset.groupby('STRAIN')
	
	#plt.boxplot(sizetable['AREA'])
	sizevalue = sizetable['AREA'].aggregate(np.mean)
	std = sizetable['AREA'].aggregate(np.std)
	my_plot = sizevalue.plot(kind='bar', yerr=std, color='r')
	my_plot.set_xlabel('Strain')
	my_plot.set_ylabel('Body size (um)')
	return plt.savefig('Bodysize_bar.png', bbox_inches='tight')
	
def bodysize_box(dataSet):
	import matplotlib.pyplot as plt
	Sizetable = dataSet.boxplot(column = ['AREA'], by=['STRAIN'], showfliers=False, showmeans = True, return_type = 'axes')
	return Sizetable
	
	
def bodylength_bar(box):
	import matplotlib.pyplot as plt
	import numpy as np
	length_table = box.groupby('STRAIN')
	
	lengthvalue = length_table['LENGTH'].aggregate(np.mean)
	std = length_table['LENGTH'].aggregate(np.std)
	myplot = lengthvalue.plot(kind='bar', yerr=std )
	myplot.set_xlabel('Strain')
	myplot.set_ylabel('Body length (um)')
	return plt.savefig('length_bar.png', bbox_inches='tight')

def bodylength_box(Box):
	import matplotlib.pyplot as plt
	Lengthtable = Box.boxplot(column = ['LENGTH'],by = ['STRAIN'], showfliers=False, showmeans = True, return_type = 'axes')
	return Lengthtable

def floor_time_int(time_value):
    "Takes a time. Returns the a time bin."
    return ((time_value // 20) * 20)+10

def plot_speed_vs_time(dataframe):
    '''plot speed decay over time bin into time intervals to make it 
    quicker to plot (average speed over every 20s for 10 min)
    input: a dataframe consisting of plate, strain, time, and speed
    output: a plot object plotting time versus speed'''
    
    ## get rid of data from 0-40s of the experiment (sometimes the tracker 
    ## doesn't start tracking until 15s into the experiment)
    dataframe = dataframe[(dataframe['time']>=40) & (dataframe['time']<600)]
    
    ## call function floor_time_int() to replace continuous time 
    ## column with time binned into 20s intervals
    time = floor_time_int(dataframe['time'])
    dataframe.loc[:,('time')] = floor_time_int(dataframe['time'])
     
    ## plot time series
    my_speed_plot = dataframe.boxplot(column = ['speed'], by=['time', 'strain'], showfliers=False, showmeans = True, return_type = 'axes')
    
    ## return plot object
    return my_speed_plot

if __name__ == '__main__':
	
	main()		