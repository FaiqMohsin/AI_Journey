# Day 8 - List Comprehension, map, filter and lambda

num =[1,1,2,2,3,3,4,5,6,7,8,9,10]
name=['bruce','clark','diana','barry','arthur']
hero=['batman','superman','wonder woman','flash','aquaman']

#list
mylist = [n for n in num]
print (mylist)

#list with square of main values
mylist = [n*n for n in num ]
print (mylist)

#list containing only even numbers
mylist=[n for n in num if n%2==0]
print (mylist)

#list containing only odd numbers
mylist=[n for n in num if n%2!=0]
print (mylist)

#list containing tuples of letters and numbers
mylist=[(letter,num) for letter in 'abcd' for num in range(4)]
print (mylist)

#Dictionary container list of name and hero assigned to each other as key and value
mydict={name:hero for name,hero in zip(name,hero) if name != 'barry'}
print (mydict)

#set contains unique values
myset={n for n in num }
print (myset)

#generator expression
mygenerator=(n for n in num)
for n in mygenerator:
    print (n)

# filter keep only items that pass a condition
# map do something to every item in a list
# lambda  a function without a name, written in one line
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, numbers)))
print(result)  # [4, 8, 12, 16, 20]


