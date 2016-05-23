#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年4月3日'
__author__  =  'zhang dong;708986950@qq.com'

def get_files(myargs):
    if os.path.isdir(myargs.AAin) and os.path.isdir(myargs.NUCin):
        pro_file = list(map(lambda x:myargs.AAin+'/'+x,os.listdir(myargs.AAin))) 
        nuc_file = list(map(lambda x:myargs.NUCin+'/'+x,os.listdir(myargs.NUCin)))
        inputfiles = list(map(lambda x,y:x+' '+y,pro_file,nuc_file))
    elif os.path.isfile(myargs.AAin) and os.path.isfile(myargs.NUCin):
        inputfiles = [myargs.AAin + ' ' + myargs.NUCin]
    else:
        print('Input format error!') 
    return inputfiles

def remove_dir(path):
    filelist=os.listdir(path)  
    for f in filelist:
        filepath = os.path.join( path, f )  
        if os.path.isfile(filepath):  
            os.remove(filepath)  
            print(filepath+" removed!")
        elif os.path.isdir(filepath):  
            shutil.rmtree(filepath,True)
            print("dir "+filepath+" removed!")
            
def main(myargs):
    scripts_path = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
    input_files = get_files(myargs)
    try:
        os.mkdir(scripts_path + '/BackTrans_out')
    except:
        remove_dir(scripts_path + '/BackTrans_out')
        pass
    for each in input_files:
        commands = 'perl pal2nal.pl '+each+\
        ' -output '+myargs.style + ' -codontable ' +myargs.codontable \
        + ' > '+ scripts_path + '/BackTrans_out/'+each.split()[1].split('/')[-1]\
        +myargs.nogap+myargs.nomismatch+myargs.blockonly
        os.system(commands)
def parameter():
    scripts_path = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
    parser = argparse.ArgumentParser(\
formatter_class=argparse.RawTextHelpFormatter,\
prog = 'BackTrans.py',\
description = 'Volume back translate AA sequences',\
epilog = r'''- sequence order in AA and NUC files should be the same.

- IDs in nuc.fasta are used in the output.

example:
            1.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin F:\software\mafft\mafft-win\pro -NUCin C:\Users\Administrator\Desktop\nuc -s fasta -c 2   【for folder】
            2.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin pro -NUCin nuc -s paml -c 2   【for folder】
            3.python C:\Users\Administrator\Desktop\scripts\backtrans.py -AAin test.aln -NUCin test.nuc -s clustal -c 2 -nogap -blockonly  【for file】
''')
    
    parser.add_argument('-s',dest='style',\
help='output style【clustal|paml|fasta|codon】',\
choices=['clustal','paml','fasta','codon'],default='fasta')
    parser.add_argument('-c',dest='codontable',\
help='''Choose a codon table!【1(default)|2|3|4|5|6|9|10|11|12|13|14|15|16|21|22|23】
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
23  Thraustochytrium mitochondrial code''',\
choices=['1', '2', '3', '4', '5', '6', '7', '8',\
         '9', '10', '11', '12', '13', '14', '15', '16','21','22','23'],\
default='1')
    parser.add_argument('-AAin',dest='AAin',\
help='''the path of folder of AA sequences
【just drag and drop the folder or file onto the command prompt】''',\
default=scripts_path+'/AA')
    parser.add_argument('-NUCin',dest='NUCin',\
help='the path of folder of nucleotide sequences',\
default=scripts_path+'/NUC')
    parser.add_argument('-nogap',dest='nogap',\
help='remove columns with gaps and inframe stop codons',default='',\
const=' -nogap',action='store_const')
    parser.add_argument('-nomismatch',dest='nomismatch',\
help='remove mismatched codons (mismatch between pep and cDNA)\
from the output',default='',\
const=(' -nomismatch'),action='store_const')
    parser.add_argument('-blockonly',dest='blockonly',\
help="Show only user specified blocks\
 '#' under CLUSTAL alignment (see example of pal2nal.pl for detail)",\
const=' -blockonly',action='store_const',default='')
    myargs = parser.parse_args(sys.argv[1:])
    return myargs

if __name__ == '__main__':
    import os,sys,argparse,shutil
    myargs = parameter()
    main(myargs)
    print('completed!')
