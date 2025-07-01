"Conditionals"

# lower
'''
Day_of_week = input("Enter the day of week: ").lower()
print(str(Day_of_week))

if Day_of_week == "sunday" or Day_of_week == "saturday":
    print("I will do python practice whole day")
else:
    print("I will practice devops tools")
'''


# Note: 
# 1. single equal (=) means assigning a value
# 2. Double equal (==) means compare the values of two arguments


a = int(input("Enter value of a: "))
b = int(input("Enter value of b: "))

choice = input("Enter the options for choice: (options +, -, *, /, %) ")

if choice == "+":
    result1 = a + b
    print("addition: ", result1) 
elif choice == "-":
    result2 = a - b
    print("substraction: ", result2)
elif choice == "*":
    result3 = a * b
    print("multiplication: ", result3)
elif choice == "/":
    result4 = a / b
    print("Devision: ", result4)
elif choice == "%":
    result5 = a % b
    print("remainder: ", result5)
else:
    print("invalid input") 