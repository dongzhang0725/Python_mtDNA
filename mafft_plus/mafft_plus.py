#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年7月30日'
__author__  =  'zhang dong;708986950@qq.com'
__version__ = 'python3.4.3'

class Make_dir(object):
    def remove_dir(self,path):
        filelist=os.listdir(path)  
        for f in filelist:
            filepath = os.path.join( path, f )  
            if os.path.isfile(filepath):  
                os.remove(filepath)  
                print(filepath+" removed!")
            elif os.path.isdir(filepath):  
                shutil.rmtree(filepath,True)
                print("dir "+filepath+" removed!")
    def make_dir(self):
        def make(folder):
            try:
                os.mkdir(folder)
            except FileExistsError:        
                self.remove_dir(folder)
        if myargs.codon:
            make(scripts_path+"/vessel")
            make(scripts_path+"/vessel/AA_sequence")
            make(scripts_path+"/vessel/AA_alignments")
            make(scripts_path+"/codon_alignments")
        else:
            make(scripts_path+"/mafft_out")
        
class Read_fas(object): 
    def __init__(self): 
        self.dict_file = {} 
        self.table = CodonTable.ambiguous_dna_by_id[int(myargs.codontable)]
    def handle(self,file):
        self.dict_fas = {} 
        with open(file) as File:
            line = File.readline()
            while line != '':
                while not line.startswith('>'):  
                    line = File.readline()
                name = line
                seq = ''
                line = File.readline()  
                while not line.startswith('>') and line != '':
                    seq += line.strip().replace(' ','')                    
                    line = File.readline()
                self.dict_fas[name] = seq
    def mapping(self,spe,nuc,pro):
        self.dict_file[self.each_file][spe] = [] 
        num = 1
        for each_aa in pro:
            self.dict_file[self.each_file][spe].append((each_aa,nuc[(num-1)*3:num*3]))
            num += 1
    def trim_ter(self,spe,seq): 
        size = len(seq)
        if size % 3 == 0:
            if _translate_str(seq[-3:], self.table) == "*":
                self.trim_seq = seq[:-3]
            else:
                self.trim_seq = seq
        elif size % 3 == 1:
            print("The length of %s sequence in %s is not the mutiple of three, %d is given\n"%(spe.strip(),self.each_file,size))
            self.trim_seq = seq[:-1]
        elif size % 3 == 2:
            print("The length of %s sequence in %s is not the mutiple of three, %d is given\n"%(spe.strip(),self.each_file,size))
            self.trim_seq = seq[:-2]        
    def translate(self):
        list_keys = sorted(list(self.dict_fas.keys()))
        aa_fas = ""
        for i in list_keys:
            self.trim_ter(i,self.dict_fas[i]) 
            protein = _translate_str(self.trim_seq, self.table) 
            aa_fas += i + protein + os.linesep
            self.mapping(i,self.trim_seq, protein)
        with open(scripts_path+"/vessel/AA_sequence/" + self.each_file,"w") as f:
            f.write(aa_fas)
    def read_fas(self,input_file):
        if os.path.isdir(input_file):
            files = os.listdir(input_file) 
            for self.each_file in files:
                self.handle(input_file+'/'+self.each_file) 
                self.dict_file[self.each_file] = {}  
                self.translate() 
        elif os.path.isfile(input_file): 
            self.each_file = os.path.basename(input_file)
            self.handle(input_file)
            self.dict_file[self.each_file] = {} 
            self.translate() 
        else:
            print('Your input is neither file nor folder!')
    
class Alignment(object):
    def sel_out(self):
        print('''Output format?
     1. Clustal format / Sorted
     2. Clustal format / Input order
     3. Fasta format   / Sorted
     4. Fasta format   / Input order
     5. Phylip format  / Sorted
     6. Phylip format  / Input order''')
        while True:
            try:      
                choice = input()
                if choice == '1':
                    ch_out = ' --clustalout --reorder '
                    break
                elif choice == '2':
                    ch_out = ' --clustalout --inputorder '
                    break
                elif choice == '3':
                    ch_out = ' --reorder '
                    break
                elif choice == '4':
                    ch_out = ' --inputorder '
                    break
                elif choice == '5':
                    ch_out = ' --phylipout --reorder '
                    break
                elif choice == '6':
                    ch_out = ' --phylipout --inputorder '
                    break
                else:
                    raise TypeError
            except TypeError:
                print('ERROR!Please enter 1-6')
        return ch_out
    def sel_strategy(self):
        print('''Strategy?
     1. --auto
     2. FFT-NS-1 (fast)
     3. FFT-NS-2 (default)
     4. G-INS-i  (accurate)
     5. L-INS-i  (accurate)
     6. E-INS-i  (accurate)''')
        while True:
            try:      
                choice = input()
                if choice == '1':
                    strategy = ' --auto'
                    break
                elif choice == '2':
                    strategy = ' --retree 1'
                    break
                elif choice == '3':
                    strategy = ' --retree 2'
                    break
                elif choice == '4':
                    strategy = ' --globalpair --maxiterate 16'
                    break
                elif choice == '5':
                    strategy = ' --localpair --maxiterate 16'
                    break
                elif choice == '6':
                    strategy = ' --genefpair --maxiterate 16'
                    break
                else:
                    raise TypeError
            except TypeError:
                print('ERROR!Please enter 1-6!')   
        return strategy
    
    def add_args(self):
        print('''Additional arguments?
     1. --ep
     2. --op
     3. --kappa
     If not need additional arguments,please press enter directly!''')
        while True:
            try:
                choice = input()
                if choice == '1':
                    arg = ' --ep'
                    break
                elif choice == '2':
                    arg = ' --op'
                    break
                elif choice == '3':
                    arg = ' --kappa'
                    break
                elif choice == '':
                    arg = ''
                    break
                else:
                    raise TypeError
            except TypeError:
                print('ERROR!Please enter 1-3!')
        return arg
    
    def align(self):
        ch_out = self.sel_out()
        strategy = self.sel_strategy()
        arg = self.add_args()
        if myargs.codon: 
            path = scripts_path + '/vessel/AA_sequence'
            list_files = os.listdir(path)
            out_path = scripts_path+"/vessel/AA_alignments/" 
        else:
            path = myargs.file
            out_path = scripts_path+"/mafft_out/"
            if os.path.isdir(path):
                list_files = os.listdir(path)
            elif os.path.isfile(path): 
                list_files = [os.path.basename(path)]
                path = os.path.dirname(path)
            else:
                print('Your input is neither file nor folder!')                 
        for each_fas in list_files:
            align_file = os.path.join(path, each_fas)
            commands = myargs.mafft + arg + strategy + ch_out + '"' + align_file  + \
                       '"' + ' > ' +'"' + out_path + each_fas + '"'
            print(commands)
            os.system(commands)    

class Back_trans(Make_dir,Read_fas,Alignment):
    def locate(self):
        for i in self.aa_align:
            if i != "-":
                mapping = self.list_mapping.pop(0) 
                assert i == mapping[0],i
                self.codon_seq += mapping[1]
            if i == "-":
                self.codon_seq += "---"
        self.codon_seq += "\n"    
    def tocodon(self):
        list_keys = sorted(list(self.dict_fas.keys()))
        self.codon_seq = "" 
        for i in list_keys:   
            self.codon_seq += i
            self.aa_align = self.dict_fas[i] 
            self.list_mapping = self.dict_file[self.each_aa_align][i] 
            self.locate()
        with open(scripts_path+"/codon_alignments/"+self.each_aa_align,"w") as f:
            f.write(self.codon_seq)
    def back_trans(self):
        files = os.listdir(scripts_path+"/vessel/AA_alignments")
        for self.each_aa_align in files:
            self.handle(scripts_path+'/vessel/AA_alignments/'+self.each_aa_align) 
            self.tocodon()
if __name__ == '__main__':
    from Bio.Seq import _translate_str
    from Bio.Data import CodonTable    
    import argparse,sys,os,shutil
    scripts_path=os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
    def parameter():
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawDescriptionHelpFormatter,\
                prog = 'mafft_plus.py',\
                description = 'Add codon alignment and batch run to mafft ',\
                epilog = r'''
    examples:
Normal align (the output file will be deposited in the mafft_out folder of scripts directionary):
    【single file】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta
    【input folder】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align

Codon align (the output file will be deposited in the codon_alignments folder of scripts directionary):
    【single file】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta -table 1 -mafft C:\Users\Desktop\mafft.bat -codon
    【input folder】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align -table 1 -mafft C:\Users\Desktop\mafft.bat -codon   
                ''')
        parser.add_argument('-f',dest ='file',help='input fasta file or folder',default=scripts_path+"/align")
        parser.add_argument('-table',dest='codontable',\
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
                            choices=[1, 2, 3, 4, 5, 6, 7, 8,\
                            9, 10, 11, 12, 13, 14, 15, 16,21,22,23],\
                            default=1,type=int)   
        parser.add_argument('-mafft',dest ='mafft',help='the path of the mafft',\
                            default=scripts_path+"/mafft-win/mafft.bat")
        parser.add_argument('-codon',dest ='codon',help='Boolean, whether codon alignment or not',\
                            default=False,action='store_true')
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
    def main():
        mymain = Back_trans() 
        if myargs.codon:
            mymain.make_dir() 
            mymain.read_fas(myargs.file) 
            mymain.align()
            mymain.back_trans() 
        else:
            mymain.make_dir()
            mymain.align()
        '''
        with open(scripts_path+"/file.txt","w") as f:
            f.write(str(mymain.dict_file))'''
    main()
    print("completed!")
        
