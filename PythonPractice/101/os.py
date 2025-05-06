import os 
import sys 
from pathlib import Path
sys.path.append("D:\\LearnPython\\")

cwd = os.getcwd()

print(cwd)

dirname =  "demo"
dirpath = "D:\\LearnPython\\"

path = os.path.join(dirpath, dirname)

if os.path.exists(path):
    print('True')
else:
    os.mkdir(path)

dirname =  "dirnotexists/dummy"
path = os.path.join(dirpath, dirname)

if os.path.exists(path):
    print('True')
else:
    os.makedirs(path)

path = dirpath
for dir in os.scandir(path):
    if dir.is_file():
        print(dir.path)

print(os.name) #nt

path = "D:\\LearnPython\\first"
for dirpath,dirnames,filenames in os.walk(path):
    for file in filenames:
        print(file)
        #print(f"{file} : {os.path.getsize(file)}") #in bytes
     
"""

IMPORTANT OS FUNCTIONS
=====================
path: A path-like object representing a file system path. 
A path-like object is either a string or bytes object representing a path.

os.getcwd()
os.path.isfile()
os.path.isdir()
os.path.join(dirpath , dirname)
os.path.makedir(dirpath)
os.path.makedirs(dirpath)   #also creating missing folders in the path
os.path.remove(fullfilepath)
os.path.getsizeof(filename)  #internally calls os.stat(filename).st_size
os.path.split(filepath)  #list containing - head - filedirpath  #tail - filename

sys.modules  #shows all modules imported by the python shell
"""

print("Pathlib module useful functions........................",end= "\n")

print(Path.cwd())
Pathobj = Path("D:\\LearnPython\\PythonPractice\\101")
posixpath = Pathobj.as_posix()
print(posixpath) #D:/LearnPython/PythonPractice/101
print(Pathobj.exists())
for f in Pathobj.rglob("*.py"):
    if f.is_file():
      print(f)

print("Path object iterdir() method...",end= "\n")
for f in Pathobj.iterdir():
    print(f.parent)  #parent folder/dir
    print(f.stem)  #filename with suffix
    print(f.parts) #list of file parts
    print(f.suffix) #extension
    print(f.stat().st_size) #bytes   
    print("\n")
   
rainalertPathobj = Path("D:\\LearnPython\\PythonPractice\\101\\rainalert.py")
rainalertnewPathobj = rainalertPathobj.with_stem("rainalert_new")
print(rainalertnewPathobj)

print(Path.cwd().parent)  #parent is D:\ when current dir is D:\LearnPython

print(Path.cwd().home()) # home dir is C:\Users\conne

# demopathObj = Path("D:\\LearnPython\\demo1")
# demopathObj.rmdir()




    







 

