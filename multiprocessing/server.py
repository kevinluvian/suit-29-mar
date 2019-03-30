import time

def validate_password(password):
    time.sleep(0.1)
    real_password = '9d5e3ecdeb4cdb7acfd63075ae046672'
    if len(real_password) != len(password):
        return 'Wrong password length'
    
    for i in range(len(real_password)):
        if real_password[i] != password[i]:
            return f'Wrong password at position {i}'
    return 'Correct password'
