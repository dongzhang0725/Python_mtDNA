# BackTrans.py 

`Description:`Volume back translate AA sequences   

`【python 3.4.3】`

`Usage example:`

            1.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin F:\software\mafft\mafft-win\pro -NUCin C:\Users\Administrator\Desktop\nuc -s fast a -c 2   【for folder】
                        		
            2.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin pro -NUCin nuc -s paml -c 2   【for folder】
                        		
            3.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin test.aln -NUCin test.nuc -s clustal -c 2 -nogap -blockonly   【for file】

#convertfmt.py

`Description:`Convert fasta to selected format `【phylip|nexus|paml|axt】`

optional arguments:

              -h:       --help  show this help message and exit
              
              -f:       input fasta file
              
              -phy:     turn into phylip format
              
              -nex:     turn into nexus format
              
              -paml:    turn into paml format
              
              -axt:     turn into axt format
              
              -stat:    generate statistics of the fasta file
              
`【python 3.4.3】`

`Usage example:`

            1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
            
            2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat
            
#seq_matrix.py

`Description:` Concatenated muti-sequences into one file

`optional arguments:`

	-h	--help  show this help message and exit
	
	-f	FOLDER   input folder which include muti-sequences
	
	-phy	generate phylip format
	
	-nex	generate nexus format
	
	-paml	generate paml format
	
	-axt	generate axt format
	
	-fas	generate fasta file
	
	-stat	generate statistics file
	
	-part	generate partition file
	
`【python 3.4.3】`

The output file will be deposited in the dir of seq_matrix_out


`Usage example:`

	1.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -f C:\Users\Administrator\Desktop\scripts\partitions -phy

	2.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -phy -nex -paml -fas -axt -stat -part   【On condition that there is a 'partitions' folder in the directory of seq_matrix.py】

#refineGB.py

`usage:`      `refineGB.py [-h] -f FILE [-n NUM] -o OUT`

`Description:`Refine GenBank file to standard format.

optional arguments:

                  -h, --help  show this help message and exit
                  
                  -f FILE     input GenBank file or folder
                  
                  -n NUM      define minimum of the length of the NCR
                  
                  -o OUT      folder of the out file
  
`【python 3.4.3】`

`Usage example:`

        1.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\scripts\demo.gb -n 300 -o C:\Users\Desktop\myfolder
        
        2.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\gbfolder -o C:\Users\Desktop\myfolder
        
#alter_name.py

`usage:` `alter_name.py [-h] -f FILE [-o OUT]`

`Description:`Simplify default name of fasta file from NCBI

optional arguments:

                  -h, --help  show this help message and exit
                  
                  -f FILE     input fasta file
                  
                  -o OUT      out file name

`【python 3.4.3】`

`Usage example:`

      python C:\Users\Desktop\scripts\alter_name.py -f C:\Users\Desktop\demo.fasta -o C:\Users\Desktop\demo-out.fasta

