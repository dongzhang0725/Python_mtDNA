#refineGB.py

**usage:**      `refineGB.py [-h] -f FILE [-n NUM] -o OUT`

**Description:** Refine GenBank file to standard format.

**optional arguments:**

                  -h, --help  show this help message and exit
                  
                  -f FILE     input GenBank file or folder
                  
                  -n NUM      define minimum of the length of the NCR
                  
                  -o OUT      folder of the out file
  
【python 3.4.3】

**Usage example:**

        1.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\scripts\demo.gb -n 300 -o C:\Users\Desktop\myfolder
        
        2.python C:\Users\Desktop\scripts\refineGB.py -f C:\Users\Desktop\gbfolder -o C:\Users\Desktop\myfolder
