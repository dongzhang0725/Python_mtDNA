# BackTrans.py 

`Description:`Volume back translate AA sequences   

`Usage example:`

            1.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin F:\software\mafft\mafft-win\pro -NUCin C:\Users\Administrator\Desktop\nuc -s fast a -c 2   【for folder】
                        		
            2.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin pro -NUCin nuc -s paml -c 2   【for folder】
                        		
            3.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin test.aln -NUCin test.nuc -s clustal -c 2 -nogap -blockonly   【for file】

#converfmt.py

`Description:`Convert fasta to selected format 【phylip|nexus|paml|axt】

optional arguments:

              -h: --help  show this help message and exit
              
              -f :     input fasta file
              
              -phy :       turn into phylip format
              
              -nex  :      turn into nexus format
              
              -paml  :     turn into paml format
              
              -axt  :      turn into axt format
              
              -stat :      generate statistics of the fasta file

`Usage example:`

            1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
            
            2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat

