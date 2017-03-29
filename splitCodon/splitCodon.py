'''切割导入的蛋白基因序列文件，按密码子1、2、3位分别存储文件
将该脚本与序列的fas文件放在一起，然后双击该脚本即可
序列名字里面的特殊字符会被替换'''


class Commander(object):

    def __init__(self, file):
        self.file = file
        self.readFas()
        self.split()
        self.eachSite()
        self.saveFile()

    def readFas(self):
        self.dict_taxon = {}
        with open(self.file) as f2:
            line = f2.readline()
            while line != "":
                while not line.startswith('>'):
                    line = f2.readline()
                fas_name = line.strip().replace(">", "")
                # 替换名字里面的不识别字符
                fas_name = re.sub(
                    r'\||[(]|[)]|"|:|[#]|[@]|\$|[%]|[&]|\*|[!]|~|[?]|>|<|[\]|\'|`|/|[^]|[[]|[]]|{|}|\.|,|;|-', '_', fas_name)
                fas_seq = ""
                line = f2.readline()
                while not line.startswith('>') and line != "":
                    fas_seq += line.strip().replace(" ",
                                                    "").replace("\t", "")
                    line = f2.readline()
                self.dict_taxon[fas_name] = fas_seq

    def split(self):
        self.dict_codsite = {}  # 得到DL0,DL1,DL2
        list_keys = list(self.dict_taxon.keys())
        for i in list_keys:
            lenth = len(self.dict_taxon[i])
            for j in range(lenth):  # 这里1,2,0;0代表第三位
                remainder = (j + 1) % 3
                try:
                    self.dict_codsite[
                        i + str(remainder)] += self.dict_taxon[i][j]
                except KeyError:
                    self.dict_codsite[
                        i + str(remainder)] = self.dict_taxon[i][j]

    def eachSite(self):
        list_keys = list(self.dict_taxon.keys())
        self.first, self.second, self.third = "", "", ""
        for i in list_keys:
            self.first += ">" + i + "\n" + self.dict_codsite[i + "1"] + "\n"
            self.second += ">" + i + "\n" + self.dict_codsite[i + "2"] + "\n"
            self.third += ">" + i + "\n" + self.dict_codsite[i + "0"] + "\n"

    def saveFile(self):
        output_prefix = os.path.splitext(self.file)[0] if os.path.dirname(
            self.file) else "./" + os.path.splitext(self.file)[0]
        with open(output_prefix + "_codon1.fasta", "w") as f:
            f.write(self.first)
        with open(output_prefix + "_codon2.fasta", "w") as f1:
            f1.write(self.second)
        with open(output_prefix + "_codon3.fasta", "w") as f2:
            f2.write(self.third)

if __name__ == "__main__":
    import re
    import os
    import sys
    import argparse
    import glob

    listFiles = glob.glob(os.getcwd() + os.sep + "*.fas")

    def parameter():
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='splitCodon.py',
            description='Split a file acording to the three codon site',
            epilog=r'''Usage example:
python C:\Users\Desktop\splitCodon.py C:\Users\Desktop\demo.fasta
              ''')
        parser.add_argument(
            "files", help='input file', default=listFiles, nargs='*')
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
    for i in myargs.files:
        Commander(i)
    print("Done!")
