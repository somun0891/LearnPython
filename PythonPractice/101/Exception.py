

class InvalidFileNameError(Exception): #inherited from base class
    def __init__(self):
        print("cannot specify invalid file name...")
    pass


try:
     f = open('testfile.txt')
     if f.name == 'corrupt_file.txt':
         raise InvalidFileNameError('Incorrect name error!')
except FileNotFoundError as e:
    print(e)
except InvalidFileNameError as e:
    print(e)    
except Exception as e:
    print(e)
# except (InvalidFileNameError,Exception) as e:
#     print(e)
else: #can be used to retry or conitnue further after exception
    print(f.read()) 
finally: #runs no matter what
    f.close() 
    print("Executing finally...")   
    



