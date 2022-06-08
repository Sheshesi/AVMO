import math
import itertools


def reading_equations():
    """
    Считывание матрицы из консоли в масив matrix_from_equation.
    [ строка
    [ значение элемента:
    [числитель, знаминатель]
    ]
    ]
    :return: возвращает массив, хранящий матрицу со значениями
    """
    print('Введите количество строк: ', end='')
    lines = int(input())
    print('Введите коэффициенты уравнений матрицы и результат в виде \'0 -1 10 -11 100\'')
    matrix_from_equation = []
    for line in range(lines):
        values_from_input = input().strip().split()
        matrix_from_equation.append([])
        for pair in range(len(values_from_input)):
            matrix_from_equation[-1].append([int(values_from_input[pair]), 1])
    return matrix_from_equation


def print_matrix(matrix_for_print):
    """
    Вывод матрицы на экран, с учетом отделения правой части расширенной матрицы и правильного вывода дробных
   значений.
    :param matrix_for_print: матрица со значениями
    :return: nothing
    """
    print()
    for line in range(len(matrix_for_print)):
        for element in range(len(matrix_for_print[line])):
            print(str(matrix_for_print[line][element][0]) if matrix_for_print[line][element][1] == 1
                else str(matrix_for_print[line][element][0]) + '/' + str(matrix_for_print[line][element][1]), end=' ')
            if element == len(matrix_for_print[line]) - 2:
                print('|', end=' ')
        print()


def divide_by_gcd(pair):
    """
    Сокращение дроби на НОД и перенос знака в числитель.
    :param pair: [числитель, знаменатель]
    :return: сокращенные значения числителя и знаменателя
    """
    gcd_value = math.gcd(pair[0], pair[1])
    pair[0] //= gcd_value
    pair[1] //= gcd_value
    if pair[1] < 0:
        pair[0] *= -1
        pair[1] *= -1
    return pair


def drop_zero_lines(matrix_with_zero_line):
    """
    Если в матрице есть нулевые строки, функция удаляет их для удобства работы и выводит итог на экран.
    :param matrix_with_zero_line: матрица с, предположительно, нулевыми строками
    :return: матрица без нулевый строк.
    """
    matrix_without_zero_line = []
    for line in range(len(matrix_with_zero_line)):
        zero_line_flag = True
        for element in range(len(matrix_with_zero_line[line])):
            if matrix_with_zero_line[line][element][0] != 0:
                zero_line_flag = False
                break
        if not zero_line_flag:
            matrix_without_zero_line.append(matrix_with_zero_line[line])
    if matrix_with_zero_line != matrix_without_zero_line:
        print_matrix(matrix_without_zero_line)
    return matrix_without_zero_line


def calculating_matrices(matrix, text=''):
    """
    Решение матрицы методом Жордана-Гаусса.
    :param matrix: матрица в виде:
    [ строка
    [ значение элемента:
    [числитель, знаминатель]
    ]
    ]
    :param text: для удобства поиска базисных решений
    :return: возвращает итоговое значение марицы
    """
    if text != '':
        print(text + ':', end='')
    for diagonal in range(min(len(matrix), len(matrix[0]) - 1)):
        # поиск ненулевого значения для элемента главной диагонали
        for line in range(diagonal, len(matrix)):
            if matrix[line][diagonal][0] != 0:
                if line == 0:
                    break
                else:
                    matrix[diagonal], matrix[line] = matrix[line], matrix[diagonal]
                    break
        # проверка на ноль элемента на главной диагонали
        if  matrix[diagonal][diagonal][0] == 0:
            continue
        # создаем копию матрицы для рассчетов
        temp_matrix = []
        for i in range(len(matrix)):
            temp_matrix.append([])
            for j in range(len(matrix[i])):
                temp_matrix[i].append([matrix[i][j][0], matrix[i][j][1]])
        # деление соответствующей строчки на значение разрешающего элемента
        for element in range(len(matrix[diagonal])):
            matrix[diagonal][element][1] *= temp_matrix[diagonal][diagonal][0]
            matrix[diagonal][element][0] *= temp_matrix[diagonal][diagonal][1]
            matrix[diagonal][element] = divide_by_gcd(matrix[diagonal][element])
        # зануляем все значения, кроме выбранного значения на главной диагонали
        for element in range(len(matrix)):
            matrix[element][diagonal][0] = 0 if element != diagonal else 1
            matrix[element][diagonal][1] = 1
        # вычисление методом прямоугольника
        for line in range(len(matrix)):
            if line == diagonal:
                continue
            for element in range(diagonal + 1, len(matrix[line])):
                matrix[line][element][0] *= temp_matrix[line][diagonal][1] * temp_matrix[diagonal][element][1] * \
                                    temp_matrix[diagonal][diagonal][0]
                matrix[line][element][0] -= temp_matrix[line][diagonal][0] * temp_matrix[diagonal][element][0] * \
                                temp_matrix[diagonal][diagonal][1] * temp_matrix[line][element][1]
                matrix[line][element][1] *= temp_matrix[line][diagonal][1] * temp_matrix[diagonal][element][1] * \
                                temp_matrix[diagonal][diagonal][0]
                matrix[line][element] = divide_by_gcd(matrix[line][element])
                # matrix[line][element] = temp_matrix[line][element] \
                # - (temp_matrix[line][diagonal] * temp_matrix[diagonal][element]) \
                # / temp_matrix[diagonal][diagonal]
        print_matrix(matrix)
    matrix = drop_zero_lines(matrix)
    if text != '':
        print('----------------------')
    return matrix


def basis_solutions(basis):
    """
    Поиск базисных решений системы линейных уравнений.
    :param basis: матрица после подсчета методом Жордана-Гаусса, без нулевых строк.
    :return:
    """
    print('\nБазисное решение:\n')
    basis_solution = []
    calculating_if_one = []
    combination_line = [1 if i < len(basis) else 0 for i in range(len(basis[0]) - 1)]
    all_positions = set(itertools.permutations(combination_line, len(basis[0]) - 1))
    for line in all_positions:
        calculating_if_one.append([])
        for massive_line in range(len(line)):
                calculating_if_one[-1].append(line[massive_line])
    calculating_if_one.sort()
    calculating_if_one.reverse()
    # for line in range(len(calculating_if_one)):
    # print(calculating_if_one[line])
    c_n_r = int(math.factorial(len(basis[0]) - 1) /
                (math.factorial(len(basis)) * math.factorial(len(basis[0]) - 1 - len(basis))))
    for line in range(c_n_r):
        basis_solution.append([])
        for x in range(len(basis[0]) - 1):
            basis_solution[line].append([0, 1])

    for cnr_line in range(c_n_r):
        temp_basis_matrix = []
        for line in range(len(basis)):
            temp_basis_matrix.append([])

        for element in range(len(calculating_if_one[cnr_line])):
            if calculating_if_one[cnr_line][element] == 1:
                for line in range(len(basis)):
                    temp_basis_matrix[line].append([0, 1])
                    temp_basis_matrix[line][-1][0] = basis[line][element][0]
                    temp_basis_matrix[line][-1][1] = basis[line][element][1]
        for line in range(len(basis)):
            temp_basis_matrix[line].append([0, 1])
            temp_basis_matrix[line][-1][0] = basis[line][-1][0]
            temp_basis_matrix[line][-1][1] = basis[line][-1][1]
        temp_basis_matrix = calculating_matrices(temp_basis_matrix, str(calculating_if_one[cnr_line]))
        diagonal = 0
        for paste_to in range(len(calculating_if_one[cnr_line])):
            if calculating_if_one[cnr_line][paste_to] == 1 and temp_basis_matrix[diagonal][diagonal][0] == 1:
                basis_solution[cnr_line][paste_to][0] = temp_basis_matrix[diagonal][-1][0]
                basis_solution[cnr_line][paste_to][1] = temp_basis_matrix[diagonal][-1][1]
                diagonal += 1
    output_line = ''
    for line in range(c_n_r):
        count_x = 0
        line_to_add_x = ''
        line_to_add_values = '('
        for element in range(len(basis_solution[line])):
            if calculating_if_one[line][element] == 1:
                count_x += 1 if basis_solution[line][element][0] != 0 else 0
                line_to_add_x += 'x' + str(element + 1) + (', ' if count_x < len(basis) else '')
            line_to_add_values += (', ' if line_to_add_values != '(' else '') + (str(basis_solution[line][element][0]) if
                                                                         basis_solution[line][element][1] == 1 \
                else str(basis_solution[line][element][0]) + '/' + str(basis_solution[line][element][1]))
        if count_x == len(basis):
            output_line += line_to_add_x + ': ' + line_to_add_values + ')\n'
        else:
            output_line += line_to_add_x[:-2] + ': не может быть вместе в базисе\n'
    print(output_line)


def result(final_matrix):
    """
    Нахождение общего решения или отсутствия решений.
    :param final_matrix: матрица в виде:
    [ строка
    [ значение элемента:
    [числитель, знаминатель]
    ]
    ]
    :return: nothing
    """
    for i in range(len(final_matrix)):
        for j in range(len(final_matrix[i])):
            if final_matrix[i][j][0] != 0:
                if j < len(final_matrix[i]) - 1:
                    break
                else:
                    print('Система не имеет решения.')
                    return
    common_decision = 'Общее решение:\n'
    for i in range(len(final_matrix)):
        for j in range(i, len(final_matrix[i]) - 1):
            if final_matrix[i][j][0] != 0:
                common_decision += '+ ' if final_matrix[i][j][0] > 0 and common_decision[-3] == 'x' else ''
                common_decision += ((str(final_matrix[i][j][0]) if final_matrix[i][j][1] == 1
                         else str(final_matrix[i][j][0]) + '/' + str(final_matrix[i][j][1]))
                        if final_matrix[i][j][0] != 1 or final_matrix[i][j][1] != 1 else '') \
                       + 'x' + str(j + 1) + ' '
        common_decision += ('= ' + (str(final_matrix[i][-1][0]) if final_matrix[i][-1][1] == 1
                                else str(final_matrix[i][-1][0]) + '/' + str(final_matrix[i][-1][1]))
                        if final_matrix[i][-1][0] != 0 and final_matrix[i][-1][1] != 0 else '') + '\n'
    print()
    print(common_decision)
    basis_solutions(final_matrix)


if __name__ == '__main__':
    matrix_from_equations = reading_equations()
    print_matrix(matrix_from_equations)
    matrix_from_calculating = calculating_matrices(matrix_from_equations)
    result(matrix_from_calculating)
