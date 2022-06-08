import math


def reading_equations():
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
    print()
    for line in range(len(matrix_for_print)):
        for element in range(len(matrix_for_print[line])):
            print(str(matrix_for_print[line][element][0]) if matrix_for_print[line][element][1] == 1
                  else str(matrix_for_print[line][element][0]) + '/' + str(matrix_for_print[line][element][1]), end=' ')
            if element == len(matrix_for_print[line]) - 2:
                print('|', end=' ')
        print()


def divide_by_gcd(pair):
    gcd_value = math.gcd(pair[0], pair[1])
    pair[0] //= gcd_value
    pair[1] //= gcd_value
    if pair[1] < 0:
        pair[0] *= -1
        pair[1] *= -1
    return pair


def calculating_matrices(matrix):
    for diagonal in range(min(len(matrix), len(matrix[0]) - 1)):
        for line in range(diagonal, len(matrix)):
            if matrix[line][diagonal][0] != 0:
                if line == 0:
                    break
                else:
                    matrix[diagonal], matrix[line] = matrix[line], matrix[diagonal]
                    break
        if matrix[diagonal][diagonal][0] == 0:
            continue

        temp_matrix = []
        for i in range(len(matrix)):
            temp_matrix.append([])
            for j in range(len(matrix[i])):
                temp_matrix[i].append([matrix[i][j][0], matrix[i][j][1]])

        for element in range(len(matrix[diagonal])):
            matrix[diagonal][element][1] *= temp_matrix[diagonal][diagonal][0]
            matrix[diagonal][element][0] *= temp_matrix[diagonal][diagonal][1]
            matrix[diagonal][element] = divide_by_gcd(matrix[diagonal][element])

        for element in range(len(matrix)):
            matrix[element][diagonal][0] = 0 \
                if element != diagonal \
                else 1
            matrix[element][diagonal][1] = 1

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

        print_matrix(matrix)
    return matrix


def result(final_matrix):
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
                common_decision += '+ ' if final_matrix[i][j][0] > 0 and common_decision[- 3] == 'x' else \
                    ''
                common_decision += ((str(final_matrix[i][j][0]) if final_matrix[i][j][1] == 1
                                     else str(final_matrix[i][j][0]) + '/' + str(final_matrix[i][j][1]))
                                    if final_matrix[i][j][0] != 1 or final_matrix[i][j][1] != 1 else '') \
                                   + 'x' + str(j + 1) + ' '
                common_decision += ('= ' + (str(final_matrix[i][-1][0]) if final_matrix[i][-1][1] == 1
                                            else str(final_matrix[i][-1][0]) + '/' + str(final_matrix[i][-1][1]))
                                    if final_matrix[i][-1][0] != 0 and final_matrix[i][-1][1] != 0 else '') + '\n'
    print()
    print(common_decision)


if __name__ == '__main__':
    matrix_from_equations = reading_equations()
    print_matrix(matrix_from_equations)
    matrix_from_calculating = calculating_matrices(matrix_from_equations)
    result(matrix_from_calculating)
