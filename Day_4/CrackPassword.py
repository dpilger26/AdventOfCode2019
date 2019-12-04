"""
Cracks the Venus depot password
"""
PASSWORD_LENGTH = 6
PASSWORD_MIN = 272091
PASSWORD_MAX = 815432


def countPossiblePasswords():
    """
    Counts the possible password combinations
    """
    numPossiblePasswords = 0
    for password in range(PASSWORD_MIN, PASSWORD_MAX):
        passwordStr = str(password)
        if not containsDoubleNumber(passwordStr):
            continue

        if not isIncreasingDigits(passwordStr):
            continue

        numPossiblePasswords += 1

    print(f'Number of Possible Passwords = {numPossiblePasswords}')


def countPossiblePasswordsRefined():
    """
    Counts the possible password combinations
    """
    numPossiblePasswords = 0
    for password in range(PASSWORD_MIN, PASSWORD_MAX):
        passwordStr = str(password)
        if not isIncreasingDigits(passwordStr):
            continue

        if not containsOnlyADouble(passwordStr):
            continue

        numPossiblePasswords += 1

    print(f'Refined Number of Possible Passwords = {numPossiblePasswords}')


def isIncreasingDigits(password: str):
    """
    Returns true if the digits of the password are increasing
    """
    return ''.join(sorted(password)) == password


def containsDoubleNumber(password: str):
    """
    Returns true if the password contains a double value
    """
    return ('11' in password or
            '22' in password or
            '33' in password or
            '44' in password or
            '55' in password or
            '66' in password or
            '77' in password or
            '88' in password or
            '99' in password or
            '00' in password)


def containsOnlyADouble(password: str):
    """
    Returns true if the password a double not part of a larger sequence
    """
    for value in range(10):
        containsDouble = False
        valueStr = str(value)
        if valueStr * 2 in password:
            containsDouble = True

        for numDigits in range(3, PASSWORD_LENGTH + 1):
            if valueStr * numDigits in password:
                containsDouble = False

        if containsDouble:
            return True

    return False


if __name__ == '__main__':
    countPossiblePasswords()
    countPossiblePasswordsRefined()
