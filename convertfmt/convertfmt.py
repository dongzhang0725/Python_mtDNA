#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年5月18日'
__author__  =  'zhang dong;708986950@qq.com'


class Handle_file:
    def __init__(self,file):
        self.file = file        
        self.phy = ''
        self.nex = ''
        self.paml = ''
        self.axt_name = ''
        self.axt_seq = ''
        self.statistics = 'Name,Lenth\n'
        self.count = 1   
    def align(self):  
        list_seq = re.findall(r'(.{60})',self.seq)   
        remainder = len(self.seq)%60  
        if remainder == 0:
            self.align_seq = '\n'.join(list_seq) + '\n'
        else:
            self.align_seq = '\n'.join(list_seq) +'\n' + self.seq[-remainder:] + '\n'
    def assign(self):
        self.align()
        self.statistics += self.name + ',' + str(len(self.seq)) + '\n'
        self.phy += self.name + ' ' + self.seq + '\n'
        self.nex += '['+str(self.count) +'] ' + self.name + ' ' + self.seq + '\n'
        self.paml += self.name + '\n' + self.align_seq + '\n'
        self.axt_name += self.name.replace('_',' ') + '-'
        self.axt_seq += self.seq + '\n'
        self.count += 1
    def judge(self):
        DNA = re.search(r'[ATCG]{10}',self.seq,re.I)  
        PROTEIN = re.search(r'[GAVLIFWYDHNEKQMRSTCP]{10}',self.seq,re.I)
        if DNA:
            self.pattern = 'DNA'
        elif PROTEIN:
            self.pattern = 'PROTEIN'
        else:
            print('ERROR!neither nucleotide nor protein sequences!')
    def complete(self):
        self.phy = ' '+str(self.count - 1)+' '+str(len(self.seq))+'\n' + self.phy  
        self.nex = '#NEXUS\nBEGIN DATA;\ndimensions ntax=%s nchar=%s;\nformat missing=?\ndatatype=%s gap= -;\n\nmatrix\n'\
              %(str(self.count - 1),str(len(self.seq)),self.pattern) + self.nex + ';\nEND;\n'
        self.paml = str(self.count - 1)+'  '+str(len(self.seq))+'\n\n' + self.paml
        self.axt = self.axt_name.strip('-') + '\n' + self.axt_seq
    def handle(self):
        with open(self.file) as self.f:
            self.line = self.f.readline()
            while self.line != '':
                while not self.line.startswith('>'):  
                    self.line = self.f.readline()
                self.name = self.line.strip('>').strip('\n').replace(' ','_')
                self.name = re.sub(r'\||[(]|[)]|"|:','',self.name) 
                self.seq = ''
                self.line = self.f.readline()  
                while not self.line.startswith('>') and self.line != '':
                    self.seq += self.line.strip().replace(' ','')                    
                    self.line = self.f.readline()
                self.assign()    
    def save(self,inputfile):
        if myargs.phy:
            with open(myargs.out+'/'+os.path.basename(inputfile).split('.')[0]+'.phy','w') as f1:
                f1.write(self.phy)
        if myargs.nex:
            with open(myargs.out+'/'+os.path.basename(inputfile).split('.')[0]+'.nex','w') as f2:
                f2.write(self.nex)
        if myargs.paml:
            with open(myargs.out+'/'+os.path.basename(inputfile).split('.')[0]+'.PML','w') as f3:
                f3.write(self.paml)
        if myargs.axt:
            with open(myargs.out+'/'+os.path.basename(inputfile).split('.')[0]+'.axt','w') as f4:
                f4.write(self.axt)
        if myargs.stat:
            with open(myargs.out+'./statistics.csv','w') as f5:
                f5.write(self.statistics)       
if __name__ == '__main__':
    import re,argparse,sys,os,shutil
    def parameter():
        scripts_path=os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawTextHelpFormatter,\
                prog = 'convertfmt.py',\
                description = 'Convert fasta to selected format 【phylip|nexus|paml|axt】',\
                epilog = r'''
    examples:
            1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
            2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat 
            3.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\fas-folder -nex
                ''')
        parser.add_argument('-f',dest ='file',help='input fasta file or folder',required=True)
        parser.add_argument('-phy',dest ='phy',help='turn into phylip format',\
                            default=False,action='store_true')   
        parser.add_argument('-nex',dest ='nex',help='turn into nexus format',\
                            default=False,action='store_true')
        parser.add_argument('-paml',dest ='paml',help='turn into paml format',\
                            default=False,action='store_true') 
        parser.add_argument('-axt',dest ='axt',help='turn into axt format',\
                            default=False,action='store_true') 
        parser.add_argument('-stat',dest ='stat',help='generate statistics of the fasta file',\
                            default=False,action='store_true')
        parser.add_argument('-o',dest='out',help='folder of the out file',default=scripts_path+'/batch_out')
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
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
    try:
        os.mkdir(myargs.out)
    except FileExistsError:        
        remove_dir(myargs.out)
    def main(file):        
        myHandle = Handle_file(file)
        myHandle.handle() 
        myHandle.judge()  
        myHandle.complete() 
        myHandle.save(file) 
    if os.path.isdir(myargs.file):
        files = os.listdir(myargs.file)
        for each_file in files:
            main(myargs.file+'/'+each_file)
    elif os.path.isfile(myargs.file): 
        main(myargs.file)
    else:
        print('input error!')
    print('completed!')
