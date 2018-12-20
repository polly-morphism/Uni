from data import dataset

from validators.lib import getUserDocs
from validators.lib import getSubjName


from task1 import addStudentSubj


#   Написати функцію, що зберігає інформацію про покупку користувачем товару у словник.
#   Усі дані вводить користувач. Використати валідатори. Викликати функцію

def addUserSubjValidator():

    user_name = getUserDocs()
    while not user_docs:
        print("Error in docs. Try again")
        user_docs = getUserDocs()


    subj_name = getSubjName()
    while not subj_name:
        print("Error in subject name. Try again")
        subj_name = getSubjName()

        addStudentSubj(user_name, subj_name)



print("Task 1")
addUserSubjValidator()
print(dataset)


print("\n\n")