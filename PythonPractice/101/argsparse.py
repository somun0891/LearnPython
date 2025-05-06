
import argparse 
from pathlib import Path

#create a parser object
parser = argparse.ArgumentParser()

#Add arguments
parser.add_argument("path")
parser.add_argument("date_string")

#declare args
args = parser.parse_args()

#use it
target_dir = Path(args.path)
date_str = args.date_string

print(date_str)

if not target_dir.exists():
    print("The target dir doesn't exist")
    raise SystemExit(1)
else:
    print(target_dir)
	 

#  & d:/LearnPython/.venv/Scripts/python.exe d:/LearnPython/PythonPractice/101/argsparse.py d:/LearnPython/PythonPractice/101/  2024-01-01

"""    LEARN PATHLIB MODULE   """

path = Path('d:/LearnPython/PythonPractice/101/')
for file in path.rglob('*.py'):
    print(file.relative_to('d:/LearnPython/PythonPractice/'))

path  = Path(__file__)
print(path.parent)
print(path.with_stem('argsparse_modified'))  #file name modified + same extension
print(path.with_suffix('.txt')) #extension/suffix changed
print(path.with_name('argsparse_modified'))  #no extension 

print(path.parts) #('d:\\', 'LearnPython', 'PythonPractice', '101', 'argsparse.py')
print(path.suffixes) #argsparse.txt.py  -    ['.txt', '.py']

