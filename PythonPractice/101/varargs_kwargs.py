

def foo(*args, **kwargs):
    print(f"args={args}, kwargs={kwargs}")

foo()
foo(1,2,3)
foo([1,2,3])
foo("hello")
foo(one=1 , two=2)
foo(1,2,3,one=1 , two=2)


def foo_alt(*args, **kwargs):
    print(f"args={args}, kwargs={kwargs}")
    
    print(len(args[0]))

foo_alt([1,2,3])


def sum(a,b,c):
    print(a+b+c)

sum(*[1,2,3]) #6

def sumd(*inputs):
    result = 0
    for inp in inputs:
        result += inp
    
    return result

    
print(sumd(1,2,5)) #8 passed as individual integers in a tuple - (1, 2, 3)

 #MAKE SURE TO UNPACK THE LIST FIRST AND THEN PASS IT ELSE IT IS A SINGLE TUPLE CONTAINING LIST ([1, 2, 3],)
print(sumd(*[1,2,5])) #8 , same output as above

def greeting(*greeting):
  print(f"{greeting}")


greeting(*"hello Sachi!") #('h', 'e', 'l', 'l', 'o', ' ', 'S', 'a', 'c', 'h', 'i', '!')


def greeting(*greeting , **kwargs):
     print(f"{greeting[0]} {kwargs['name']}, {kwargs['msg']}")


greeting("Hello" , name="Sachi" , msg="How are you doing today?" )
greeting("Welcome" , name="Maya" , msg="Join us for the presentation." )


l1 = [1,2,3]
l2 = [5,6,7]

#merging 2 lists
l3= (*l1 , *l2)
print(list(l3))

d1 = {"name": "Sachi"}
d2 = {"age": 33}

#merging 2 dictionaries
d3= {**d1 , **d2}
print(d3)

"""
Difference between vargs and kwargs

1. Vargs takes positional args but kwargs takes keyword arguments
2. Vargs works with any iterable like list,tuple and even string/range but kwargs work with only dictionaries
3. Vargs MUST COME after standard args but before kwargs
4. Unpacking a iterable and passing it to a variable num of args requires the iterable have exact number of
elements else it throws error.
5. If no arguments are passed in function call , varags returns a empty tuple () and kwargs an empty dict {}
6. Both can be used merge 2 lists/dicts.


"""
