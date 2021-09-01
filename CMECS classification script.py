# CMECS classification script.py
# Geospatial analysis of deep-sea environments using ROV video data with the Coastal and Marine Ecological Classification Standard (CMECS).
# Creator: Jacob Freeman 
# Institution: Mississippi State University, Department of Geosciences

import csv, sys
import pdb

# The only potion of this script that should be modified are the paths specified in "file" and "outfile" below.
# The "file" path specifies the location of the .csv file containing downloaded SeaTube annotations that will be converted to CMECS compliant substrate units.
# The "outfile" path specifies the location of a new .csv file that will be created by this script and contain the converted CMECS substate unit annotations.

file = ('C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\Dive_annotation_files\\EX 1806\\Dive14old.csv')
outfile = ('C:\\Users\\Jakeb\\OneDrive\\Desktop\\Graduate Research- Desktop\\Dive_annotation_files\\EX 1806\\new\\Dive#14_new.csv')



with open(file, 'r') as csvfile:
	reader = csv.DictReader(csvfile)	
	
	with open(outfile, 'w') as csvoutfile:
		writer = csv.DictWriter(csvoutfile, lineterminator='\n', fieldnames = reader.fieldnames)
		writer.writeheader()
		
		for row in reader:
			try:
				# Grab substrate string.
				reclass = row['Substrate']
				#pdb.set_trace()
				# Find start index of "Primary" in string
				findstart = reclass.index('Primary')
				# Take from start of "Primary" through the end of the string
				reclass = reclass[findstart:len(reclass)]

				# Example: Primary Unconsolidated Secondary Unconsolidated

				# Split string into a list
				reclass_list = reclass.split(' ')
				
				#pdb.set_trace()
				
				# Find where "Primary" is in list
				pindex = reclass_list.index('Primary')
				# Grab next list value for primary classification
				primary = reclass_list[pindex + 1]

				# Find where "Secondary" is in list
				sindex = reclass_list.index('Secondary')
				# Grab next list value for secondary classification
				secondary = reclass_list[sindex + 1]
				
				# Eliminate any text after colon
				
				# Example: Unconsolidated:Sloping (5 to <30 Degrees)
				# [Unconsolidated, Sloping (5 to <30 Degrees)]
				# Take index of first and assign to secondary class variable

				secondary = secondary.split(':')[0]
				
				# Create empty string
				reclass_string = ""

				# Build primary portion of string
				primary = primary.lower()
				if primary == 'unconsolidated':
					reclass_string = reclass_string + 'Fine:'
				elif primary == 'rock':
					reclass_string = reclass_string + 'Rock:'
				elif primary == 'reef' or primary == 'rubble' or primary == 'hash':
					reclass_string = reclass_string + 'Coarse:'
				else:
					print ("Primary:unrecognized term")
					
				# Build secondary portion of string
				secondary = secondary.lower()
				if secondary == 'unconsolidated':
					reclass_string = reclass_string + 'Fine'
				elif secondary == 'rock':
					reclass_string = reclass_string + 'Rock'
				elif secondary == 'reef' or secondary == 'rubble' or secondary == 'hash':
					reclass_string = reclass_string + 'Coarse'
				else:
					print ("Secondary: unrecognized term")
				
				# Write new string back to row.
				row['Substrate'] = reclass_string
				writer.writerow(row)
			except:
				print ("Error in parsing annotation text.")
				print (reclass)
