#converfmt.py

`Description:`Convert fasta to selected format 【phylip|nexus|paml|axt】

optional arguments:

              -h:       --help  show this help message and exit
              
              -f:       input fasta file
              
              -phy:     turn into phylip format
              
              -nex:     turn into nexus format
              
              -paml:    turn into paml format
              
              -axt:     turn into axt format
              
              -stat:    generate statistics of the fasta file

`Usage example:`

            1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
            
            2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat
