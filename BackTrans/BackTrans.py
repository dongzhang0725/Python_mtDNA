#coding = utf-8
#!/usr/bin/env python
from email.policy import default

__date__  =  '2016年4月3日'
__author__  =  'zhang dong;708986950@qq.com'

def get_files(myargs):
    if os.path.isdir(myargs.AAin) and os.path.isdir(myargs.NUCin):
        pro_file = list(map(lambda x:myargs.AAin+'/'+x,os.listdir(myargs.AAin)))  #得到pro每个文件全路径
        nuc_file = list(map(lambda x:myargs.NUCin+'/'+x,os.listdir(myargs.NUCin)))  #得到nuc每个文件全路径
        inputfiles = list(map(lambda x,y:x+' '+y,pro_file,nuc_file))
    elif os.path.isfile(myargs.AAin) and os.path.isfile(myargs.NUCin):  #传入单个文件的情况
        inputfiles = [myargs.AAin + ' ' + myargs.NUCin] #必须转为列表，因为main()有for循环
    else:
        print('Input format error!') 
    return inputfiles
def main(myargs):
    os.chdir(os.path.dirname(sys.argv[0])) #路径切换到脚本所在文件夹
    input_files = get_files(myargs) #得到pro和nuc输入文件的列表
    try:
        os.mkdir('output')
    except:
        pass
    for each in input_files:
        #以核苷酸文件名命名输出名
        commands = 'perl pal2nal.pl '+each+\
        ' -output '+myargs.style + ' -codontable ' +myargs.codontable \
        + ' > '+ './output/'+each.split()[1].split('/')[-1]\
        +myargs.nogap+myargs.nomismatch+myargs.blockonly
        #这里each[1]是一个全路径:C:\Users\Administrator\Desktop\scripts/nuc/NAD6.fas
        #print('commands=%s'%commands)
        os.system(commands)
def parameter():
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
default=os.path.dirname(sys.argv[0])+'/pro')
    parser.add_argument('-NUCin',dest='NUCin',\
help='the path of folder of nucleotide sequences',\
default=os.path.dirname(sys.argv[0])+'/nuc')
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
    import os,sys,argparse
    myargs = parameter()
    main(myargs)
    print('completed!')
