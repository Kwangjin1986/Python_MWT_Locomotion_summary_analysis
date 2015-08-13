def main(): 
	
	##sys library is required for arguments 
	import sys
	import matplotlib.pyplot as plt
	
	##data regular expression
	ttable = regularexpression(sys.argv[1])

	## export revised table to newfile
	#ttable.to_csv("newmerged.file", sep='\t')
	
	##cut table from 530 - 590
	modified_table = cuttable(ttable)
	#modified_table.to_csv("cuttable.file", sep='\t')
	
	#Figures_bodysize
	#bodysize_bar(modified_table)
	bodysize_box(modified_table)
	
	#Figure_length
	#bodylength_bar(modified_table)
	bodylength_box(modified_table)
	
	

	
# regularexpression function
def regularexpression(data):
	
	
	import re
	
	##pandas is dataframe library
	import pandas as pd
	
	## read a file as table
	datatable = pd.read_table(data, sep="\s+", names = ['v1', "FRAME", "ID", "PERSISTANCE", "AREA", "SPEED", "ANGULARSPEED", "LENGTH", "RELLENGTH", "WIDTH", "RELWIDTH", "ASPECT", "RELASPECT", "MIDLINE", "MORPHWIDTH", "KINK", "BIAS", "PATHLEN", "CURVE", "DIR", "loc_x", "loc_y", "vel_x", "vel_y", "ORIENT", "CRAB", "TAP", "PUFF", "STIM3", "STIM4"])
	
	
	## delete column(v1) from the table
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
	
	## To save memory
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
	Sizetable = dataSet.groupby('STRAIN')
	Sizetable.boxplot(column = 'AREA', showfliers=False, showmeans = True, return_type = 'axes')
	return plt.savefig('Bodisize_boxplot.png', bbox_inches='tight')
	
	
def bodylength_bar(box):
	#import matplotlib.pyplot as plt
	import matplotlib.pyplot as plt
	import numpy as np
	length_table = box.groupby('STRAIN')
	
	#plt.boxplot(sizetable['AREA'])
	lengthvalue = length_table['LENGTH'].aggregate(np.mean)
	std = length_table['LENGTH'].aggregate(np.std)
	myplot = lengthvalue.plot(kind='bar', yerr=std )
	myplot.set_xlabel('Strain')
	myplot.set_ylabel('Body length (um)')
	return plt.savefig('length_bar.png', bbox_inches='tight')

def bodylength_box(Box):
	import matplotlib.pyplot as plt
	Length_table = Box.groupby('STRAIN')
	Length_table.boxplot(column = 'LENGTH', showfliers=False, showmeans = True, return_type = 'axes')
	return plt.savefig('length_boxplot.png', bbox_inches='tight')

if __name__ == '__main__':
	
	main()		