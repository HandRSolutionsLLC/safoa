import sys,os,tkinter,random, time ,Crypto
from cx_Freeze import setup , Executable

##build_exe_options={'packages':['os','time','random','sqlite3'],'excludes':['tkinter'],
##                   'include_files':[r'C:/Users/HAOMA/Desktop/#BLAKSTAR_NET/Send Me/images' ]}
# choice,options=input('Enter \"1\" for EXEC. FILE OR \"2\" for INSTALLER: '),('1','2')
choice,options='1',('1','2')
while choice not in options:input('Enter \"1\" for EXEC. FILE or \nEnter \"2\" for INSTALLER')
if choice=='1': sys.argv.append('build')
else : sys.argv.append('bdist_msi')
os.environ['TCL_LIBRARY'] = r"C:\Users\HAOMA\AppData\Local\Programs\Python\Python38\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\HAOMA\AppData\Local\Programs\Python\Python38\tcl\tk8.6"

base=None
if sys.platform=='win32': base='Win32GUI'
elif sys.platform=='win64': base='Win64GUI'

build_exe_options={'packages':['os','tkinter','random','time','Crypto'],
                   'include_files':[r"C:\Users\HAOMA\AppData\Local\Programs\Python\Python38\DLLs\tcl86t.dll",r"C:\Users\HAOMA\AppData\Local\Programs\Python\Python38\DLLs\tk86t.dll",r"images"]}

executables=[Executable("SAFOA_silver.pyw",base=base,icon=r'images\icon.ico')]

setup(
    name="SAFOA_S.exe",
    version='1.0',
    description='An encryption software acting as an external key.',
    options={'build_exe':build_exe_options},
    executables=executables)

##import os
##print(os.listdir())
##print('\n')
##print(os.listdir('images'))
