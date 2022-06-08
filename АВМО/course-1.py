import math


class Fraction:
    def __init__(self, numerator, denominator=1):
        self.numerator = numerator
        self.denominator = denominator
        self.canonize()

    @staticmethod
    def fromstr(string):
        return Fraction(*(int(i.strip()) for i in string.split('/')))

    def __str__(self):
        if self.denominator == 1:
            return f'{self.numerator}'
        elif self.denominator == -1 and self.numerator != 0:
            return f'{-self.numerator}'
        elif self.numerator != 0:
            if self.numerator < 0 or self.denominator < 0:
                return f'-{abs(self.numerator)}/{abs(self.denominator)}'
            else:
                return f'{self.numerator}/{self.denominator}'
        else:
            return f'{self.numerator}'

    def canonize(self):
        def gcd(a, b):
            f = 0
            if a < 0:
                a = -a
                f += 1
            if b < 0:
                b = -b
                f += 1
            while a != 0 and b != 0:
                if a > b:
                    a %= b
                else:
                    b %= a
            if f == 2:
                return (a + b) * (-1)
            return a + b

        g = gcd(self.numerator, self.denominator)
        self.numerator //= g
        self.denominator //= g

    def __float__(self):
        return self.numerator / self.denominator

    def __add__(self, value):
        return Fraction(
            self.numerator * value.denominator + value.numerator * self.denominator,
            self.denominator * value.denominator
        )

    def __sub__(self, value, /):
        return Fraction(
            self.numerator * value.denominator - value.numerator * self.denominator,
            self.denominator * value.denominator
        )

    def __mul__(self, value):
        return Fraction(
            self.numerator * value.numerator,
            self.denominator * value.denominator
        )

    def __truediv__(self, value):
        return Fraction(
            self.numerator * value.denominator,
            self.denominator * value.numerator
        )

    def __neg__(self):
        return Fraction(
            -self.numerator,
            self.denominator
        )


def tabel_print(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if j == len(arr[i]) - 1:
                print('|', end=' ')
            print(arr[i][j], end=' ')
        print()
    print()


def str_print(a, flag=0):
    global basisVars
    k = 0

    basisVars[curr_string], basisVars[k] = basisVars[k], basisVars[curr_string]

    curr = a[curr_string][curr_column]
    a[curr_string], a[k] = a[k], a[curr_string]
    if flag != 1:
        a[0][:] = [a[0][i].__truediv__(curr) for i in
                   range(0, len(a[0]))]


def is_fully_zero(a):
    count = 0
    for i in range(len(a)):
        if a[i].numerator == 0.0:
            count += 1
    return count == len(a)


def nullify(a):
    global curr_string
    n = len(a)
    for i in range(len(a)):
        if i != 0:
            factor = a[i][curr_column]
            a[i][:] = [a[i][j].__sub__(a[0][j].__mul__(factor)) for j in range(len(a[i]))]


def is_optimal_solution(a, basis_vars):
    optimal = True
    for i in range(len(a) - 1):
        if a[i][- 1].__float__() < 0:
            optimal = False
    p = 0
    res[0] = [0] * 5
    for j in basisVars:
        res[0][j] = a[p][len(a[0]) - 1].__float__()
        p += 1
    for j in range(len(a[0]) - 1):
        if j not in basis_vars and a[len(a) - 1][j].__float__() == 0:
            print('Many solution')
            many_solutions(a, j)
            break
    return optimal


def find_min_el(a):
    min_el = []
    for i in range(len(a) - 1):
        for j in range(len(a[i])):
            if j == len(a[i]) - 1:
                min_el.append((a[i][j].__float__(), i))
    return min_el


def calc_co(a, row):
    co = [math.inf] * (len(a[0]) - 1)
    flag = False
    for j in range(len(a[row]) - 1):
        if a[row][j].__float__() < 0:
            flag = True
    if not flag:
        return flag
    for j in range(len(a[row]) - 1):

        if a[len(a) - 1][j].__float__() != 0 and a[row][j].__float__() != 0:
            co[j] = abs(a[len(a) - 1][j].__truediv__(a[row][j]).__float__())
    return co


def many_solutions(a, col):
    global curr_string
    global curr_column
    co = [math.inf] * (len(a) - 1)

    for i in range(len(a) - 1):

        if a[i][col].__float__() > 0:
            co[i] = a[i][len(a[i]) - 1].__truediv__(a[i][col]).__float__()
    minem = min(enumerate(co), key=lambda p: p[1])[0]

    curr_string = minem
    curr_column = col
    basisVars[curr_string] = curr_column
    str_print(a)
    nullify(a)
    tabel_print(a)

    for k, i in enumerate(basisVars):
        print(f'x{i + 1} = {a[k][len(a[k]) - 1]}', end='; ')

    p = 0
    res[1] = [0] * 5
    for j in basisVars:
        res[1][j] = a[p][len(a[0]) - 1]
        p += 1

    lambda_return(res)
    exit()


def lambda_return(res):
    ret = []
    for j in range(len(res[0])):
        ret.append(f'(1-L){res[0][j]}+L*{res[1][j]}')
    for i in ret:
        print(i)


a = [[-3, -2, 1, 0, 0, -13], [-2, -5, 0, 1, 0, -16], [-4, -1, 0, 0, 1, -9], [-3, -5, 0, 0, 0, 0]]

res = [[], []]

if __name__ == '__main__':
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = Fraction(a[i][j])
    tabel_print(a)
    curr_column = 0
    curr_string = 0
    n = len(a) - 1

    start_position = (len(a[0]) - len(a))
    basisVars = [0] * (len(a) - 1)
    basisVars[:] = [a for a in range(start_position, start_position + (len(a) - 1))]

    try:
        while not is_optimal_solution(a, basisVars):
            minEl = find_min_el(a)
            row = min(minEl)[1]
            CO = calc_co(a, row)
            if not CO:
                print('No solutions')
                exit()
            column = min(enumerate(CO), key=lambda p: p[1])[0]
            print(f'\n{basisVars=}')
            tabel_print(a)
            for k, i in enumerate(basisVars):
                print(f'x{i + 1} = {a[k][len(a[k]) - 1]}', end='; ')
            print(f'[{a[len(a) - 1][len(a[0]) - 1]}]')
            print(f'{row=} {column=} [{a[row][column]}]')
            curr_string = row
            curr_column = column
            basisVars[curr_string] = curr_column
            str_print(a)
            nullify(a)
        else:
            print(f'\n{basisVars=}')
            tabel_print(a)
            for k, i in enumerate(basisVars):
                print(f'x{i + 1} = {a[k][len(a[k]) - 1]}', end='; ')
            print(f'[{a[len(a) - 1][len(a[0]) - 1]}]')

            print('\nOptimal solution!')
    except Exception as ex:
        print(ex)
        print('Exception!')
