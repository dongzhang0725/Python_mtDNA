#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年3月27日'
__author__  =  'zhang dong;708986950@qq.com'


class Get_results:    
    def __init__(self):
        self.filename = list(map(lambda x:myargs.folder+'/'+x,sorted(os.listdir(myargs.folder))))  
        self.dict_species = {}  
        self.dict_statistics = dict(prefix = 'taxon' )
        self.partition_style = '【partitionfinder style】\n'
        self.bayes_style = '【bayes style】\n'
        self.partition_name = '' 
        self.count = 0
        self.gene_index = []
    def handle(self):
        while self.line != '':
            self.spe_key = self.line.strip().replace('>','')
            self.spe_key = re.sub(r'\||[(]|[)]|"|:','',self.spe_key)
            self.line = self.f.readline()  
            self.seq = ''
            while not self.line.startswith('>') and self.line != '':
                self.seq += self.line.strip().replace(' ','')
                self.line = self.f.readline()              
            if self.count == 1:  
                self.dict_species[self.spe_key] = self.seq
                lenth = len(self.seq) 
                indels = self.seq.count('-')
                self.dict_statistics[self.spe_key] = self.spe_key+'\t'+str(lenth)+' ('+str(indels)+' indels)'
            else:
                self.count_num += 1
                self.list_spe.append(self.spe_key)
                try:                
                    self.dict_species[self.spe_key] += self.seq 
                except KeyError as reason:
                    print('''ERROR:Can't find %s in 【%s】 which exsisted in 【%s】!'''%(reason,self.filename[0],self.each))
                lenth = len(self.seq)  
                indels = self.seq.count('-')  
                self.dict_statistics[self.spe_key] += '\t'+str(lenth)+' ('+str(indels)+' indels)'
    def lack(self):
        if self.count_num != len(list(self.dict_species.keys())) and self.count_num != 0:
            lack = [i for i in list(self.dict_species.keys()) if i not in self.list_spe]
            print('''ERROR:Can't find %s in 【%s】'''%(str(lack),self.each))
    def add(self):
        span = re.search(self.seq + '$',self.dict_species[self.spe_key]).span()
        self.gene_index.append(span)
        self.partition_style += os.path.splitext(os.path.basename(self.each))[0] + '=' + str(span[0]+1) + '-' + str(span[1]) + ';\n'
        self.bayes_style += 'charset ' + os.path.splitext(os.path.basename(self.each))[0] + '=' + str(span[0]+1) + '-' + str(span[1]) + ';\n'
        self.partition_name += os.path.splitext(os.path.basename(self.each))[0]+','
        print('%s done!'%os.path.basename(self.each))
    def each_file(self):
        for self.each in self.filename:
            self.count += 1        
            with open(self.each) as self.f:
                self.count_num = 0 
                self.list_spe = [] 
                self.line = self.f.readline()
                self.dict_statistics['prefix'] += '\t'+os.path.basename(self.each)  
                self.handle()
                self.lack()  
            self.add()           
    def judge(self):
        DNA = re.search(r'[ATCG]{20}',self.seq,re.I)  
        PROTEIN = re.search(r'[GAVLIFWYDHNEKQMRSTCP]{20}',self.seq,re.I)
        if DNA:
            self.pattern = 'DNA'
        elif PROTEIN:
            self.pattern = 'PROTEIN'
        else:
            print('ERROR!neither nucleotide nor protein sequences!')
    def align(self,seq): 
        list_seq = re.findall(r'(.{60})',seq)   
        remainder = len(seq)%60  
        if remainder == 0:
            self.align_seq = '\n'.join(list_seq) + '\n'
        else:
            self.align_seq = '\n'.join(list_seq) +'\n' + seq[-remainder:] + '\n'
    def nxs_interleave(self):
        length = len(self.dict_species[self.list_keys[-1]]) 
        integer = length//60
        num = 1
        while num <= integer:
            for i in self.list_keys:
                self.nxs_inter += i+' '+self.dict_species[i][(num-1)*60:num*60]+'\n'
            self.nxs_inter += "\n"
            num += 1    
        if length%60 != 0:
            for i in self.list_keys:
                self.nxs_inter += i+' '+self.dict_species[i][(num-1)*60:length]+'\n'
        for each_span in self.gene_index: 
            for i in self.list_keys:
                self.nxs_gene += i + " " + self.dict_species[i][each_span[0]:each_span[1]] + "\n"
            self.nxs_gene += "\n"                 
    def get_str(self):
        for i in self.list_keys:
            self.num += 1
            self.dict_statistics[i] += '\t'+str(len(self.dict_species[i]))+'\t'+str(self.count)+'\n'
            self.file += '>'+i + '\n' + self.dict_species[i] + '\n'
            self.phy_file += i + ' ' + self.dict_species[i] + '\n'
            self.nxs_file += '['+str(self.num) +'] '+i+' '+self.dict_species[i]+'\n'
            self.align(self.dict_species[i])
            self.paml_file += i + '\n' + self.align_seq + '\n'
            self.axt_file += self.dict_species[i] + '\n'
            self.statistics += self.dict_statistics[i]
            
    def complete(self):
        self.partition_name = 'partition Names = %s:'%str(self.count)+self.partition_name.strip(',')+';\nset partition=Names;'  
        self.dict_statistics['prefix'] += '\tTotal lenth\tNo of charsets\n'
        self.list_keys = sorted(list(self.dict_species.keys())) 
        self.judge() 
        self.file = ''
        self.phy_file = ' '+str(len(self.list_keys))+' '+str(len(self.dict_species[self.list_keys[-1]])) + '\n'
        self.nxs_file = '#NEXUS\nBEGIN DATA;\ndimensions ntax=%s nchar=%s;\nformat missing=?\ndatatype=%s gap= -;\n\nmatrix\n'%(str(len(self.list_keys)),str(len(self.dict_species[self.list_keys[-1]])),self.pattern)
        self.nxs_inter = '#NEXUS\nBEGIN DATA;\ndimensions ntax=%s nchar=%s;\nformat missing=?\ndatatype=%s gap= - interleave;\n\nmatrix\n'%(str(len(self.list_keys)),str(len(self.dict_species[self.list_keys[-1]])),self.pattern)        
        self.nxs_gene = '#NEXUS\nBEGIN DATA;\ndimensions ntax=%s nchar=%s;\nformat missing=?\ndatatype=%s gap= - interleave;\n\nmatrix\n'%(str(len(self.list_keys)),str(len(self.dict_species[self.list_keys[-1]])),self.pattern)                
        self.paml_file = str(len(self.list_keys))+'  '+str(len(self.dict_species[self.list_keys[-1]])) + '\n\n'
        self.axt_file = '-'.join(self.list_keys) + '\n'
        self.statistics = self.dict_statistics['prefix']
        self.num = 0
        self.get_str()
        self.nxs_interleave()
    def save(self):
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
            os.mkdir(scripts_path+'/seq_matrix_out')
        except:
            remove_dir(scripts_path+'/seq_matrix_out')
            pass
        if myargs.axt:
            with open(scripts_path+'/seq_matrix_out/append.axt','w') as f1:
                f1.write(self.axt_file)
        if myargs.fas:
            with open(scripts_path+'/seq_matrix_out/append.fas','w') as f2:
                f2.write(self.file)
        if myargs.stat:
            with open(scripts_path+'/seq_matrix_out/statistics.csv','w') as f3:
                f3.write(self.statistics.replace('\t',','))
        if myargs.partition:
            with open(scripts_path+'/seq_matrix_out/partition.txt','w') as f4:
                f4.write(self.partition_style + self.bayes_style+self.partition_name)
        if myargs.phy:
            with open(scripts_path+'/seq_matrix_out/append.phy','w') as f5:
                f5.write(self.phy_file)
        if myargs.nex:
            with open(scripts_path+'/seq_matrix_out/append.nex','w') as f6:
                f6.write(self.nxs_file+';\nEND;\n')
        if myargs.paml:
            with open(scripts_path+'/seq_matrix_out/append.PML','w') as f7:
                f7.write(self.paml_file)
        if myargs.nex2:
            with open(scripts_path+'/seq_matrix_out/append_interleave.nex','w') as f8:
                f8.write(self.nxs_inter+';\nEND;\n')        
        if myargs.nex3:
            with open(scripts_path+'/seq_matrix_out/append_inter_gene.nex','w') as f9:
                f9.write(self.nxs_gene+';\nEND;\n')
        
if __name__ == '__main__':   
    import os,re,argparse,sys,shutil
    scripts_path = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
    def parameter():
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawTextHelpFormatter,\
                prog = 'seq_matrix.py',\
                description = 'Concatenated muti-self.sequences into one file',\
                epilog = r'''
【python 3.4.3】                
                
The output file will be deposited in the dir seq_matrix_out

examples:
    1.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -f C:\Users\Administrator\Desktop\scripts\partitions -phy
    2.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -phy -nex -paml -fas -axt -stat -part   【On condition that there is a 'partitions' folder in the directory of %(prog)s】 
            ''')
        parser.add_argument('-f',dest ='folder',help='input folder which include muti-sequences',\
                            default=scripts_path+'/partitions')
        parser.add_argument('-phy',dest ='phy',help='generate phylip format',\
                            default=False,action='store_true')   
        parser.add_argument('-nex',dest ='nex',help='generate nexus format',\
                            default=False,action='store_true')
        parser.add_argument('-paml',dest ='paml',help='generate paml format',\
                            default=False,action='store_true') 
        parser.add_argument('-axt',dest ='axt',help='generate axt format',\
                            default=False,action='store_true') 
        parser.add_argument('-fas',dest ='fas',help='generate fasta file',\
                            default=False,action='store_true')
        parser.add_argument('-stat',dest ='stat',help='generate statistics file',\
                            default=False,action='store_true')
        parser.add_argument('-part',dest ='partition',help='generate partition file',\
                            default=False,action='store_true')
        parser.add_argument('-nex2',dest ='nex2',help='generate interleave nexus format',\
                            default=False,action='store_true')
        parser.add_argument('-nex3',dest ='nex3',help='generate interleave nexus format delimited by genes, so as to run Best',\
                            default=False,action='store_true')
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
    def main():
        myresult = Get_results()
        myresult.each_file() 
        myresult.complete() 
        myresult.save() 
    main()    
    print('completed!')
