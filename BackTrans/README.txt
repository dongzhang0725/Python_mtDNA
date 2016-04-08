usage: BackTrans.py [-h] [-s {clustal,paml,fasta,codon}]
                     [-c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}]
                     [-AAin AAIN] [-NUCin NUCIN] [-nogap] [-nomismatch]
                     [-blockonly]

Volume back translate AA sequences

optional arguments:
  -h, --help            show this help message and exit
  -s {clustal,paml,fasta,codon}
                        output style【clustal|paml|fasta|codon】
  -c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}
                        Choose a codon table!【1(default)|2|3|4|5|6|9|10|11|12|13|14|15|16|21|22|23】
                        NCBI GenBank codon table
                         1  Universal code
                         2  Vertebrate mitochondrial code
                         3  Yeast mitochondrial code
                         4  Mold, Protozoan, and Coelenterate Mitochondrial code and Mycoplasma/Spiroplasma code
                         5  Invertebrate mitochondrial
                         6  Ciliate, Dasycladacean and Hexamita nuclear code
                         9  Echinoderm and Flatworm mitochondrial code
                        10  Euplotid nuclear code
                        11  Bacterial, archaeal and plant plastid code
                        12  Alternative yeast nuclear code
                        13  Ascidian mitochondrial code
                        14  Alternative flatworm mitochondrial code
                        15  Blepharisma nuclear code
                        16  Chlorophycean mitochondrial code
                        21  Trematode mitochondrial code
                        22  Scenedesmus obliquus mitochondrial code
                        23  Thraustochytrium mitochondrial code
						
  -AAin AAIN            the path of folder of AA sequences【just drag and drop the folder or file onto the command prompt】
  -NUCin NUCIN          the path of folder of nucleotide sequences
  -nogap                remove columns with gaps and inframe stop codons
  -nomismatch           remove mismatched codons (mismatch between pep and cDNA) from the output
  -blockonly            Show only user specified blocks '#' under CLUSTAL alignment (see example of pal2nal.pl for detail)
  
- sequence order in AA and NUC files should be the same.

- IDs in nuc.fasta are used in the output.

example:
            1.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin F:\software\mafft\mafft-win\pro -NUCin  
     		  C:\Users\Administrator\Desktop\nuc -s fast a -c 2   【for folder】
            2.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin pro -NUCin nuc -s paml -c 2   【for folder】
            3.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin test.aln -NUCin test.nuc 
			  -s clustal -c 2 -nogap -blockonly   【for file】

