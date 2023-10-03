def brackets_result(brackets):
    global array
    i = 0
    result = []
    while i < len(brackets):
        if brackets[i] == '(':
            result.append('(')
            i += 1
        else:
            k = brackets.find(' ', i)
            if k == -1:
                k = len(brackets)
            j = 1
            while not brackets[k - j].isalpha():
                j += 1
            word = brackets[i:k - j + 1]
            if word.isupper():
                logic_word = word.lower()
                result.append(logic_word)
            else:
                result.append(str(name in array))
            if j > 1:
                result.append(')' * (j - 1))
            i = k + 1
    print(result)
    return eval(' '.join(result))


string = 'abc_ON [NOT b AND (c OR (d OR e AND (f OR NOT g)) OR h) OR (i OR NOT j)]'
array = ['c', 'd', 'e', 'f', 'h', 'i']

marker = string.find(' ')
if marker == -1:
    name, status = string.split('_')
    all_result = status == 'ON' and name not in array or status == 'OFF' and name in array
else:
    name, status = string[:marker].split('_')
    brackets_bool_result = brackets_result(string[marker+2:-1])
    slave_result = status == 'ON' and name not in array or status == 'OFF' and name in array
    all_result = slave_result and brackets_bool_result

print(all_result)
