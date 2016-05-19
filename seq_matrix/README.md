#seq_matrix.py

`Description:` Concatenated muti-sequences into one file

`optional arguments:`

	-h	--help  show this help message and exit
	
	-f	FOLDER   input folder
	
	-phy	generate phylip format
	
	-nex	generate nexus format
	
	-paml	generate paml format
	
	-axt	generate axt format
	
	-fas	generate fasta file
	
	-stat	generate statistics file
	
	-part	generate partition file

`【python 3.4.3】`

The output file will be deposited in the directory of seq_matrix.py

`Usage example:`

	1.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -f C:\Users\Administrator\Desktop\scripts\partitions -phy

	2.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -phy -nex -paml -fas -axt -stat -part   【On condition that there is a 'partitions' folder in the directory of seq_matrix.py】
