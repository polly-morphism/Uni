
import re

def getUserDocs():
    """
    Проверяю правильность ввода номера зачетки
    """
    user_input = input('Введите номер своей зачетки: ')

    if (re.match(r"^[A-Z]{2}+\S+№\d{8}$", user_input) ):
        return user_input
    else:
        return False

def getSubjName():
    """
       Проверяю правильность ввода названия предмета
    """
    user_input = input('Введите номер своей зачетки: ')

    if (re.match(r"^[A-Z]{1}+[a-z]$", user_input)):
        return user_input
    else:
        return False
