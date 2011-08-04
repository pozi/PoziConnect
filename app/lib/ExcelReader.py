import pyodbc

def XLSread(options,self):
	# Historic values to phase out
	# Parameters
	sheet_filename = ur'C:\Tools\Councils\Buloke\batch\fromExcel\data\St-Data2.xls'
	sheet_name = u"MASTER SHEET"
	sheet_first_line=22
	reference_col='A'
	columns_to_extract=['A',   'B',     'C',      'D',      'E',    'F',    'G',   'EG',    'EH', 'EI',   'EJ',             'EK',  'EL',   'EM',   'EO','EP','EQ','ER',  'ES',         'ET',       'EX',    'FU',          'GS',  'GU',       'GV',            'GY']
	column_headers=     "SegId;RoadName;From_Desc;From_Dist;To_Desc;To_Dist;Length;CodeType;Width;AddSubt;ProgressCondition;OACond;ImmFail;PotFail;Rug;Rut;Pro;MtceGrade;ExisPaveDepth;PaveMatCode;PaveArea;SealedProgCond;GPSRef;RuralOrTown;SealedOrUnsealed;RoadStatus"
	csv_filename = ur'C:\Tools\PlaceLab-code\tasks\Excel\moloney_roads.csv'

	# Extract the parameters values from the options parameter, configured in the PlaceLab task
	sheet_filename = str(options.get('source'))
	sheet_name = str(options.get('sheetname'))
	sheet_first_line = int(options.get('sheetfirstline'))
	reference_col = str(options.get('referencecolumn'))
	columns_to_extract_string = options.get('columnstoextract')
	columns_to_extract = str(columns_to_extract_string).split(',')
	column_headers = str(options.get('columnheaders'))
	csv_filename = str(options.get('csvfilename'))

	print "#"*60
	print "Excel reader options: ", options

	# Local constants
	csv_separator=";"
	csv_endline="\n"
	# Excel line number limit
	tentative_last_line = 65536

	#cnxn = pyodbc.connect(u'Driver={Microsoft Excel Driver (*.xls)};FIRSTROWHASNAMES=0;READONLY=TRUE;DBQ=%s' % (sheet_filename), autocommit=True)
	try:
		cnxn = pyodbc.connect(u'Driver={Microsoft Excel Driver (*.xls)};READONLY=TRUE;DBQ=%s' % (sheet_filename), autocommit=True)
		cursor = cnxn.cursor()

		# Extraction of the whole reference column
		cursor.execute("select * from ["+sheet_name+"$"+reference_col+str(sheet_first_line)+":"+reference_col+str(tentative_last_line)+"]")
		rows_all = cursor.fetchall()

		# Determining line number by scanning the first null cell in the reference column
		line_number=0
		for row in rows_all:
			if str(row[0])=="" or str(row[0])=="None" or len(str(row[0]))==0:
				break
			else:
				line_number = line_number+1
			#print str(line_number)+str(row[0])

		sheet_last_line=sheet_first_line+line_number
		print "Number of lines extracted:"+str(line_number)

		# Open CSV file for writing
		csv_file = open(csv_filename, "w")
		col_index = 1

		for col in columns_to_extract:

			# Open the CSV file for reading and read all the lines in the l variable
			csv_file_ro = open(csv_filename, "r")
			l = csv_file_ro.readlines()
			# Close the file and delete the handler
			csv_file_ro.close()
			del csv_file_ro

			# Read the Excel document
			cursor.execute("select * from ["+sheet_name+"$"+col+str(sheet_first_line)+":"+col+str(sheet_last_line)+"]")
			rows = cursor.fetchall()

			# Loop throught all the rows in the Excel document
			row_index = 0
			for row in rows:
				# Extract the previous content of the CSV file for this line
				l_item=l[row_index].rstrip() if len(l)>row_index else ""
				# For the first column, do not add the CSV separator
				if col_index==1:
					csv_separator_mod = ""
				else:
					csv_separator_mod = csv_separator
				# If field is None, transform that as the empty string
				if str(row[0])=='None':
					col_content=""
				else:
					col_content=str(row[0]).replace(";"," ").replace(","," ")
				# Write the previous line + ; + Excel cell content + \n to build the new line
				csv_file.write(l_item+csv_separator_mod+col_content+csv_endline)

				# Increment the row index
				row_index = row_index + 1

			# Go back at the beginning of the file
			csv_file.seek(0)

			# Increment the column index	
			col_index=col_index+1

		# Close the Excel file cursor and connexion handler
		cursor.close()
		cnxn.close()

		# Write the headers
		csv_file_ro = open(csv_filename, "r")
		l = csv_file_ro.readlines()
		# Close the file and delete the handler
		csv_file_ro.close()
		del csv_file_ro

		csv_file.seek(0)
		csv_file.write(column_headers)
		csv_file.write("\n")
		csv_file.write("".join(l))

		csv_file.close()
		del csv_file

	except Exception as e:
		self.logger.error("#" * 60 + "\nERROR: The Excel spreadsheet can not be read - is it already opened by someone else? \nDetails:"+str(e)+"\nThe task will continue but this error should be investigated.\n")
