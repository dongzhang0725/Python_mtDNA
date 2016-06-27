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
    1.python C:\Users\Desktop\scripts\alter_name.py -f C:\Users\Desktop\demo.fasta -o C:\Users\Desktop\demo-out.fasta
    2.python C:\Users\Desktop\scripts\alter_name.py -f C:\Users\Desktop\demo.fasta -o C:\Users\Desktop\demo-out.fasta -gb
                ''')
        parser.add_argument('-f',dest ='file',help='input fasta file',required=True)
        parser.add_argument('-gb',dest ='gb_num',help='whether retain gb number or not',default=False,action='store_true')
        parser.add_argument('-o',dest='out',help='out file name',default = sys.stdout,type=argparse.FileType('w'))
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    def run(file,myargs):
        with open(file) as f:
            content = f.read()
            f.seek(0,0)
            line = f.readline()
            dict_name = {}
            line_num = 1
            while line != '':
                while not line.startswith('>'):
                    line = f.readline()
                    line_num += 1
                try: 
                    dict_name[line] = '>'+re.search(r'(?<=\| ).+?(?= (16S|mitochondrion|cytochrome|18S|internal transcribed spacer))',\
                                    line,re.I).group().replace(' ','_')+('_'+re.search(r'(?<=gb\|)([A-Z]{2}\d{6})(?=\.\d)', line, re.I).group() if myargs.gb_num else '')+'\n' 
                except AttributeError:
                    print('warning:nothing changed in line %d 【%s】'%(line_num,line.strip()))
                line = f.readline()
                line_num += 1
                while not line.startswith('>') and line != '':        
                    line = f.readline()
                    line_num += 1
        for key,value in dict_name.items():
            value = re.sub(r'\||[(]|[)]|"','',value)
            content = content.replace(key,value)
        myargs.out.write(content)
    myargs = parameter()                    
    run(myargs.file,myargs)
if __name__ == '__main__':
    import re,os,sys,argparse
    main()
    print('completed!')
