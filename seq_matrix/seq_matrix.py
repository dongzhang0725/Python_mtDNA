#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年3月27日'
__author__  =  'zhang dong;708986950@qq.com'

def get_results():
    scripts_path = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else '.'
    def parameter():
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawTextHelpFormatter,\
                prog = 'seq_matrix.py',\
                description = 'Concatenated muti-sequences into one file',\
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
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
    filename = list(map(lambda x:myargs.folder+'/'+x,os.listdir(myargs.folder)))  
    dict_species = {}  
    dict_statistics = dict(prefix = 'taxon' )
    partition_style = '【partitionfinder style】\n'
    bayes_style = '【bayes style】\n'
    partition_name = '' 
    count = 0
    for each in filename:
        count += 1
        def each_file():
            with open(each) as f:
                count_num = 0 
                list_spe = []
                line = f.readline()
                dict_statistics['prefix'] += '\t'+os.path.basename(each)  
                while line != '':
                    spe_key = line.strip().replace('>','')
                    line = f.readline()  
                    seq = ''
                    while not line.startswith('>') and line != '':
                        seq += line.strip().replace(' ','')
                        line = f.readline()              
                    if count == 1:  
                        dict_species[spe_key] = seq
                        lenth = len(seq) 
                        indels = seq.count('-')
                        dict_statistics[spe_key] = spe_key+'\t'+str(lenth)+' ('+str(indels)+' indels)'
                    else:
                        count_num += 1
                        list_spe.append(spe_key)
                        try:                
                            dict_species[spe_key] += seq 
                        except KeyError as reason:
                            print('''ERROR:Can't find %s in 【%s】 which exsisted in 【%s】!'''%(reason,filename[0],each))
                        lenth = len(seq)  
                        indels = seq.count('-')  
                        dict_statistics[spe_key] += '\t'+str(lenth)+' ('+str(indels)+' indels)'
            if count_num != len(list(dict_species.keys())) and count_num != 0:
                lack = [i for i in list(dict_species.keys()) if i not in list_spe]
                print('''ERROR:Can't find %s in 【%s】'''%(str(lack),each))
            return dict_species,dict_statistics,seq,spe_key
        dict_species,dict_statistics,seq,spe_key = each_file()
        span = re.search(seq + '$',dict_species[spe_key]).span()
        partition_style += os.path.basename(each).split('.')[0] + '=' + str(span[0]+1) + '-' + str(span[1]) + ';\n'
        bayes_style += 'charset ' + os.path.basename(each).split('.')[0] + '=' + str(span[0]+1) + '-' + str(span[1]) + ';\n'
        partition_name += os.path.basename(each).split('.')[0]+','
        print('%s done!'%os.path.basename(each))
    partition_name = 'partition Names = %s:'%str(count)+partition_name.strip(',')+';\nset partition=Names;'
    def complete():  
        dict_statistics['prefix'] += '\tTotal lenth\tNo of charsets\n'
        list_keys = sorted(list(dict_species.keys())) 
        def judge(seq):
            DNA = re.search(r'[ATCG]{20}',seq,re.I)  
            PROTEIN = re.search(r'[GAVLIFWYDHNEKQMRSTCP]{20}',seq,re.I)
            if DNA:
                pattern = 'DNA'
            elif PROTEIN:
                pattern = 'PROTEIN'
            else:
                print('ERROR!neither nucleotide nor protein sequences!')
            return pattern
        pattern = judge(dict_species[list_keys[-1]])
        file = ''
        phy_file = ' '+str(len(list_keys))+' '+str(len(dict_species[list_keys[-1]])) + '\n'
        nxs_file = '#NEXUS\nBEGIN DATA;\ndimensions ntax=%s nchar=%s;\nformat missing=?\ndatatype=%s gap= -;\n\nmatrix\n'%(str(len(list_keys)),str(len(dict_species[list_keys[-1]])),pattern)
        paml_file = str(len(list_keys))+'  '+str(len(dict_species[list_keys[-1]])) + '\n\n'
        axt_file = '-'.join(list_keys) + '\n'
        statistics = dict_statistics['prefix']
        num = 0
        for i in list_keys:
            num += 1
            dict_statistics[i] += '\t'+str(len(dict_species[i]))+'\t'+str(count)+'\n'
            file += '>'+i + '\n' + dict_species[i] + '\n'
            phy_file += i + ' ' + dict_species[i] + '\n'
            nxs_file += '['+str(num) +'] '+i+' '+dict_species[i]+'\n'
            def align(seq): 
                list_seq = re.findall(r'(.{60})',seq)   
                remainder = len(seq)%60  
                if remainder == 0:
                    align_seq = '\n'.join(list_seq) + '\n'
                else:
                    align_seq = '\n'.join(list_seq) +'\n' + seq[-remainder:] + '\n'
                return align_seq
            paml_file += i + '\n' + align(dict_species[i]) + '\n'
            axt_file += dict_species[i] + '\n'
            statistics += dict_statistics[i]
        return statistics,file,phy_file,nxs_file+';\nEND;\n',paml_file,axt_file 
    statistics,file,phy_file,nxs_file,paml_file,axt_file = complete()
    def save():
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
                f1.write(axt_file)
        if myargs.fas:
            with open(scripts_path+'/seq_matrix_out/append.fas','w') as f2:
                f2.write(file)
        if myargs.stat:
            with open(scripts_path+'/seq_matrix_out/statistics.csv','w') as f3:
                f3.write(statistics.replace('\t',','))
        if myargs.partition:
            with open(scripts_path+'/seq_matrix_out/partition.txt','w') as f4:
                f4.write(partition_style + bayes_style+partition_name)
        if myargs.phy:
            with open(scripts_path+'/seq_matrix_out/append.phy','w') as f5:
                f5.write(phy_file)
        if myargs.nex:
            with open(scripts_path+'/seq_matrix_out/append.nex','w') as f6:
                f6.write(nxs_file)
        if myargs.paml:
            with open(scripts_path+'/seq_matrix_out/append.PML','w') as f7:
                f7.write(paml_file)
    save()
if __name__ == '__main__':   
    import os,re,argparse,sys,shutil
    get_results()    
    print('completed!')
