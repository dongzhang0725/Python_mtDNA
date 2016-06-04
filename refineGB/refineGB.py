#coding = utf-8
#!/usr/bin/env python

__date__  =  '2016年6月1日'
__author__  =  'zhang dong;708986950@qq.com'
__version__ = 'python3.4.3'

def is_feature_start(line):   
    return line and line[5] != ' '
def source(individual_gb,line,f):
    line = f.readline() 
    assert line.startswith('     source'),line
    individual_gb += line
    line = f.readline() 
    while not is_feature_start(line):
        individual_gb += line  
        if 'isolate' in line:
            value = '_' + line.strip()[1:].split('=')[1].strip('"')
        else:
            value = ''
        line = f.readline()
    return individual_gb,line,value
def get_value(feature_content,f,line,value):
    attribute_prefix = 21*' ' + '/'
    feature_content += line
    line = f.readline()  
    while (not line.startswith(attribute_prefix) and not is_feature_start(line)): 
        feature_content += line 
        value += line.strip()  
        line = f.readline()  
    fullvalue = value.strip('"') 
    return fullvalue,line,feature_content
def read_feature(f,line,feature_content):
    feature_content += line 
    feature = line.split()   
    assert feature
    line = f.readline()  
    props = {} 
    while not is_feature_start(line):  
        assert 2 == len(line.split('=')),line.split('=')
        key,value = line.strip()[1:].split('=')  
        fullvalue,line,feature_content = get_value(feature_content,f,line,value) 
        props[key] = fullvalue  
    feature.append(props)  
    return feature,line,feature_content
def next_item(f,line):   
    while not line.startswith('ORIGIN') and not line.startswith('BASE'):  
        assert is_feature_start(line),line 
        feature_content = ''  
        feature,line,feature_content = read_feature(f,line,feature_content)     
        yield feature,feature_content,line
def substitute():
    dict_repl = {}
    try:
        with open ('replace.txt') as f:
            for each in f:
                if each != '\n':
                    former,new = each.strip().split('-->')
                    dict_repl[former] = new
    except OSError as reason:
        print('name not replaced,because:'+str(reason))
    return dict_repl
    
def replace(dict_replace,old_name):
    try:
        old_name = dict_replace[old_name]
    except KeyError:
        pass
    return old_name
def judge(new_name,values,gb_num,file):
    if new_name == 'L' or new_name == 'S':
        if re.search(r'(?<=[^1-9a-z_])(Leu1|CUA|CUN|tag|L1|trnL1)(?=[^1-9a-z_])',values,re.I): 
            new_name = 'L1'
        elif re.search(r'(?<=[^1-9a-z_])(Leu2|UUA|UUR|taa|L2|trnL2)(?=[^1-9a-z_])',values,re.I):
            new_name = 'L2'
        elif re.search(r'(?<=[^1-9a-z_])(Ser2|UCA|UCN|tga|S2|trnS2)(?=[^1-9a-z_])',values,re.I):
            new_name = 'S2'
        elif re.search(r'(?<=[^1-9a-z_])(Ser1|AGC|AGN|AGY|gct|tct|S1|trnS1)(?=[^1-9a-z_])',values,re.I):
            new_name = 'S1'
        else:
            position = '【'+'\t'.join(values.split('\n')[0].split())+'】'
            print('Ambiguous annotation about S1, S2, L1 and L2 in %s for %s within %s\n'%(position,gb_num,file))
    else:
        new_name = new_name
    return new_name        
def get_item(individual_gb,f,line,gb_num,myargs,file): 
    item = []
    dict_replace = substitute()
    generator_item = next_item(f,line)  
    feature,feature_content,line = next(generator_item)
    while True:
        try:    
            if feature[0] == 'gene':
                try: 
                    old_name = feature[2]['gene'] 
                    new_name = replace(dict_replace,old_name)                
                    previous_feature = feature
                    previous_content = feature_content
                    item.append(feature)
                    feature,feature_content,line = next(generator_item) 
                    if feature[0] == 'tRNA':
                        new_name = judge(new_name,feature_content,gb_num,file)
                    individual_gb += previous_content.replace(old_name,new_name) 
                    if feature[1] == previous_feature[1]:
                        individual_gb += feature_content
                    else:
                        print('Error：%s\t%s are not same as previous gene annotation within %s for %s!'%(feature[0],feature[1],gb_num,file))
                except KeyError: 
                    previous_feature = feature
                    previous_content = feature_content
                    item.append(feature)
                    feature,feature_content,line = next(generator_item)
                    if feature[1] == previous_feature[1]:
                        try: 
                            old_name = feature[2]['gene'] 
                            new_name = replace(dict_replace,old_name)
                            if feature[0] == 'tRNA':
                                new_name = judge(new_name,feature_content,gb_num,file)
                            previous_content += 21*' '+'/gene="%s"\n'%new_name
                            individual_gb += previous_content
                        except KeyError:
                            old_name = feature[2]['product'] 
                            new_name = replace(dict_replace,old_name)
                            if feature[0] == 'tRNA':
                                new_name = judge(new_name,feature_content,gb_num,file)
                            previous_content += 21*' '+'/gene="%s"\n'%new_name
                            individual_gb += previous_content
                        individual_gb += feature_content 
                    else:
                        print('Error：%s\t%s are not same as previous gene annotation within %s for %s!'%(feature[0],feature[1],gb_num,file))
            else: 
                try: 
                    old_name = feature[2]['gene'] 
                    new_name = replace(dict_replace,old_name)
                    if feature[0] == 'tRNA':
                        new_name = judge(new_name,feature_content,gb_num,file)
                    previous_content = 5*' ' + 'gene' + 12*' ' + feature[1] + '\n' + 21*' ' + '/gene="%s"\n'%new_name
                    individual_gb += previous_content + feature_content
                except KeyError:
                    try: 
                        old_name = feature[2]['product'] 
                        new_name = replace(dict_replace,old_name)
                        if feature[0] == 'tRNA':
                            new_name = judge(new_name,feature_content,gb_num,file)
                        previous_content = 5*' ' + 'gene' + 12*' ' + feature[1] + '\n' + 21*' ' + '/gene="%s"\n'%new_name
                        individual_gb += previous_content + feature_content  
                    except KeyError:
                        previous_content = 5*' ' + 'gene' + 12*' ' + feature[1] + '\n' + 21*' ' + '/gene=NCR\n'
                        individual_gb += previous_content + feature_content
                        print('Warning： when handle %s in %s for %s'%(feature,gb_num,file))          
            item.append(feature)     
            last_feature = feature 
            feature,feature_content,line = next(generator_item)
            def position(subject):
                ini,ter = subject.split('..')
                return ini.strip('<'),ter
            last_ter = position(last_feature[1])[1]
            now_ini = position(feature[1])[0] 
            if (int(now_ini) - int(last_ter)) >= myargs.num:
                individual_gb += 5*' '+'gene'+12*' '+str(int(last_ter)+1)+'..'+str(int(now_ini)-1)+'\n'+21*' '+'/gene=NCR\n'
        except StopIteration: 
            break
    return item,individual_gb,line        
def get_sequence(individual_gb,f,line):
    individual_gb += line
    while not line.startswith('//'):
        line = f.readline()
        individual_gb += line
    return individual_gb,line
def get_ids(src,line):
    while not line.startswith('LOCUS'):  
        line = src.readline()  
    gb_num = line.split()[1]
    assert gb_num != '',gb_num
    return gb_num
def get_latin(individual_gb,src,line):
    while not line.startswith('  ORGANISM'):
        line = src.readline()
        individual_gb += line
    name = re.search(r'  ORGANISM  (.+)\n',line).group(1)  
    return individual_gb,name.replace(' ','_'),line
def main(myargs):    
    def run(file,myargs):
        with open(file) as f:
            list_latin = []
            line = f.readline()  
            assert line.startswith('LOCUS'),line        
            while line != '':
                while not line.startswith('//') and line != '': 
                    individual_gb = line
                    gb_num = get_ids(f,line)
                    individual_gb,latin,line = get_latin(individual_gb,f,line)
                    while not line.startswith('FEATURES'): 
                        line = f.readline()
                        individual_gb += line 
                    individual_gb,line,value = source(individual_gb,line,f) 
                    latin = latin + value.replace(' ','_')                
                    if latin not in list_latin:
                        item,individual_gb,line = get_item(individual_gb,f,line,gb_num,myargs,file)
                        individual_gb,line = get_sequence(individual_gb,f,line)
                        def save():                    
                            with open(myargs.out+'/'+latin+'.gb','w') as f1:
                                f1.write(individual_gb)
                        save()
                    else:
                        while not line.startswith('//') and line != '':
                            line = f.readline()
                    list_latin.append(latin)
                while not line.startswith('LOCUS') and line != '':
                    line = f.readline() 
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
    #remove_dir(myargs.out)
    if os.path.isdir(myargs.file):
        files = os.listdir(myargs.file)
        for each_file in files:
            run(myargs.file+'/'+each_file,myargs)
    elif os.path.isfile(myargs.file): 
        run(myargs.file,myargs)
    else:
        print('input error!')
if __name__ == '__main__':
    import re,os,shutil,argparse,sys    
    def parameter():
        parser = argparse.ArgumentParser(\
                formatter_class=argparse.RawTextHelpFormatter,\
                prog = 'refineGB.py',\
                description = 'Refine GenBank file to standard format.',\
                epilog = r'''
examples:
    1.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\scripts\demo.gb -n 300 -o C:\Users\Desktop\myfolder
    2.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\gbfolder -o C:\Users\Desktop\myfolder
                ''')
        parser.add_argument('-f',dest ='file',help='input GenBank file or folder',required=True)
        parser.add_argument('-n',dest ='num',help='define minimum of the length of the NCR',\
                            default=150,type=int) 
        parser.add_argument('-o',dest='out',help='folder of the out file',required=True)
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    main(parameter())
    print('completed!')
