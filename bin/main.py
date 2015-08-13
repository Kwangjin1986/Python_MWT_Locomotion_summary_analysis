def main(): 
	
	##sys library is required for arguments 
	import sys
	import matplotlib.pyplot as plt
	
	##data regular expression
	datatable = regularexpression(sys.argv[1])

	## export revised table to newfile
	datatable.to_csv("newmerged.file", sep='\t')
	
	#Figures
	#bodysizeA(datatable)
	#bodysizeB(datatable)
	#plt.show()

	
# regularexpression function
def regularexpression(data):
	
	## If file size is small, it is ok to use *re* library.
	## *regex* is a faster regular expression library than *re* library.
	## To use regex library, download and install the library. 
	import regex
	
	##pandas is dataframe library
	import pandas as pd
	
	## read a file as table
	gDat = pd.read_table(data, sep="\s+", names = ['v1',"date", "plate", "time", "strain", "frame", "ID", "persistance", "area", "speed", "angularspeed", "length", "rellength", "width", "relwidth", "aspect", "relaspect", "midline", "morphwidth", "kink", "bias", "pathlen", "curve", "dir", "loc_x", "loc_y", "vel_x", "vel_y", "orient", "crab"])
	
	
	## delete column(v1) from the table
	newgDat = gDat.drop('v1', axis=1)
	
	## compile a regular expression pattern. It will speed up the ""findall"" function up to 100 times.
	## open a file as strings: This process is necessary for the ""regex.findall"" function.
	lines = []
	lines = open(data).read()
	
	PA = regex.compile('./([0-9]{8})_')
	PB = regex.compile('./([0-9]{8}_[0-9]{6})/')
	PC = regex.compile('/([A-Za-z]+[-]?[0-9]+)')
	N = regex.compile(':([0-9]+[.][0-9]+)')
	Date = PA.findall(lines)
	Plate = PB.findall(lines)
	Strain = PC.findall(lines)
	Time = N.findall(lines)
	table = {'DATE' : Date, 'PLATE' : Plate, 'TIME' : Time, 'STRAIN' : Strain}
	df = pd.DataFrame(table)
	df = df[['DATE', 'PLATE', 'TIME', 'STRAIN']]
	
	## To save memory and avoid to recall recent data
	del lines
	del gDat
	
	## merge two tables to one table
	Newdata = pd.merge(df, newgDat, left_index=True, right_index=True, how='outer')
	return Newdata
	
def bodysizeA(table):
	import matplotlib.pyplot as plt
	import numpy as np
	sizetable = table.groupby('STRAIN')
	
	#plt.boxplot(sizetable['AREA'])
	sizevalue = sizetable['AREA'].aggregate(np.mean)
	std = sizetable['AREA'].aggregate(np.std)
	my_plot = sizevalue.plot(kind='bar', yerr=std, color='r')
	my_plot.set_xlabel('Strain')
	my_plot.set_ylabel('Body size (um)')
	return my_plot
	
def bodysizeB(box):
	#import matplotlib.pyplot as plt
	sizetable = box.groupby('STRAIN')
	myplot = sizetable.boxplot(column = 'AREA', showfliers=False, showmeans = True, return_type = 'axes')
	return myplot
	

if __name__ == '__main__':
	
	main()		