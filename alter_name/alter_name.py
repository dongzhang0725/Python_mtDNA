#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年6月5日'
__author__  =  'zhang dong;708986950@qq.com'
__version__ = 'python3.4.3'

def main():
    def parameter():
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawTextHelpFormatter,\
                prog = 'alter_name.py',\
                description = 'Simplify default name of fasta file from NCBI',\
                epilog = r'''
examples:
    python C:\Users\Desktop\scripts\alter_name.py -f C:\Users\Desktop\demo.fasta -o C:\Users\Desktop\demo-out.fasta
                ''')
        parser.add_argument('-f',dest ='file',help='input fasta file',required=True)
        parser.add_argument('-o',dest='out',help='out file name',default = sys.stdout,type=argparse.FileType('w'))
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    def run(file,myargs):
        with open(file) as f:
            content = f.read()
            f.seek(0,0)
            line = f.readline()
            dict_name = {}
            while line != '':
                while not line.startswith('>'):
                    line = f.readline()
                dict_name[line] = '>'+re.search(r'(?<=\| ).+?(?= (16S|mitochondrion|cytochrome|18S|internal transcribed spacer))',line,re.I).group().replace(' ','_')+'\n'  
                line = f.readline()
                while not line.startswith('>') and line != '':        
                    line = f.readline()
        for key,value in dict_name.items():
            content = content.replace(key,value)
        myargs.out.write(content)
    myargs = parameter()                    
    run(myargs.file,myargs)
if __name__ == '__main__':
    import re,os,sys,argparse
    main()
    print('completed!')
