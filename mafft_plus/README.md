#mafft_plus.py
---
【python 3.4.3】 [**biopython**][hover] must be enabled 
[hover]:http://biopython.org/wiki/Download "download biopython"

**usage:** `mafft_plus.py [-h] [-f FILE] [-table {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}] [-mafft MAFFT] [-codon]`

**Description:** Add codon alignment and batch run to mafft

**optional arguments:**

					-h, --help            show this help message and exit

					-f FILE               input fasta file or folder

					-table {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21,22,23}

									  choose a codon table!【1(default)|2|3|4|5|6|9|10|11|12|13|14|15|16|21|22|23】
									  NCBI GenBank codon table
									  1 Universal code 
									  2 Vertebrate mitochondrial code 
									  3 Yeast mitochondrial code 
									  4 Mold, Protozoan, and Coelenterate Mitochondrial code and Mycoplasma/Spiroplasma code
									  5 Invertebrate mitochondrial 
									  6 Ciliate, Dasycladacean and Hexamita nuclear code 
									  9 Echinoderm and Flatworm mitochondrial code
									  10 Euplotid nuclear code 
									  11 Bacterial, archaeal and plant plastid code 
									  12 Alternative yeast nuclear code 
									  13 Ascidian mitochondrial code 
									  14 Alternative flatworm mitochondrial code 15 Blepharisma nuclear code 
									  16 Chlorophycean mitochondrial code 
									  21 Trematode mitochondrial code 
									  22 Scenedesmus obliquus mitochondrial code 
									  23 Thraustochytrium mitochondrial code
									  
					-mafft           	  the path of the mafft
					
					-codon                Boolean, whether codon alignment or not

**Usage example:**

*Normal align (the output file will be deposited in the mafft_out folder of scripts directionary):*

    【single file】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta -mafft C:\Users\Desktop\mafft-win\mafft.bat
	
    【input folder】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align -mafft C:\Users\Desktop\mafft-win\mafft.bat

*Codon align (the output file will be deposited in the codon_alignments folder of scripts directionary):*

    【single file】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta -table 1 -mafft C:\Users\Desktop\mafft.bat -codon
	
    【input folder】 python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align -table 1 -mafft C:\Users\Desktop\mafft.bat -codon
    
~~~

>* 本脚本是通过[**python3.43**][dowload]编写，请下载python3及其以上的版本。
[dowload]:https://www.python.org/downloads/release/python-343/ "python3.43下载"

>* 密码子的翻译是通过[**biopython**][hover]实现的,请安装biopython模块。
[hover]:http://biopython.org/wiki/Download "biopython模块安装方法" 

>* 脚本及相关文件下载地址：[**Github**][github] 或者 [**百度云盘**][yunpan](密码nsj4）
[github]:https://github.com/dongzhang0725/Python_mtDNA/tree/master/mafft_plus "推荐" 
[yunpan]:http://pan.baidu.com/s/1mhN2ene "密码：nsj4" 

##新增功能
本脚本在mafft原有功能基础上

- 实现mafft的codon比对

- 支持多文件同时批量运行

##codon比对原理
- 第一步将用户传入的核苷酸序列翻译为氨基酸序列
 
- 第二步将翻译后的氨基酸序列通过mafft进行比对

- 第三步将比对后的氨基酸序列回译为codon序列

>此原理的可行性还有待专业人士鉴定

##脚本操作
>* 用户可以通过-codon参数来决定是否进行codon比对。
>
	- 当无-codon参数时，即进行普通比对模式，用户只需要使用-f参数传入文件以及-mafft参数指定mafft可执行文件的路径
>
	- 当有-codon参数时，即开启codon比对模式，除了上述2个参数外，用户还需要传入-table参数以决定使用哪一套遗传密码表

>* 用户可以传入一个单独的fasta文件或者含有多个fasta文件的文件夹进行批量比对

>* 如果用户传入的核苷酸序列是比对过的（即序列内部含有gap），在codon比对模式下，脚本会将其转换为比对前的状态

>* 普通模式比对结果存在脚本目录的mafft\_out文件夹内；codon模式比对结果保存在脚本目录的codon\_alignments文件夹内，同时vessel文件夹内保存的是翻译后的氨基酸序列AA\_sequence和mafft比对后的氨基酸序列AA\_alignments

>* 所有参数均有默认设置（如果用户不输入参数时即执行默认设置）
	- -f参数默认读取脚本目录下align文件夹内的文件（如果想偷懒，就把文件粘贴到该文件夹内）
	- -mafft参数默认指定脚本目录下mafft-win文件夹内mafft.bat文件为mafft的可执行文件（如果想偷懒，将mafft解压到脚本目录）
	- -table参数默认指定第一套密码表即标准密码表
	- -codon参数为布尔开关类型，默认关闭，即进行普通比对

**操作示例：**

* 普通比对
	- 传入单文件

		- `python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta -mafft C:\Users\Desktop\mafft-win\mafft.bat`

	- 传入文件夹
		- `python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align -mafft C:\Users\Desktop\mafft-win\mafft.bat`	
		- `python C:\Users\Desktop\mafft_plus.py`【懒人模式,使用默认参数】

* codon比对
	- 传入单文件
		- `python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\demo.fasta -table 1 -mafft C:\Users\Desktop\mafft-win\mafft.bat -codon`
	- 传入文件夹
		- `python C:\Users\Desktop\mafft_plus.py -f C:\Users\Desktop\align -table 1 -mafft C:\Users\Desktop\mafft-win\mafft.bat -codon`
		- `python C:\Users\Desktop\mafft_plus.py`【懒人模式】
~~~
