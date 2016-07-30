#mafft_plus.py
---
【python 3.4.3】  `[**biopython**][hover] must be enabled `
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
