import server
from finder_helper import charrange, padder, parse_wrong_position, print1, print2

now = time.time()

# cek password length yg bener
correct_length = 0
for i in range(40):
    test_password = 'a' * i
    print1(f'Trying: {test_password}')
    msg = server.validate_password(test_password)
    if msg == 'Wrong password length':
        continue
    else:
        correct_length = i
        print2(f'Found password length: {len(test_password)}')
        break


# cek password 1 1
answer = ''
possible_char = [x for x in charrange('a', 'z')] + [x for x in charrange('0', '9')]

for i in range(correct_length):
    for test_char in possible_char:
        test_password = padder(f'{answer}{test_char}', correct_length)
        print1(f'Trying: {test_password[:len(answer)]}[{test_char}]{test_password[len(answer) + 1:]}')
        msg = server.validate_password(test_password)
        if msg == 'Correct password':
            print2(f'Found correct password: {test_password}')
            break
        wrong_position = parse_wrong_position(msg)
        if wrong_position > i:
            answer += test_char
            break

print(f'Finish time: {time.time() - now}')