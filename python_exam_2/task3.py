from data import dataset
from task1 import *
#рекурсивно вывожу номера зачеток и сколько предметов человек не шарит

def recursionByUsers(user_numbers = list(dataset.keys())):

    if user_numbers == []:
        return 'thats all'

    user_number = user_numbers[0]
    print(user_number)
    sum = len(dataset[user_number])
    print(sum)

    return recursionByUsers(user_numbers[1:])


print("Task 3")

result = recursionByUsers()
print(result)

print("\n\n")




