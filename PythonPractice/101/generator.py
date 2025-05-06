import sys

#using return 
def gen_numbers():
    for i in range(10):
        return(i) #any stmt after return is never executed and is unreachable
        print(f"Yielded - {i}")

number=gen_numbers()
print(number) #with return it will print 0


#using generators
"""
This is a generator function in Python. 
It generates numbers from 0 to 9,
 but instead of returning all numbers at once,
it yields each number one at a time. 
The `yield` keyword pauses the function's execution 
and returns the current value, allowing the caller
 to process it before the function resumes. 
 The `print` statement after `yield` will be 
 executed each time the generator yields a value.

"""
def gen_numbers():
    for i in range(10):
        yield(i) #generator object
        print(f"Yielded - {i}") #this is executed 

# number=gen_numbers()

# #generators are iterable
# #generators are lazy
# for i in number: 
#     print(i)

gen = gen_numbers()
first = next(gen)
second  = next(gen)
print(first,second)


#create an infinite list of numbers

def infinite_numbers():
    i=0
    while True:
        yield(i)
        i +=1


gen = infinite_numbers()
first = next(gen)
second = next(gen)
third = next(gen)
four = next(gen)

print(first,second,third)

gen = (g**2 for g in range(10000))
l = [l**2 for l in range(10000)]

print(sys.getsizeof(gen)) #104
print(sys.getsizeof(l)) #85176


