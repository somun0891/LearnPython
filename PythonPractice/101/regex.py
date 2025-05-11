import re 

text = 'abcxxxabc'
pattern = re.compile(r'abc') # r implies raw string

matches = pattern.finditer('abcabc')

#re.compile , re.search , re.sub , re.split , re.findall
#  , pattern_obj.finditer 
for match in matches:
    print(match)

#Metacharacter

# . - any character except new line 
# , \d - any digit 0-9
# , \D - not a digit
# , \w - word character
# , \W - not a word character
# , \s - whitespace(space , tab , newline)
# , \S - not whitespace (space , tab , newline)
# , \b - word boundary
# , \B - not a word boundary
# , ^ - beginning of string
# , $ - end of string

# Quantifiers
# * - zero or more
# + - one or more
# ? - zero or one
# {n} - exactly n
# {n,} - n or more
# {n,m} - at least n but not more than m
# {,n} = up to n

# | - either or
# ( ) - group

# flags
# re.IGNORECASE
# re.MULTILINE
# re.VERBOSE

phone = '''321-555-4321  
          123.555.1234
          123*555*1234 
          800-555-1234   
          900-555-1234                           
          '''


pattern = re.compile(r'(\d+).(\d+).(\d+)')      

matches = pattern.finditer(phone)
print("\n")
for match in matches:
    print(match)

# A hyphen or a dot
pattern2 = re.compile(r'(\d+)[.-](\d+)[.-](\d+)')

matches  = pattern2.finditer(phone)
print("\n")
for match in matches:
    print(match)

pattern3 = re.compile(r'[89]00[.-]\d{3}[.-]\d{4}')  
matches = pattern3.finditer(phone)
print("pattern3")
for match in matches:
    print(match)


rhymes = 'cat mat pat sat fat hat horn mourn born,flat'
pattern = re.compile(r'[a-zA-Z0-9]+at')
matches = pattern.findall(rhymes)
print("\n")
for match in matches:
    print(match)

pattern = re.compile(r'[^p]at')
matches = pattern.findall(rhymes)
print("\n")
for match in matches:
    print(match)

names = '''
 Mr. Schafer
 Ms. crow
 Mr.  robin
 Ms Pfiffer
 Dr. Schafer
 Prof. Schafer
 Mr. T
'''
pattern = re.compile(r'[Mr|Dr|Ms]+\.?\s{1,}\w*') #??
pattern = re.compile(r'M(r|s|rs)\.?\s{1,}\w*') #??
matches = pattern.finditer(names)

for match in matches:
    print(match)


emails = '''    
CoreyMschafer@gmail.com
Corey.schafer@uni.edu
Corey-321-schafer@my-work.net
Corey_schafer@uni.edu
'''


try:
    pattern = re.compile(r'[a-zA-Z0-9.-_]+@[a-zA-Z-]+\.[a-zA-Z]{2,}' ,re.IGNORECASE)
    matches = pattern.finditer(emails)

    for match in matches:   
        print(match)


except re.error as e:
    print(f"Regex compilation error: {e}")


urls = '''
http://www.google.com
http://yahoo.com
https://www.nasa.gov
https://www.youtube.com
'''
pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w{2,})')

matches = pattern.finditer(urls)

for match in matches:
    print(match.group(2))
    print(match.group(3))

subbed_urls = pattern.sub(r'\2\3', urls)  
print(subbed_urls)
#google.com
#yahoo.com
#nasa.gov
#youtube.com

matches = pattern.findall(urls)
print(matches)

#[('www.', 'google', '.com'), ('', 'yahoo', '.com'), ('www.', 'nasa', '.gov'), ('www.', 'youtube', '.com')]
 
string = 'My phone number is 415-555-4242 and my friend\'s phone number is 408-555-1234'
pattern = re.compile(r'\d{3}-\d{3}-\d{4}')
match = pattern.search(string) #only finds first match
print(match) #415-555-4242
#print(match.group(1))#error - no such group

pattern = re.compile(r'(\d{3})-(\d{3})-(\d{4})')
match = pattern.search(string) #only finds first match
print(match.group(1)) #415
print(match.group(2)) #555
print(match.group(3)) #4242

import os
str = 'I am using #prod_env# environment #dev_env# environment'

env_list = re.findall(r'#(.*?)#' ,str ,re.IGNORECASE)
#print(env_list) #['prod_env', 'dev_env']

env_vars = os.environ.keys()
print('\n')
for env in env_list:
   if not env in env_vars:
       print(f'Environment variable - {env} not found')
#    print( env ,':',os.getenv(env))
   str = str.replace('#'+env+'#',os.getenv(env))

print(str)

print('\n')

s = '012-3456-7890'

match = re.search(r'(\d{3})-(\d{4})-(\d{4})' , s)
print(match.group(2)) #3456

print(re.findall(r'(\d{3})-(\d{4})-(\d{4})' , s)[0][1]) #3456
print(re.findall('<(sachi)>','<sachi>hello<sachi>'))


print(re.findall(r'\(.*\)', 'abc(def)ghi'))  #escape ( ) using backslash
print(re.findall(r'\(.*\)', 'abc()ghi')) #['()']  # .* - zero or more

print(re.findall(r'\(.+\)', 'abc(def)ghi')) #['(def)']
print(re.findall(r'\(.+\)', 'abc(d)ghi')) #['(d)']  #.+ - one or more
print(re.findall(r'\(.?\)', 'abc(d)ghi')) #['(d)']  # .? - zero or one
print(re.findall(r'\(.+\)', 'abc()ghi'))  #[]  #.+ - one or more

s = 'axxxb-012'
print(re.findall('a.*b', s))
# ['axxxb']
print(re.findall(r'\d+', s))
# ['012']
print(re.findall(r'a.*b|\d+', s))
# ['axxxb', '012']