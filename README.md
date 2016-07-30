#gb_parser.py
【python 3.4.3】  【python 3.4.3】 [**biopython**][hover] must be enabled 
[hover]:http://biopython.org/wiki/Download "download biopython"

**usage:** `gb_parser.py [-h] [-f FILE] [-n {14,15}] [-r REPLACE] [-t {1,2,3,4}] [-c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}] [-e EXCLUDE] [-p PREFER] [-aa] [-nuc] [-rRNA] [-tRNA] [-geom] [-table] [-order] [-name] [-stat] [-csv]`

**Description:** Parse GenBank file to extract interested information

**optional arguments:**

                    -h, --help            show this help message and exit
                    
                    -f FILE               input GenBank file
                    
                    -n {14,15}            the amount of the protein plus rRNA genes among mtDNA
                    
                    -r REPLACE            the replace file with unified gene names involved in
                    
                    -t {1,2,3,4}          **** choose a type of the header of the fasta file **** 
                                         【1】by latin,     for instance:>Benedenia_hoshinai (default) 
                                         【2】by Genbank,   for instance:>NC_014591 
                                         【3】by logogram,  for instance:>B_hoshinai 
                                         【4】by latin_gb,  for instance:>Benedenia_hoshinai_NC_014591
                                         
                    -c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}
                    
                                          choose a codon table!【1(default)|2|3|4|5|6|9|10|11|12|13|14|15|16|21|22|23】
                                          NCBI GenBank codon table
                                          1 Universal code 
                                          2 Vertebrate mitochondrial code 
                                          3 Yeast mitochondrial code 
                                          4 Mold, Protozoan, and Coelenterate Mitochondrial code and Mycoplasma/Spiroplasma code
                                          5 Invertebrate mitochondrial 
                                          6 Ciliate, Dasycladacean and Hexamita nuclear code 
                                          9 Echinoderm and Flatworm mitochondrial code
                                          10 Euplotid nuclear code 
                                          11 Bacterial, archaeal and plant plastid code 
                                          12 Alternative yeast nuclear code 
                                          13 Ascidian mitochondrial code 
                                          14 Alternative flatworm mitochondrial code 15 Blepharisma nuclear code 
                                          16 Chlorophycean mitochondrial code 
                                          21 Trematode mitochondrial code 
                                          22 Scenedesmus obliquus mitochondrial code 
                                          23 Thraustochytrium mitochondrial code
                                          
                    -e EXCLUDE            the gb number of the excluded species
                    
                    -p PREFER             the gb number of the species that we prefer to its genome statistics
                    
                    -aa                   generate AA sequence files (fasta) of individual PCGs
                    
                    -nuc                  generate nucleotide sequence files (fasta) of individual PCGs
                    
                    -rRNA                 generate nucleotide sequence files (fasta) of individual rRNAs
                    
                    -tRNA                 generate nucleotide sequence files (fasta) of individual tRNAs
                    
                    -geom                 generate nucleotide sequence files (fasta) of the whole genome
                    
                    -table                generate statistics file of the whole genome and individual genes
                    
                    -order                generate a file with mt genes order involved in
                    
                    -name                 generate a file of detailed name so as to edit phylogenetic tree by iTOl
                    
                    -stat                 generate statistics file about the inclusive species of individual genes
                    
                    -csv                  generate csv files about the nucleotide sequence of PCGs, rRNAs and tRNAs


**Usage example:**

    You can omit '-f' and '-r' under the premise of a GenBank file named 'sequences.gb' and a replace file named 'replace.txt' are placed in the dir of the scripts:
    
        【muti-prefer species】 python D:\parseGB\bin\gb_parser.py -c 9 -p NC_030050 NC_016950 JQ038228 -aa -nuc -rRNA -tRNA -geom -table -order -name -stat -csv
        
        【muti-excluded species】python D:\parseGB\bin\gb_parser.py -c 9 -e NC_030050 NC_016950 JQ038228 -aa -nuc -rRNA -tRNA -geom -table -order -name -stat -csv
    
    Specify GenBank file and replace file:
    
        【only output AA sequence】 python D:\parseGB\bin\gb_parser.py -c 9 -f C:\users\sequences.gb -r C:\users\replace.txt -aa
        
        【specify the number of PCGs plus rRNAs】 python D:\parseGB\bin\gb_parser.py -c 9 -n 15 -f C:\users\sequences.gb -r C:\users\replace.txt -aa -nuc
        
        【specify type of the species name】 python D:\parseGB\bin\gb_parser.py -c 9 -t 2 -f C:\users\sequences.gb -r C:\users\replace.txt -table -order
       
        【use default codon table(1)】  python D:\parseGB\bin\gb_parser.py -t 2 -f C:\users\sequences.gb -r C:\users\replace.txt -table -order

---
#mafft_plus.py

【python 3.4.3】 [**biopython**][hover] must be enabled 
[hover]:http://biopython.org/wiki/Download "download biopython"

**usage:** `mafft_plus.py [-h] [-f FILE] [-table {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}] [-mafft MAFFT] [-codon]`

**Description:** Add codon alignment and batch run to mafft

**optional arguments:**

					-h, --help            show this help message and exit

					-f FILE               input fasta file or folder

					-table {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}

									  choose a codon table!【1(default)|2|3|4|5|6|9|10|11|12|13|14|15|16|21|22|23】
									  NCBI GenBank codon table
									  1 Universal code 
									  2 Vertebrate mitochondrial code 
									  3 Yeast mitochondrial code 
									  4 Mold, Protozoan, and Coelenterate Mitochondrial code and Mycoplasma/Spiroplasma code
									  5 Invertebrate mitochondrial 
									  6 Ciliate, Dasycladacean and Hexamita nuclear code 
									  9 Echinoderm and Flatworm mitochondrial code
									  10 Euplotid nuclear code 
									  11 Bacterial, archaeal and plant plastid code 
									  12 Alternative yeast nuclear code 
									  13 Ascidian mitochondrial code 
									  14 Alternative flatworm mitochondrial code 15 Blepharisma nuclear code 
									  16 Chlorophycean mitochondrial code 
									  21 Trematode mitochondrial code 
									  22 Scenedesmus obliquus mitochondrial code 
									  23 Thraustochytrium mitochondrial code
									  
					-mafft           	  the path of the mafft
					
					-codon                Boolean, whether codon alignment or not

**Usage example:**

*Normal align (the output file will be deposited in the mafft_out folder of scripts directionary):*

    【single file】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta
	
    【input folder】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align

*Codon align (the output file will be deposited in the codon_alignments folder of scripts directionary):*

    【single file】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta -table 1 -mafft C:\Users\Desktop\mafft.bat -codon
	
    【input folder】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align -table 1 -mafft C:\Users\Desktop\mafft.bat -codon

---
#seq_matrix.py

**Description:** Concatenated muti-sequences into one file

**optional arguments:**

	-h	--help  show this help message and exit
	
	-f	FOLDER   input folder which include muti-sequences
	
	-phy	generate phylip format
	
	-nex	generate nexus format
	
	-nex2   generate interleave nexus format
	
	-nex3   generate interleave nexus format delimited by genes, so as to run Best
	
	-paml	generate paml format
	
	-axt	generate axt format
	
	-fas	generate fasta file
	
	-stat	generate statistics file
	
	-part	generate partition file

【python 3.4.3】

`The output file will be deposited in the dir of seq_matrix_out`

**Usage example:**

	1.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -f C:\Users\Administrator\Desktop\scripts\partitions -phy

	2.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -phy -nex -paml -fas -axt -stat -part   【On condition that there is a 'partitions' folder in the directory of seq_matrix.py】

---
#convertfmt.py

**Description:** Convert fasta file to selected format `【phylip|nexus|paml|axt】`

**optional arguments:**

              -h:       --help  show this help message and exit
              
              -f:       input fasta file or folder
              
              -phy:     convert into phylip format
              
              -nex:     convert into nexus format
              
              -paml:    convert into paml format
              
              -axt:     convert into axt format
              
              -stat:    generate statistics of the fasta file
              
              -out      folder of the out files

【python 3.4.3】

**Usage example:**

            1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
            
            2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat
            
            3.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\fas-folder -nex

---
# BackTrans.py 

**Description:** Volume back translate AA sequences   

**【python 3.4.3】**

**Usage example:**

            1.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin F:\software\mafft\mafft-win\pro -NUCin C:\Users\Administrator\Desktop\nuc -s fast a -c 2   【for folder】
                        		
            2.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin pro -NUCin nuc -s paml -c 2   【for folder】
                        		
            3.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin test.aln -NUCin test.nuc -s clustal -c 2 -nogap -blockonly   【for file】

---
#refineGB.py

**usage:**      `refineGB.py [-h] -f FILE [-n NUM] -o OUT`

**Description:** Refine GenBank file to standard format.

**optional arguments:**

                  -h, --help  show this help message and exit
                  
                  -f FILE     input GenBank file or folder
                  
                  -n NUM      define minimum of the length of the NCR
                  
                  -o OUT      folder of the out file
  
【python 3.4.3】

**Usage example:**

        1.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\scripts\demo.gb -n 300 -o C:\Users\Desktop\myfolder
        
        2.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\gbfolder -o C:\Users\Desktop\myfolder

---
#alter_name.py

---

**usage:** `alter_name.py [-h] -f FILE [-gb] [-o OUT]`

**Description:** Simplify default name of fasta file from NCBI

**optional arguments:**

                  -h, --help  show this help message and exit
                  
                  -f FILE     input fasta file
                  
                  -gb         whether retain gb number or not
                  
                  -o OUT      out file name

【python 3.4.3】

**Usage example:**

	  1.python C:\Users\Desktop\scripts\alter_name.py -f C:\Users\Desktop\demo.fasta -o C:\Users\Desktop\demo-out.fasta
      
      2.python C:\Users\Desktop\scripts\alter_name.py -f C:\Users\Desktop\demo.fasta -o C:\Users\Desktop\demo-out.fasta -gb
      
