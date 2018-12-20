from data import dataset

def addStudentSubj(user_name, subj_name):
    if user_name in dataset:
        subj_set = dataset[user_name]
        subj_set.add(subj_name)
    else:
        dataset[user_name] = {subj_name}



print("Task 1")

addStudentSubj("AA №00000003", 'PE')

addStudentSubj("AA №00000002", 'Programming')

print(dataset)


print("\n\n")