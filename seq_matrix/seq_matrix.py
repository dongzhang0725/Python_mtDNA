#coding = utf-8
#!/usr/bin/env python
'''模拟sequence matrix程序，实现其部分功能
2016.3.29：新增span匹配结束位置
2016.4.1：新增生成phy和nxs格式文件
2016.4.2：优化了partition文件,partitionfinder的基因索引增加了顺序，可以方便贝叶斯设置分区。
2016.4.13：新增了识别不同文件序列数目差别的功能
2016.5.19：改为由dos窗口输入命令来使用'''

__date__  =  '2016年3月27日'
__author__  =  'zhang dong;708986950@qq.com'

def get_results():
    def parameter():
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawTextHelpFormatter,\
                prog = 'seq_matrix.py',\
                description = 'Concatenated muti-sequences into one file',\
                epilog = r'''
    The output file will be deposited in the directory of %(prog)s
    
    examples:
            1.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -f C:\Users\Administrator\Desktop\scripts\partitions -phy
            2.python C:\Users\Administrator\Desktop\scripts\seq_matrix.py -phy -nex -paml -fas -axt -stat -part   【On condition that there is a 'partitions' folder in the directory of %(prog)s】 
                ''')
        parser.add_argument('-f',dest ='folder',help='input folder',\
                            default=os.path.dirname(sys.argv[0])+'./partitions')
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
    filename = list(map(lambda x:myargs.folder+'/'+x,os.listdir(myargs.folder)))  #得到fas文件名的列表
    dict_species = {}  
    dict_statistics = dict(prefix = 'taxon' ) #统计基因
    partition_style = '【partitionfinder style】\n'
    bayes_style = '【bayes style】\n'
    partition_name = '' #容纳贝叶斯要用到的分区名字
    count = 0
    for each in filename:
        count += 1
        def each_file():
            with open(each) as f:
                count_num = 0   #记录剩下各文件的序列数目
                list_spe = []
                line = f.readline()
                dict_statistics['prefix'] += '\t'+os.path.basename(each)  #表格第一行
                while line != '':
                    spe_key = line.strip().replace('>','')
                    line = f.readline()  #读到序列一行
                    seq = ''
                    while not line.startswith('>') and line != '':
                        seq += line.strip().replace(' ','')
                        line = f.readline()              
                    if count == 1:  #第一次生成字典
                        dict_species[spe_key] = seq
                        lenth = len(seq)  #每个基因序列长度
                        indels = seq.count('-')
                        dict_statistics[spe_key] = spe_key+'\t'+str(lenth)+' ('+str(indels)+' indels)'
                    else:
                        count_num += 1
                        list_spe.append(spe_key)
                        try:                
                            dict_species[spe_key] += seq  #增加序列
                        except KeyError as reason:
                            print('''ERROR:Can't find %s in 【%s】 which exsisted in 【%s】!'''%(reason,filename[0],each))
                        lenth = len(seq)  #每个基因序列长度
                        indels = seq.count('-')  #插入缺失个数
                        dict_statistics[spe_key] += '\t'+str(lenth)+' ('+str(indels)+' indels)'
            if count_num != len(list(dict_species.keys())) and count_num != 0:
                lack = [i for i in list(dict_species.keys()) if i not in list_spe]
                print('''ERROR:Can't find %s in 【%s】'''%(str(lack),each))
            return dict_species,dict_statistics,seq,spe_key
        dict_species,dict_statistics,seq,spe_key = each_file()
        span = re.search(seq + '$',dict_species[spe_key]).span() #匹配结束位置
        partition_style += os.path.basename(each).split('.')[0] + '=' + str(span[0]+1) + '-' + str(span[1]) + ';\n'
        bayes_style += 'charset ' + os.path.basename(each).split('.')[0] + '=' + str(span[0]+1) + '-' + str(span[1]) + ';\n'
        partition_name += os.path.basename(each).split('.')[0]+','
        print('%s done!'%os.path.basename(each))
    partition_name = 'partition Names = %s:'%str(count)+partition_name.strip(',')+';\nset partition=Names;'
    def complete():  #完善字典
        dict_statistics['prefix'] += '\tTotal lenth\tNo of charsets\n'
        list_keys = sorted(list(dict_species.keys()))  #不能用dict_statistics，因为有prefix
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
            def align(seq):  #给paml_file对齐
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
        return statistics,file,phy_file,nxs_file+';\nEND;\n',paml_file,axt_file  #加上尾巴
    statistics,file,phy_file,nxs_file,paml_file,axt_file = complete()
    def save():
        if myargs.axt:
            with open(os.path.dirname(sys.argv[0])+'./append.axt','w') as f1:
                f1.write(axt_file)
        if myargs.fas:
            with open(os.path.dirname(sys.argv[0])+'./append.fas','w') as f2:
                f2.write(file)
        if myargs.stat:
            with open(os.path.dirname(sys.argv[0])+'./statistics.csv','w') as f3:
                f3.write(statistics.replace('\t',','))
        if myargs.partition:
            with open(os.path.dirname(sys.argv[0])+'./partition.txt','w') as f4:
                f4.write(partition_style + bayes_style+partition_name)
        if myargs.phy:
            with open(os.path.dirname(sys.argv[0])+'./append.phy','w') as f5:
                f5.write(phy_file)
        if myargs.nex:
            with open(os.path.dirname(sys.argv[0])+'./append.nex','w') as f6:
                f6.write(nxs_file)
        if myargs.paml:
            with open(os.path.dirname(sys.argv[0])+'./append.PML','w') as f7:
                f7.write(paml_file)
    save()
if __name__ == '__main__':   
    import os,re,argparse,sys
    get_results()    
    print('completed!')
