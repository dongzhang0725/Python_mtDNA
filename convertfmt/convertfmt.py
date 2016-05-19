#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年5月18日'
__author__  =  'zhang dong;708986950@qq.com'

def judge(seq):
    DNA = re.search(r'[ATCG]{10}',seq,re.I)  
    PROTEIN = re.search(r'[GAVLIFWYDHNEKQMRSTCP]{10}',seq,re.I)
    if DNA:
        pattern = 'DNA'
    elif PROTEIN:
        pattern = 'PROTEIN'
    else:
        print('ERROR!neither nucleotide nor protein sequences!')
    return pattern    
def sort_seq(seq):
    list_seq = re.findall(r'(.{60})',seq)   #得到60个序列一个列表，但是最后多余的不包括
    remainder = len(seq)%60  #求出余数
    if remainder == 0:
        align_seq = '\n'.join(list_seq) + '\n'
    else:
        align_seq = '\n'.join(list_seq) +'\n' + seq[-remainder:] + '\n'
    return align_seq
def save(phy,nex,paml,axt,statistics,inputfile,myargs):
    if myargs.phy:
        with open(inputfile.split('.')[0]+'.phy','w') as f1:
            f1.write(phy)
    if myargs.nex:
        with open(inputfile.split('.')[0]+'.nex','w') as f2:
            f2.write(nex)
    if myargs.paml:
        with open(inputfile.split('.')[0]+'.PML','w') as f3:
            f3.write(paml)
    if myargs.axt:
        with open(inputfile.split('.')[0]+'.axt','w') as f4:
            f4.write(axt)
    if myargs.stat:
        with open(os.path.dirname(inputfile)+'./statistics.csv','w') as f5:
            f5.write(statistics)  
def parameter():
    parser = argparse.ArgumentParser(\
            formatter_class=argparse.RawTextHelpFormatter,\
            prog = 'convertfmt.py',\
            description = 'Convert fasta to selected format 【phylip|nexus|paml|axt】',\
            epilog = r'''
examples:
        1.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f C:\Users\Administrator\Desktop\scripts\demo.fasta -phy
        2.python C:\Users\Administrator\Desktop\scripts\convertfmt.py -f demo.fasta -phy -nex -paml -axt -stat 
            ''')
    parser.add_argument('-f',dest ='file',help='input fasta file',required=True)
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
    myargs = parser.parse_args(sys.argv[1:])
    return myargs
def main():
    myargs = parameter()
    with open(myargs.file) as f:
        line = f.readline()
        phy = ''
        nex = ''
        paml = ''
        axt_name = ''
        axt_seq = ''
        statistics = 'Name,Lenth\n'
        count = 1
        while line != '':
            while not line.startswith('>'):  #忽略fas文件前面的header
                line = f.readline()
            name = line.strip('>').strip('\n').replace(' ','_') #将空格换为下划线，方便软件运行
            seq = ''
            line = f.readline()  #读到序列一行
            while not line.startswith('>') and line != '':
                seq += line.strip().replace(' ','')                    
                line = f.readline()
            statistics += name + ',' + str(len(seq)) + '\n'
            phy += name + ' ' + seq + '\n'
            nex += '['+str(count) +'] ' + name + ' ' + seq + '\n'
            paml += name + '\n' + sort_seq(seq) + '\n'
            axt_name += name.replace('_',' ') + '-'
            axt_seq += seq + '\n'
            count += 1
        pattern = judge(seq)
        phy = ' '+str(count - 1)+' '+str(len(seq))+'\n' + phy  
        nex = '#NEXUS\nBEGIN DATA;\ndimensions ntax=%s nchar=%s;\nformat missing=?\ndatatype=%s gap= -;\n\nmatrix\n'\
              %(str(count - 1),str(len(seq)),pattern) + nex + ';\nEND;\n'
        paml = str(count - 1)+'  '+str(len(seq))+'\n\n' + paml
        axt = axt_name.strip('-') + '\n' + axt_seq
    save(phy,nex,paml,axt,statistics,myargs.file,myargs)
 
    
if __name__ == '__main__':
    import re,argparse,sys,os
    main()
    print('completed!')