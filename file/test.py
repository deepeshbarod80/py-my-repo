'''
file1 = open('test1.txt', 'r')    # will open file and read the content
file2 = open('test3.txt', 'w')    # will overwrite the file content
file3 = open('test.txt', 'a')     # will add new content to end of file existing content

print(file.read())
file3.write("\nMY House owner is not good guy4\n")
print(file3)
file3.close()
'''

import os
import os.path
import shutil

#os.mkdir('test')            # will create the folder
#os.rmdir('test')            # will remove the folder
#os.remove('text1.txt')      # will remove the file


#F = os.listdir('/home/deepesh-barod/py/file')
#print(F)


#a = os.path.exists('/home/deepesh-barod/py/file')
#print(a)

#b = os.path.isdir('/home/deepesh-barod/py/file')
#print(b)

"""
shutil.rmtree('test')        # will remove the dir recursively with it's contents
a = os.path.isdir('/home/deepesh-barod/py/file/test')
print(a)
"""

'''
def addition(x, y):
    return x + y

print(addition(3, 4))
'''


'''
a = int(input("Enter an integer number: "))
print("Printing integer number: ", a)

b = float(input("Enter a float number: "))
print("Printing a float number: ", b)

c = str(input("Enter a name: "))
print("Printing a string: ", c)
'''


'''
age = int(input("Enter your age: "))

if age >= 18:
    print("you have right to vote")
else:
    print("you are not eligible to vote")
'''



'''
score = int(input("Enter your score: "))

if score >= 90:
    print("Grade A")

elif score >= 80:
    print("Grade B")

elif score >= 70:
    print("Grade C")

elif score >= 60:
    print("Grade D")

elif score >= 33:
    print("Grade E")

elif score < 33:
    print("Failed")

else:
    print("Invalid score")
'''


x = int(input("Enter a number: "))
y = int(input("Enter a number: "))
z = int(input("Enter a number: "))

if  x > y:
    print("X is bigger than y")
elif y > z:
    print("Y is bigger than z")
elif x > z:
    print("X is bigger than z")
elif y > x:
    print("Y is bigger than x")
elif z > x:
    print("Z is bigger than x")
elif z > y:
    print("Z is bigger than y")
elif x == y:
    print("X is equal to Y")
elif y == z:
    print("Y is equal to Z")
elif x == z:
    print("X is equal to Z")
elif x == y == z:
    print("X is equal to Y and Z")
elif x < y:
    print("X is smaller than Y")
elif y < z:
    print("Y is smaller than Z")
elif x < z:
    print("X is smaller than Z")
elif y < x:
    print("Y is smaller than X")
elif z < x:
    print("Z is smaller than X")
elif z < y:
    print("Z is smaller than Y")

else:
    print("Invalid score")