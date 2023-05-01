import matrix

# Класс считывает данные из файла и переводит их в канонический вид
class Canonical_matrix(object):
    def __init__(self, file_name):
        self.elements_name = []
        self.limitation = []
        self.target_function = []
        self.min = False
        self.basis = []
        self.const = 0
        if file_name != '':
            self.read_file(file_name)
            self.canonical

    # функция считывает данные из файла
    def read_file(self, file_name):
        f = open(file_name, 'r', encoding='utf-8')
        for i in f:
            self.limitation.append(i.replace('\n', ''))
        f.close()
        self.elements_name = self.limitation[0].split(' ')
        self.limitation.pop(0)
        self.target_function = self.limitation[0].split(' ')
        self.limitation.pop(0)
        copy = []
        for i in self.limitation:
            copy.append(i.split(' '))
        self.limitation = copy

        for i in range(len(self.target_function) - 2):
            self.target_function[i] = float(self.target_function[i])

        for i in range(len(self.limitation)):
            for l in range(len(self.limitation[i])):
                if self.limitation[i][l] not in ['>=', '<=', '=']:
                    self.limitation[i][l] = float(self.limitation[i][l])

    # функция переводит данные в канонический вид
    @property
    def canonical(self):
        # меняем min на max
        if self.target_function[-1] == 'min':
            for i in range(len(self.target_function) - 2):
                self.target_function[i] = float(self.target_function[i]) * -1
            self.target_function.pop(-1)
            self.target_function.pop(-1)
            self.min = True
        else:
            self.target_function.pop(-1)
            self.target_function.pop(-1)

        # забираем константу
        if len(self.target_function) == len(self.limitation[0]) - 1:
            self.const = self.target_function[len(self.elements_name)]
            if min:
                self.const *= -1
            self.target_function.pop(len(self.elements_name))

        M = self.M_find
        n = 0

        while n < len(self.limitation):
            if self.limitation[n][-1] == 0 and self.limitation[n].count(1) == 1:
                elem = self.limitation[n].index(1)
                if sign[self.limitation[n][-2]] == 0:
                    self.target_function.append(0.0)
                    for l in range(len(self.limitation)):
                        self.limitation[l].insert(-2, self.limitation[l][elem] * -1)
                elif sign[self.limitation[n][-2]] == 1:
                    self.target_function[elem] = self.target_function[elem] * -1
                    for l in range(len(self.limitation)):
                        self.limitation[l][elem] = self.limitation[l][elem] * -1
                self.limitation.pop(n)
            else:
                n += 1

        for i in range(len(self.limitation)):
            if sign[self.limitation[i][-2]] == 0:
                self.basis.append(len(self.limitation[i]) - 2)
                self.append_M(i, M)
            elif sign[self.limitation[i][-2]] == 1:
                self.basis.append(len(self.limitation[i]) - 2)
                self.append_M(i, 0)
            elif sign[self.limitation[i][-2]] == 2:
                self.basis.append(len(self.limitation[i]) - 1)
                self.append_M(i, 0, -1.0)
                self.append_M(i, M)

        for i in range(len(self.limitation)):
            self.limitation[i].pop(-2)

    # функция находит наибольший элемент и создает на его основе значение исскуственного базиса
    @property
    def M_find(self):
        max = 0
        for i in self.limitation:
            for l in i:
                if l in ['=', '>=', '<=']:
                    break
                if float(l) > max:
                    max = float(l)
        for i in self.target_function:
            if float(i) > max:
                max = float(i)
            elif float(i) * -1 > max:
                max = float(i) * -1
        return (max + 20) * -1

    # функция добавляет новый базис во все ограничения
    def append_M(self, where, M, one=1.0):
        self.target_function.append(M)
        self.limitation[where].insert(-2, one)
        for l in range(len(self.limitation)):
            if l != where:
                self.limitation[l].insert(-2, 0.0)

# Класс решате задачу и выдает ответ
class Mextures(object):
    def __init__(self, file_name):
        self.matrix = Canonical_matrix(file_name)
        self.basis = self.matrix.basis
        self.limitation = self.matrix.limitation
        self.answer = []
        self.summ = 0
        self.simplex

    # функция реализующая сам симплекс метод
    @property
    def simplex(self):
        while 1:
            calculation = []
            for i in range(len(self.matrix.target_function) - 1):
                calculation.append(0)
            for i in range(len(self.matrix.target_function) - 1):
                n = 0
                for l in self.basis:
                    calculation[i] += self.limitation[n][i] * self.matrix.target_function[l]
                    n += 1
                calculation[i] -= self.matrix.target_function[i]
            min = 0
            for i in calculation:
                if i < min:
                    min = i

            if min == 0:
                break

            score = []
            for i in self.limitation:
                if i[calculation.index(min)] <= 0:
                    score.append('-')
                else:
                    score.append(i[-1] / i[calculation.index(min)])

            if score.count('-') == len(self.limitation):
                break

            min_2 = score[0]
            for i in score:
                if i != '-' and (min_2 == '-' or i < min_2):
                    min_2 = i
            min = calculation.index(min)
            min_2 = score.index(min_2)
            self.limitation[min_2] = matrix.divide_line(self.limitation[min_2], self.limitation[min_2][min])
            for i in range(len(self.limitation)):
                if i != min_2:
                    matrix.subtract_from_line(self.limitation[min_2], self.limitation[i], self.limitation[i][min])
            self.basis[min_2] = min

    # функция на основе полученного ответа выбирает только введенные пользователем переменные
    @property
    def create_answer(self):
        answer = []
        for i in self.limitation:
            answer.append(i[-1])
        n = 0

        # проверяем что в ответе не участвуют исскуственные базисы
        for i in self.basis:
            if self.matrix.target_function[i] != 0 and i > len(self.matrix.elements_name):
                return False

        while n != len(self.basis):
            if self.basis[n] >= len(self.matrix.elements_name):
                answer.pop(n)
                self.basis.pop(n)
            else:
                n += 1

        for i in range(len(self.matrix.elements_name)):
            if i not in self.basis:
                self.answer.append(0)
            else:
                self.answer.append(answer[self.basis.index(i)])

        # проверяем есть ли в ответе хоть один из элементов введенных пользователем
        if len(self.basis) == 0:
            return False

        for i in range(len(self.matrix.target_function)):
            if i in self.basis:
                self.summ += self.matrix.target_function[i] * self.answer[i]
        if self.matrix.min:
            self.summ *= -1
        self.summ += self.matrix.const
        return self.summ != 0

# Знаки
sign = {'=': 0, '<=': 1, '>=': 2}
