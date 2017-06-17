
class Commander(object):

    def __init__(self, targetFile):
        super(Commander, self).__init__()
        self.targetFile = targetFile
        self.dict_AA = {"F": "Phe",
                        "L": "Leu",
                        "L1": "Leu1",
                        "L2": "Leu2",
                        "I": "Ile",
                        "M": "Met",
                        "V": "Val",
                        "S": "Ser",
                        "S1": "Ser1",
                        "S2": "Ser2",
                        "P": "Pro",
                        "T": "Thr",
                        "A": "Ala",
                        "Y": "Tyr",
                        "H": "His",
                        "Q": "Gln",
                        "N": "Asn",
                        "K": "Lys",
                        "D": "Asp",
                        "E": "Glu",
                        "C": "Cys",
                        "W": "Trp",
                        "R": "Arg",
                        "G": "Gly",
                        "*": "Ter"}
        self.format_mega()
        self.readFile()
        self.saveFile()

    def format_mega(self):
        with open(self.targetFile) as f:
            fileContent = f.read()
        rgx_mega = re.compile(
            r"Domain: Data\s+?(Codon.+)Average# codons=(\d+)", re.I | re.S)
        fileContent = re.sub(r",{2,}", "", fileContent)
        table, self.codonSum = rgx_mega.findall(fileContent)[0]
        col_1 = []
        col_2 = []
        col_3 = []
        col_4 = []
        self.aaSum = 0
        for i in table.split("\n"):
            if not i.startswith("Codon") and not i == "":
                list_i = i.strip().split(",")
                col_1.append(list_i[:3])
                col_2.append(list_i[3:6])
                col_3.append(list_i[6:9])
                col_4.append(list_i[9:])
                self.aaSum += int(col_1[-1][1]
                                  ) if "*" not in col_1[-1][0] else 0
                self.aaSum += int(col_2[-1][1]
                                  ) if "*" not in col_2[-1][0] else 0
                self.aaSum += int(col_3[-1][1]
                                  ) if "*" not in col_3[-1][0] else 0
                self.aaSum += int(col_4[-1][1]
                                  ) if "*" not in col_4[-1][0] else 0
        self.list_mega = col_1 + col_2 + col_3 + col_4

    def leu_ser(self, codon, abbre):
        if codon in ["CUU", "CUC", "CUA", "CUG", "AGU", "AGC", "AGA", "AGG"]:
            return abbre + "1"
        elif codon in ["UUA", "UUG", "UCU", "UCC", "UCA", "UCG"]:
            return abbre + "2"
        else:
            return abbre

    def readFile(self):
        self.csv = "AA,Codon,Count,RSCU,Fill,Equality,%AT,aaRatio\n"
        self.stat = "AA,Count,%\n"
        self.AT_end = 0
        last_abbre = ""
        # for list_line in self.list_mega:
        for list_line in self.list_mega:
            abbre = re.search(r"\((.)\)", list_line[0]).group(1)
            codon = re.sub(r"\((.)\)", "", list_line[0])
            abbre = self.leu_ser(codon, abbre)  # 处理L1、L2
            number = int(list_line[-2])
            if codon[-1] == "U" or codon[-1] == "A":
                self.AT_end += number
            if abbre == last_abbre:
                count += 1
                aaNumber += number
                self.csv = self.csv.strip("\n") + ",\n"
            else:
                count = 1
                if last_abbre != "" and last_abbre != "*":
                    aaRatio = '%.2f' % ((aaNumber / self.aaSum) * 100)
                    self.stat += self.dict_AA[last_abbre] + \
                        "(" + last_abbre + ")" + "," + str(aaNumber) + \
                        "," + aaRatio + "\n"
                    self.csv = self.csv.strip("\n") + ",%s\n" % aaRatio
                aaNumber = number
            ratio = '%.2f' % (int(list_line[1]) * 100 / int(self.codonSum))
            if abbre in list(self.dict_AA.keys()) and abbre != "*":
                self.csv += self.dict_AA[abbre] + "," + codon + "," + \
                    list_line[-2] + "," + list_line[-1] + \
                    "," + str(count) + ",-0.5,%s\n" % ratio
            elif abbre != "*":
                self.csv += abbre + "," + codon + "," + \
                    list_line[-2] + "," + list_line[-1] + \
                    "," + str(count) + ",-0.5,%s\n" % ratio
            last_abbre = abbre
        self.stat += self.dict_AA[last_abbre] + "(" + last_abbre + ")" + "," + \
            str(aaNumber) + ',%.2f' % (aaNumber * 100 / self.aaSum) + \
            "\n"   + "codon end in A or T," + \
            str(self.AT_end) + \
            ",%.2f" % ((self.AT_end / self.aaSum) * 100) + "\n"  + \
            "Total," + str(self.aaSum) + "\n"
        aaRatio = '%.2f' % (aaNumber * 100 / self.aaSum)
        self.csv = self.csv.strip("\n") + ",%s\n" % aaRatio

    def saveFile(self):
        input_path = os.path.dirname(
            self.targetFile) if os.path.dirname(
            self.targetFile) else '.'
        base = os.path.splitext(os.path.basename(self.targetFile))[0]
        with open(input_path + os.sep + "%s_stack.csv" % base, "w") as f:
            f.write(self.csv)
        with open(input_path + os.sep + "%s_stat.csv" % base, "w") as f1:
            f1.write(self.stat)
if __name__ == "__main__":
    import re
    import os
    import sys
    import argparse
    from collections import OrderedDict

    def parameter():
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='csvStack.py',
            description='Sorting MEGA RSCU results so as to draw RSCU figure',
            epilog=r'''
examples:
python  csvStack.py file_path
              ''')
        parser.add_argument("files", help='input file', default=[], nargs='*')
        myargs = parser.parse_args(sys.argv[1:])
        return myargs
    myargs = parameter()
    for i in myargs.files:
        Commander(i)
    print("Done!")
