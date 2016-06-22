#!/usr/bin/env python
# -*- coding:utf-8 -*-

__file__    = 'gb_parser.py'
__date__    = '2016-3-8'
__author__  = 'zhang dong;708986950@qq.com;@P&Clab @CAS @CHINA'
__version__ = 'python3.4.3'

class Handle_GB:
    def get_ids(self):
        while not self.line.startswith('LOCUS'):  
            self.line = self.src.readline()  
        self.gb_num = self.line.split()[1]
        assert self.gb_num != '',self.gb_num
        try:     
            while not self.line.startswith('VERSION'):
                self.line = self.src.readline()
            parts = self.line.split()
            assert 3 == len(parts) , parts
            giparts = parts[2].partition(':')
            assert giparts[2] , giparts
            assert giparts[2].isdigit()
            self.GB_1 = parts[1]
            self.GI = giparts[2]  
        except:
            pass
    def get_latin(self):
        self.line = self.src.readline()
        while not self.line.startswith('  ORGANISM'):
            self.line = self.src.readline()
        self.latin = re.search(r'  ORGANISM  (.+)\n',self.line).group(1).replace(' ','_')  
    
    def skip_to_feature(self):   
        self.line = self.src.readline()
        while not self.line.startswith('FEATURES'):
            self.line = self.src.readline()
        return self.line
    
    def is_feature_start(self):   
        return self.line and self.line[5] != ' '
    def next_item(self):  
        self.line = self.skip_to_feature()  
        self.line = self.src.readline()   
        while not self.line.startswith('ORIGIN'):  
            assert self.is_feature_start()   
            feature = self.read_feature()         
            yield feature    
    def is_attribute_start(self):
        attribute_prefix = 21*' ' + '/' 
        return self.line and self.line.startswith(attribute_prefix)
    
    def read_feature(self):
        feature = self.line.split()
        assert feature
        self.line = self.src.readline()  
        props = {}
        while not self.is_feature_start():
            assert 2 == len(self.line.split('=')),self.line.split('=')
            key,value = self.line.strip()[1:].split('=')  
            fullvalue,self.line = self.get_value(value) 
            props[key] = fullvalue
        feature.append(props)
        return feature
    def get_value(self,value):
        self.line = self.src.readline() 
        while (not self.is_attribute_start() and not self.is_feature_start()): 
            value += self.line.strip()  
            self.line = self.src.readline()  
        fullvalue = value.strip('"') 
        return fullvalue,self.line    
    def get_item(self):
        self.item = []
        for self.each in self.next_item():
            self.item.append(self.each)
    
    def skip_to_origin(self):
        self.line = self.src.readline()
        while not self.line.startswith('ORIGIN'):
            self.line = self.src.readline()
    
    def get_sequence(self):
        self.line = self.src.readline()   
        self.seq = ''
        while not self.line.startswith('//'):
            self.seq += self.line[10:-1].replace(' ','')
            self.line = self.src.readline()            
    def species_generator(self):          
        self.line = self.src.readline()
        while not self.line == '':
            self.get_ids() 
            self.get_latin() 
            self.get_item() 
            self.get_sequence() 
            while not self.line.startswith('LOCUS') and self.line != '':  
                self.line = self.src.readline()  
            yield
class Extract_inf():
    def decide(self):
        if myargs.type == 1:
            self.decision = self.latin
        if myargs.type == 2:
            self.decision = self.gb_num
        if myargs.type == 3:
            self.decision = self.breviary
        if myargs.type == 4:
            self.decision = self.latin_gb        
    def find_pos(self):
        list1 = re.findall(r'[0-9]+',self.i[1])     
        ini,ter = list1[0],list1[1]    
        assert ini.isdigit() and ter.isdigit(),ini
        start,stop = int(ini) - 1,int(ter) 
        if self.i[1].startswith('complement'):
            if 'join' in self.i[1]:
                assert len(list1) == 4,list1
                seq = self.seq[start:stop] + self.seq[int(list1[2])-1:int(list1[3])]  
            else:
                seq = self.seq[start:stop]  
            seq = seq[::-1].upper() 
            gene_seq = ''
            dict1 = {"A":"T","T":"A","C":"G","G":"C"}
            for self.i in seq:
                if self.i in 'ATGC':
                    gene_seq += dict1[self.i]     
                else:
                    gene_seq += self.i  
            return gene_seq
        else:
            if 'join' in self.i[1]:
                assert len(list1) == 4,list1
                return self.seq[start:stop] + self.seq[int(list1[2])-1:int(list1[3])]  
            else:
                return self.seq[start:stop]  
    
    def substitute(self):
        self.dict_replace = {}
        try:
            for each in myargs.replace:
                if each != '\n':
                    former,new = each.strip().split('-->')
                    self.dict_replace[former] = new
        except OSError as reason:
            print('name not replaced,because:'+str(reason))        
    def replace(self,old_name):
        try:
            old_name = self.dict_replace[old_name]
        except KeyError:
            pass
        return old_name              
    def judge(self,name,values):
        if name == 'tRNA-Leu' or name == 'tRNA-Ser':
            if re.search(r'(?<=[^1-9a-z_])(Leu1|CUA|CUN|tag|L1|trnL1)(?=[^1-9a-z_])',values,re.I): 
                name = 'tRNA-Leu1'
            elif re.search(r'(?<=[^1-9a-z_])(Leu2|UUA|UUR|taa|L2|trnL2)(?=[^1-9a-z_])',values,re.I):
                name = 'tRNA-Leu2'
            elif re.search(r'(?<=[^1-9a-z_])(Ser2|UCA|UCN|tga|S2|trnS2)(?=[^1-9a-z_])',values,re.I):
                name = 'tRNA-Ser2'
            elif re.search(r'(?<=[^1-9a-z_])(Ser1|AGC|AGN|AGY|gct|tct|S1|trnS1)(?=[^1-9a-z_])',values,re.I):
                name = 'tRNA-Ser1'
            else:
                position = '【'+self.i[0] + '\t' + self.i[1] + '】'
                self.exception += 'Ambiguous annotation about S1, S2, L1 and L2 in %s for %s\n'%(position,self.gb_num)
        else:
            name = name
        return name
    def gene_num(self):
        list_PCGs14 = ['COX1','COX2','NAD6','NAD5','COX3','CYTB','NAD4L','NAD4','ATP6','NAD2','NAD1','NAD3','12S','16S']
        list_PCGs15 = ['COX1','COX2','NAD6','NAD5','COX3','CYTB','NAD4L','NAD4','ATP6','NAD2','NAD1','NAD3','ATP8','12S','16S']
        if myargs.num == 14:
            return list_PCGs14
        elif myargs.num == 15:
            return list_PCGs15
    def variable(self):
        self.pro_seq = ''
        self.rRNA_seq = ''
        self.tRNA_seq = ''
        self.tRNA_fas = ''
        self.NCR = ''
        self.dict_pro = {}
        self.dict_rRNA = {}
        self.dict_tRNA = {}
        self.dict_name = {} 
        self.dict_start = {}    
        self.dict_stop = {}
        self.dict_PCG = {}  
        self.dict_RNA = {}  
        self.dict_geom = {} 
        self.dict_spe_stat = {} 
        self.list_abbre = []
        self.list_sequence = []
        self.substitute()  
        self.linear_order = ''  
        self.complete_seq = ''
        self.exception = '' 
        self.error_species = ''  
        self.error_gb = ''
        self.list_PCGs = self.gene_num() 
    def variable1(self):
        self.list_sequence.append(self.seq)
        self.PCGs = '' 
        self.tRNAs = '' 
        self.dict_genes = {}  
        self.breviary = self.latin.split('_')[0][0] + '_' + '_'.join(self.latin.split('_')[1:])  
        self.latin_gb = self.latin + '_' + self.gb_num
        self.tree_name = self.latin.replace('_',' ') + ' (' + self.gb_num + ')'
        self.abbreviation = self.latin.split('_')[0][0]+'_'+self.latin.split('_')[1][0]
        self.dict_geom[self.latin.replace('_',' ')] = self.latin.replace('_',' ')+','+self.abbreviation+\
        ',' + self.gb_num+','+str(len(self.seq))+','+str((self.seq.upper().count('A')+self.seq.upper().count('T'))/len(self.seq.upper())*100)+'\n'
        self.list_abbre.append(self.abbreviation)  
    def source(self):
        if 'isolate' in self.i[2]:
            self.latin = self.latin + '_' + self.i[2]['isolate'].replace(' ','_')
        self.breviary = self.latin.split('_')[0][0] + '_' + '_'.join(self.latin.split('_')[1:])
        self.decide() 
        self.gene_order = '>' +  self.decision+'\n'
        self.dict_name[self.decision] = self.tree_name
        self.complete_seq += '>' + self.decision +'\t'+ self.seq + '\n'  
    def CDS(self):
        def codon():
            seq = self.find_pos().upper()
            size = len(seq)
            ini = seq[0:3]
            if size % 3 == 0:
                ter = seq[-3:]
            elif size % 3 == 1:
                ter = seq[-1]
            elif size % 3 == 2:
                ter = seq[-2:]
            return ini,ter,size,seq
        ini,ter,size,seq = codon()
        try:       
            try:
                old_name = self.i[2]['gene'].upper()
            except:
                self.exception += 'ERROR:no "/gene" annotation in 【%s】 for %s, "/product" has been invoked\n'%(self.i[1],self.latin+'_'+self.gb_num)
                old_name = self.i[2]['product']           
            new_name = self.replace(old_name)  
            try:     
                self.list_pro.remove(new_name)
            except ValueError:  
                print('%s is a superfluous gene in %s\n'%(new_name,self.latin)) 
                self.exception += '%s is a superfluous gene in %s\n'%(new_name,self.latin)       
                self.error_species += '【%s】\t'%(self.latin + '_' + self.gb_num)
                self.error_gb += self.gb_num + ' '
            self.dict_pro[new_name + '>' + self.latin] = '>' + self.decision +'\n'+ self.find_pos() + '\n'
            self.pro_seq +=  self.decision +'\t'+ new_name + '\t' + self.find_pos() + '\n'
            self.gene_order += new_name + ' '
            try:
                self.dict_PCG[new_name]+=','+str(size)
                self.dict_start[new_name]+=','+ini
                self.dict_stop[new_name]+=','+ter                            
            except KeyError:
                self.dict_PCG[new_name]=new_name+','+str(size)   
                self.dict_start[new_name]=new_name+','+ini
                self.dict_stop[new_name]=new_name+','+ter   
            self.dict_genes[new_name]=new_name+','+str(size)+','+'%.1f'%(seq.count('T')*100/size)+','+\
                                 '%.1f'%(seq.count('C')*100/size)+','+'%.1f'%(seq.count('A')*100/size)+','+\
                                 '%.1f'%(seq.count('G')*100/size)+','+'%.1f'%((seq.count('T')+seq.count('A'))*100/size)+','+\
                                 '%.1f'%(100-((seq.count('T')+seq.count('A'))*100/size))+'\n' 
            self.PCGs += seq      
        except:
            self.exception += 'ERROR:error annotation in 【%s】 for %s\n'%(self.i[1],self.latin+'_'+self.gb_num)
            pass
    def rRNA_(self):
        try:
            old_name = self.i[2]['product']
        except:
            old_name = self.i[2]['gene']
        new_name = self.replace(old_name)
        try:     
            self.list_pro.remove(new_name)
        except ValueError: 
            print('%s is a superfluous gene in %s\n'%(new_name,self.latin)) 
            self.exception += '%s is a superfluous gene in %s\n'%(new_name,self.latin)       
            self.error_species += '【%s】\t'%(self.latin + '_' + self.gb_num)
            self.error_gb += self.gb_num + ' '
        self.dict_rRNA[new_name + '>' + self.latin] = '>' + self.decision +'\n'+ self.find_pos() + '\n'
        self.rRNA_seq += self.decision +'\t'+ new_name + '\t' + self.find_pos() + '\n'
        self.gene_order += new_name + ' '
        try:
            self.dict_RNA[new_name]+=','+str(len(self.find_pos()))
        except KeyError:
            self.dict_RNA[new_name]=new_name+','+str(len(self.find_pos())) 
        seq = self.find_pos().upper()
        size = len(seq)
        self.dict_genes[new_name]=new_name+','+str(size)+','+'%.1f'%(seq.count('T')*100/size)+','+\
                             '%.1f'%(seq.count('C')*100/size)+','+'%.1f'%(seq.count('A')*100/size)+','+\
                             '%.1f'%(seq.count('G')*100/size)+','+'%.1f'%((seq.count('T')+seq.count('A'))*100/size)+','+\
                             '%.1f'%(100-((seq.count('T')+seq.count('A'))*100/size))+'\n' 
    def tRNA_(self):
        try:
            name = self.i[2]['product']
        except:
            name = self.i[2]['gene'].replace(' ','-')
        values = ':'+':'.join(list(self.i[2].values()))+':' 
        name = self.judge(name,values)  
        self.dict_tRNA[name + '>' + self.latin] = '>' + self.decision +'\n'+ self.find_pos() + '\n'
        self.tRNA_seq += self.decision +'\t'+ name + '\t' + self.find_pos() + '\n'
        self.tRNA_fas += '>' + self.decision +'_'+ name + '\n' + self.find_pos() + '\n'
        self.gene_order += name + ' '
        self.tRNAs += self.find_pos().upper()
    def NCR_(self):
        seq = self.find_pos().upper()
        size = len(seq)
        self.NCR = 'NCR,'+str(size)+','+'%.1f'%(seq.count('T')*100/size)+','+\
             '%.1f'%(seq.count('C')*100/size)+','+'%.1f'%(seq.count('A')*100/size)+','+\
             '%.1f'%(seq.count('G')*100/size)+','+'%.1f'%((seq.count('T')+seq.count('A'))*100/size)+','+\
             '%.1f'%(100-((seq.count('T')+seq.count('A'))*100/size))+'\n'
    def specie_stat(self):
        list_genes = [value for (key,value) in sorted(self.dict_genes.items())]
        size = len(self.PCGs)
        seq = self.PCGs
        self.PCGs_stat = 'PCGs,'+str(size)+','+'%.1f'%(seq.count('T')*100/size)+','+\
                 '%.1f'%(seq.count('C')*100/size)+','+'%.1f'%(seq.count('A')*100/size)+','+\
                 '%.1f'%(seq.count('G')*100/size)+','+'%.1f'%((seq.count('T')+seq.count('A'))*100/size)+','+\
                 '%.1f'%(100-((seq.count('T')+seq.count('A'))*100/size))+'\n'
        size = len(self.tRNAs)
        seq = self.tRNAs
        tRNA_stat = 'tRNAs,'+str(size)+','+'%.1f'%(seq.count('T')*100/size)+','+\
                 '%.1f'%(seq.count('C')*100/size)+','+'%.1f'%(seq.count('A')*100/size)+','+\
                 '%.1f'%(seq.count('G')*100/size)+','+'%.1f'%((seq.count('T')+seq.count('A'))*100/size)+','+\
                 '%.1f'%(100-((seq.count('T')+seq.count('A'))*100/size))+'\n'
        size = len(self.seq)
        seq = self.seq.upper()
        geom_stat = 'Full genome,'+str(size)+','+'%.1f'%(seq.count('T')*100/size)+','+\
                 '%.1f'%(seq.count('C')*100/size)+','+'%.1f'%(seq.count('A')*100/size)+','+\
                 '%.1f'%(seq.count('G')*100/size)+','+'%.1f'%((seq.count('T')+seq.count('A'))*100/size)+','+\
                 '%.1f'%(100-((seq.count('T')+seq.count('A'))*100/size))+'\n'                
        stat = 'Regions,Size (bp),T(U),C,A,G,AT(%),GC(%)\n'+ self.PCGs_stat + ''.join(list_genes)+\
              tRNA_stat+self.NCR+geom_stat
        self.dict_spe_stat[self.gb_num] = stat 
    def assert_gene_num(self):
        try:      
            assert len(self.list_pro) == 0
        except AssertionError:
            self.exception += '%s have been absent in %s\n'%(self.list_pro,self.latin)
            self.error_species += '【%s】\t'%(self.latin + '_' + self.gb_num)
            self.error_gb += self.gb_num + ' '
    def output_from_file(self):
        self.variable()
        for i in self.species_generator():
            self.list_pro = self.list_PCGs[:]
            if (not self.gb_num in myargs.exclude) and (not self.seq in self.list_sequence):  
                self.variable1()
                for self.i in self.item:
                    if self.i[0] in 'source SOURCE':
                        self.source()
                    if self.i[0] == 'CDS': 
                        self.CDS()                        
                    if self.i[0] == 'rRNA':
                        self.rRNA_()
                    if self.i[0] == 'tRNA':
                        self.tRNA_()                        
                    if self.i[0] == 'repeat_region' or self.i[0] == 'misc_feature':
                        self.NCR_()                       
                self.specie_stat()                                         
                self.linear_order += self.gene_order + '\n'
                self.assert_gene_num()
class Save_files(Handle_GB,Extract_inf):
    def __init__(self):
        self.src = myargs.file
        super().__init__()
    def trim_ter(self,raw_sequence): 
        size = len(raw_sequence)
        if size % 3 == 0:
            trim_sequence = raw_sequence[:-3]
        elif size % 3 == 1:
            trim_sequence = raw_sequence[:-1]
        elif size % 3 == 2:
            trim_sequence = raw_sequence[:-2]        
        return trim_sequence 
    def nuc(self,seq_pro,gene):
        if myargs.NUC:
            try:                
                os.mkdir('./NUC')
            except FileExistsError:
                pass          
            with open('./NUC/' + gene + '.fas','w') as f:
                f.write(seq_pro)
    def aa(self,trans_pro,gene):
        if myargs.AA:
            try:                 
                os.mkdir('./AA')
            except FileExistsError:
                pass          
            with open('./AA/' + gene + '.fas','w') as f1:      
                f1.write(trans_pro)
    def rRNA(self,seq_rRNA,gene):
        if myargs.rRNA:
            try:                  
                os.mkdir('./rRNA')
            except FileExistsError:
                pass                  
            with open ('./rRNA/' + gene + '.fas','w') as f:
                f.write(seq_rRNA)
    def tRNA(self,seq_tRNA,gene):
        if myargs.tRNA:
            try:                 
                os.mkdir('./tRNA')
            except FileExistsError:
                pass         
            with open ('./tRNA/' + gene + '.fas','w') as f:
                f.write(seq_tRNA)
    def sort_pro(self):     
        list_pro = sorted(list(self.dict_pro.keys()))
        previous = ''
        seq_pro = ''
        trans_pro = ''
        it = iter(list_pro)
        table = CodonTable.ambiguous_dna_by_id[int(self.table_num)] 
        statistics = ''
        while True:
            try:
                i = next(it)       
                gene = re.match('^[^>]+',i).group()
                if gene == previous or previous == '':        
                    seq_pro += self.dict_pro[i]
                    raw_sequence = self.dict_pro[i].split('\n')[1]   
                    trim_sequence = self.trim_ter(raw_sequence)  
                    protein = _translate_str(trim_sequence, table)  
                    trans_pro += self.dict_pro[i].replace(raw_sequence,protein)
                    previous = gene            
                if gene != previous:   
                    self.nuc(seq_pro,previous)
                    self.aa(trans_pro,previous)  
                    statistics += previous+','+str(seq_pro.count('>'))+'\n'
                    seq_pro = ''
                    trans_pro = ''
                    seq_pro += self.dict_pro[i]
                    raw_sequence = self.dict_pro[i].split('\n')[1] 
                    trim_sequence = self.trim_ter(raw_sequence)  
                    protein = _translate_str(trim_sequence, table) 
                    trans_pro += self.dict_pro[i].replace(raw_sequence,protein)
                    previous = gene  
            except StopIteration: 
                self.nuc(seq_pro,gene)
                self.aa(trans_pro,gene)
                statistics += gene+','+str(seq_pro.count('>'))+'\n'
                break
        return statistics            
    def sort_rRNA(self):
        list_rRNA = sorted(list(self.dict_rRNA.keys()))
        previous = ''
        seq_rRNA = ''
        it = iter(list_rRNA)
        statistics = ''
        while True:
            try:
                i = next(it)
                gene = re.match('^[^>]+',i).group()
                if gene == previous or previous == '':
                    seq_rRNA += self.dict_rRNA[i]
                    previous = gene                
                if gene != previous:
                    self.rRNA(seq_rRNA,previous)
                    statistics += previous+','+str(seq_rRNA.count('>'))+'\n'
                    seq_rRNA = ''
                    seq_rRNA += self.dict_rRNA[i]
                    previous = re.match('^[^>]+',i).group()
            except StopIteration: 
                self.rRNA(seq_rRNA,gene)
                statistics += gene+','+str(seq_rRNA.count('>'))+'\n'
                break
        return statistics
    def sort_tRNA(self):
        list_tRNA = sorted(list(self.dict_tRNA.keys()))
        previous = ''
        seq_tRNA = ''
        it = iter(list_tRNA)
        statistics = ''
        while True:
            try:
                i = next(it)
                gene = re.match('^[^>]+',i).group()
                if gene == previous or previous == '':
                    seq_tRNA += self.dict_tRNA[i]
                    previous = gene            
                if gene != previous:
                    self.tRNA(seq_tRNA,previous)
                    statistics += previous+','+str(seq_tRNA.count('>'))+'\n'
                    seq_tRNA = ''
                    seq_tRNA += self.dict_tRNA[i]
                    previous = re.match('^[^>]+',i).group()
            except StopIteration: 
                self.tRNA(seq_tRNA,gene)
                statistics += gene+','+str(seq_tRNA.count('>'))+'\n'
                break
        return statistics            
    def individual_genes(self):
        self.table_num = myargs.codontable
        os.chdir(scripts_path+'/output')
        self.statistics = 'Gene,specie number\n'
        self.statistics += self.sort_pro()    
        self.statistics += self.sort_rRNA()
        self.statistics += self.sort_tRNA()
    def store(self): 
        list_name = sorted(list(self.dict_name.keys()))
        self.exception += 'exception species:'+self.error_species+'\n'+self.error_gb.strip(' ')
        str1 = ''
        if myargs.name:
            for i in list_name:
                str1 += i + '\t' + self.dict_name[i] + '\n'
            with open('./files/name.txt','w') as f:
                f.write(str1)
        if myargs.stat:  
            with open('./files/statistics.csv','w') as f:
                f.write(self.statistics) 
        with open('./files/error_report.txt','w') as f1:
            f1.write(self.exception)
    def save_seq(self):
        if myargs.geom:
            with open('./files/complete_seq.fas','w') as f:
                f.write(self.complete_seq)
    def save_order(self):
        if myargs.order:   
            with open('./files/linear_order.txt','w') as f:
                f.write(self.linear_order) 
    def save_files(self):
        if myargs.csv:
            with open('./files/PCGs.csv','w') as f: 
                f.write(self.pro_seq.replace('\t',','))
            with open('./files/rRNA.csv','w') as f1:
                f1.write(self.rRNA_seq.replace('\t',','))
            with open('./files/tRNA.csv','w') as f2:
                f2.write(self.tRNA_seq.replace('\t',','))
        if myargs.tRNA:
            with open('./files/tRNA.fas','w') as f4:
                f4.write(self.tRNA_fas)
    def save_stat(self):
        if myargs.table:
            list_geom = [value for (key,value) in sorted(self.dict_geom.items())]
            list_start = [value for (key,value) in sorted(self.dict_start.items())]
            list_stop = [value for (key,value) in sorted(self.dict_stop.items())]
            list_PCGs = [value for (key,value) in sorted(self.dict_PCG.items())]
            list_RNA = [value for (key,value) in sorted(self.dict_RNA.items())]
            with open('./files/genome_tbl.csv','w') as f1:
                prefix = 'Species,Abbreviations,GeneBank accesion no.,Full length (bp),A+T content (%)\n'
                f1.write(prefix+'\n'.join(list_geom))
            with open('./files/gene_tbl.csv','w') as f2:
                headers = 'Gene,Species\n,'+','.join(self.list_abbre)+'\n'
                prefix_PCG = 'Length of PCGs (bp)\n'
                prefix_rRNA = 'Length of rRNA genes (bp)\n'
                prefix_ini = 'Putative start codon\n'
                prefix_ter = 'Putative terminal codon\n'
                f2.write(headers+prefix_PCG+'\n'.join(list_PCGs)+'\n'+\
                         prefix_rRNA+'\n'.join(list_RNA)+'\n'+\
                         prefix_ini+'\n'.join(list_start)+'\n'+\
                         prefix_ter+'\n'.join(list_stop))
    def specie_select(self):
        if myargs.prefer != []:
            for j in myargs.prefer:
                with open('./files/'+j+'.csv','w') as f3:
                    f3.write(self.dict_spe_stat[j])
    def files(self):
        try:              
            os.mkdir('./files')
        except FileExistsError:
            pass
        self.save_order()
        self.store()
        self.save_seq()
        self.save_files()
        self.save_stat()
        self.specie_select()
    def save(self):
        self.output_from_file()
        def remove_dir(path):
            filelist=os.listdir(path)  
            for f in filelist:
                filepath = os.path.join(path, f )  
                if os.path.isfile(filepath):  
                    os.remove(filepath)  
                    print(filepath+" removed!")
                elif os.path.isdir(filepath):  
                    shutil.rmtree(filepath,True)
                    print("dir "+filepath+" removed!")
        try:
            os.mkdir(scripts_path+'/output')
        except FileExistsError:
            remove_dir(scripts_path+'/output')
            pass
        self.individual_genes()
        self.files()        
if __name__ == '__main__':
    from Bio.Seq import _translate_str
    from Bio.Data import CodonTable
    import re,os,shutil,sys,argparse
    scripts_path = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
    def parameter():
        scripts_path=os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawDescriptionHelpFormatter,\
                prog = 'gb_parser.py',\
                description = 'Parse GenBank file to extract interested information',\
                epilog = r'''
examples:
You can omit '-f' and '-r' under the premise of a GenBank file named 'sequences.gb' and a replace file named 'replace.txt' are placed in the dir of the scripts:
    【muti-prefer species】 python D:\parseGB\bin\gb_parser.py -c 9 -p NC_030050 -p NC_016950 -p JQ038228 -aa -nuc -rRNA -tRNA -geom -table -order -name -stat -csv 
    【muti-excluded species】python D:\parseGB\bin\gb_parser.py -c 9 -e NC_030050 -e NC_016950 -e JQ038228 -aa -nuc -rRNA -tRNA -geom -table -order -name -stat -csv 
Specify GenBank file and replace file:
    【only output AA sequence】 python D:\parseGB\bin\gb_parser.py -c 9 -f C:\users\sequences.gb -r C:\users\replace.txt -aa
    【specify the number of PCGs plus rRNAs】 python D:\parseGB\bin\gb_parser.py -c 9 -n 15 -f C:\users\sequences.gb -r C:\users\replace.txt -aa -nuc
    【specify type of the species name】 python D:\parseGB\bin\gb_parser.py -c 9 -t 2 -f C:\users\sequences.gb -r C:\users\replace.txt -table -order
    【use default codon table(1)】  python D:\parseGB\bin\gb_parser.py -t 2 -f C:\users\sequences.gb -r C:\users\replace.txt -table -order          
                ''')
        parser.add_argument('-f',dest ='file',help='input GenBank file',type=argparse.FileType('r'),default=scripts_path+'/sequences.gb')
        parser.add_argument('-n',dest ='num',help='the amount of the protein plus rRNA genes among mtDNA',\
                            choices=[14,15],default=14,type=int) 
        parser.add_argument('-r',dest='replace',help='the replace file with unified gene names involved in',type=argparse.FileType('r'),default=scripts_path+'/replace.txt')
        parser.add_argument('-t',dest='type',help='''**** choose a type of the header of the fasta file ****
                            【1】by latin,   for instance:>Benedenia_hoshinai (default)                            
                            【2】by Genbank, for instance:>NC_014591                            
                            【3】by logogram,for instance:>B_hoshinai                            
                            【4】by latin_gb,for instance:>Benedenia_hoshinai_NC_014591''',\
                            type=int,choices=[1,2,3,4],default=1)
        parser.add_argument('-c',dest='codontable',\
                            help='''choose a codon table!【1(default)|2|3|4|5|6|9|10|11|12|13|14|15|16|21|22|23】
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
        parser.add_argument('-e',dest='exclude',help='the gb number of the excluded species',\
                            action='append',default=[])
        parser.add_argument('-p',dest='prefer',help='the gb number of the species that we prefer to its genome statistics',\
                            action='append',default=[])
        parser.add_argument('-aa',dest='AA',help='generate AA sequence files (fasta) of individual PCGs',\
                            default=False,action='store_true')
        parser.add_argument('-nuc',dest='NUC',help='generate nucleotide sequence files (fasta) of individual PCGs',\
                            default=False,action='store_true')
        parser.add_argument('-rRNA',dest='rRNA',help='generate nucleotide sequence files (fasta) of individual rRNAs',\
                            default=False,action='store_true')
        parser.add_argument('-tRNA',dest='tRNA',help='generate nucleotide sequence files (fasta) of individual tRNAs',\
                            default=False,action='store_true')
        parser.add_argument('-geom',dest='geom',help='generate nucleotide sequence files (fasta) of the whole genome',\
                            default=False,action='store_true')
        parser.add_argument('-table',dest='table',help='generate statistics file of the whole genome and individual genes',\
                            default=False,action='store_true')
        parser.add_argument('-order',dest='order',help='generate a file with mt genes order involved in',\
                            default=False,action='store_true')
        parser.add_argument('-name',dest='name',help='generate a file of detailed name so as to edit phylogenetic tree by iTOl',\
                            default=False,action='store_true')
        parser.add_argument('-stat',dest='stat',help='generate statistics file about the inclusive species of individual genes',\
                            default=False,action='store_true')
        parser.add_argument('-csv',dest='csv',help='generate csv files about the nucleotide sequence of PCGs, rRNAs and tRNAs',\
                            default=False,action='store_true')
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
    def main():
        mymain = Save_files()
        mymain.save()
    main()
    print('completed!')


        


              
              
    
    
        
        
    
        
        
    
