## This is the driver script that will call modulars scripts to attack each chunk
## of the problem
##
## Set working directory to project's root directory
##
## Requires the following input from the user:
##		$1: gigabytes of memory to be used to run Choreography (dependent upon
##			the machine you are using
##		$2: path to  directory containing MWT experiment folders
##		$3: path to directory where data will be saved
##    	$4: control strain, which will be plotted first and used as a baseline for 
##      radarplot strain comparisons. 
##      NOTE: input is case-sensitive!

## Set amount of memory to be devoted to running Choreography
export MWT_JAVA_OPTIONS=-Xmx$1g

## call choreography to analyze the MWT data (each .zip in the folder data)
## error: Exactly one filename required
##  Use --help to list valid options.
for folder in $2/*/; do Chore --shadowless -p 0.027 -M 2 -t 20 -S -N all -o fDpesSlLwWaAmMkbPcdxyuvor1234 --plugin Reoutline::despike --plugin Respine --plugin MeasureReversal::all $folder; done

## need to create a large file containing all data files with 
## data, plate name and strain name in each row
##grep -r '[0-9]' $(find ./data -name '*.dat') > merged.file
for filename in $(find $2/. -name '*.dat'); do grep -H '[0-9]' $filename >> $2/merged.file; done

## Use regular expressions in R to parse apart the information in the filepath
## so we can get data, plate ID and strain as delimited columns
## call R script with the command line using an argument for the filename we want to parse
## After data is parsed, figures are plotted and stats are done and saved in results 
## directory
python bin/locomotion.py $2/merged.file $2/merged_parsed.file $3 
