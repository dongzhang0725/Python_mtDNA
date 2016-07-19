#convertfmt.py

`Description:`Convert fasta file to selected format `【phylip|nexus|paml|axt】`

optional arguments:

              -h:       --help  show this help message and exit
              
              -f:       input fasta file
              
              -phy:     convert into phylip format
              
              -nex:     convert into nexus format
              
              -paml:    convert into paml format
              
              -axt:     convert into axt format
              
              -stat:    generate statistics of the fasta file

`【python 3.4.3】`

`Usage example:`

            1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
            
            2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat
            
            3.3.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\fas-folder -nex
