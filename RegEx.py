import re


def regEmail(email):
    ex = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
    output = str(re.fullmatch(ex, email))
    print(output)
    return output


def regPhoneNo(phoneNo):
    ex = re.compile('^(\()?\d{3}(\))?(-|\s)?\d{3}(-|\s)\d{4}$')
    output = str(re.fullmatch(ex, phoneNo))
    print(output)
    return output


def regDateTime(input):
    print(input)
    ex = re.compile('\d{2}-\d{2}-\d{2}-\d{2}:\d{2}$')
    output = str(re.fullmatch(ex, input))
    print(output)
    return output
