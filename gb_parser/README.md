#gb_parser.py
`【python 3.4.3】`  `biopython must be enabled`

`usage:` 

`gb_parser.py [-h] [-f FILE] [-n {14,15}] [-r REPLACE] [-t {1,2,3,4}] [-c {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}] [-e EXCLUDE] [-p PREFER] [-aa] [-nuc] [-rRNA] [-tRNA] [-geom] [-table] [-order] [-name] [-stat] [-csv]`

`Description:` Parse GenBank file to extract interested information

`optional arguments:`

                    -h, --help            show this help message and exit
                    
                    -f FILE               input GenBank file
                    
                    -n {14,15}            the amount of the protein plus rRNA genes among mtDNA
                    
                    -r REPLACE            the replace file with unified gene names involved in
                    
                    -t {1,2,3,4}          **** choose a type **** 
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


`Usage example:`

    You can omit '-f' and '-r' under the premise of a GenBank file named 'sequences.gb' and a replace file named 'replace.txt' are placed in the dir of the scripts:
    
        【muti-prefer species】 python D:\parseGB\bin\gb_parser.py -c 9 -p NC_030050 -p NC_016950 -p JQ038228 -aa -nuc -rRNA -tRNA -geom -table -order -name -stat -csv
        
        【muti-excluded species】python D:\parseGB\bin\gb_parser.py -c 9 -e NC_030050 -e NC_016950 -e JQ038228 -aa -nuc -rRNA -tRNA -geom -table -order -name -stat -csv
    
    Specify GenBank file and replace file:
    
        【only output AA sequence】 python D:\parseGB\bin\gb_parser.py -c 9 -f C:\users\sequences.gb -r C:\users\replace.txt -aa
        
        【specify the number of PCGs plus rRNAs】 python D:\parseGB\bin\gb_parser.py -c 9 -n 15 -f C:\users\sequences.gb -r C:\users\replace.txt -aa -nuc
        
        【specify type of the species name】 python D:\parseGB\bin\gb_parser.py -c 9 -t 2 -f C:\users\sequences.gb -r C:\users\replace.txt -table -order
       
        【use default codon table(1)】  python D:\parseGB\bin\gb_parser.py -t 2 -f C:\users\sequences.gb -r C:\users\replace.txt -table -order
