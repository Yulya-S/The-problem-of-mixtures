import pygame
import mextures
import os

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY_BLUE = (132, 141, 160)
PURPLE = (217, 216, 227)
RED = (255, 0, 0)


def text_at_center(screen, font, message, x, y, is_active=False):
    text = font.render(message, True, BLUE if is_active else GREY_BLUE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def text_at_left(screen, font, message, x, y, is_active=False):
    text = font.render(message, True, BLUE if is_active else GREY_BLUE)
    text_rect = text.get_rect(center=(0, y))
    text_rect.left = x
    screen.blit(text, text_rect)


def text_at_90_deg(screen, message, x, y, is_active=False):
    font = pygame.font.SysFont('Comic Sans MS', 15)
    for i in message:
        text = font.render(i, True, BLUE if is_active else GREY_BLUE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        y -= 8
        x += 8


def button_with_text(screen, font, message, x, y, wight, is_active):
    pygame.draw.rect(screen, BLUE if is_active else GREY_BLUE, (x, y, wight, 50), 1)
    text_at_center(screen, font, message, wight / 2 + x, y + 20, is_active)


def radio_buttons(screen, font, box_name, labels, y, select_button_x, is_our_y, activ):
    text_at_center(screen, font, box_name, 1200 / 2, y - 50)
    lambda_x = 1200 / (len(labels) * 1.5)
    x = 1200 / (len(labels) * 1.8)
    for i in labels:
        color_activ = BLUE if labels.index(i) == select_button_x and is_our_y else GREY_BLUE
        text_at_left(screen, font, i, x + 20, y, color_activ == BLUE)
        pygame.draw.circle(screen, color_activ, [x, y], 10, 1)
        if activ == labels.index(i):
            pygame.draw.circle(screen, color_activ, [x, y], 5)
        x += lambda_x


def window_for_text(screen, font, labels, x, y, is_active):
    text_at_left(screen, font, labels[0], x + 30, y)
    button_with_text(screen, font, labels[1], x * 3 + 30, y - 20, 1200 / 4, is_active)


def is_degit_in_list(list):
    for i in list:
        if not i.isdigit():
            return False
    return True


def is_degit_float_for_list(content):
    for i in content:
        c = i.split('.')
        if len(c) > 2 or not is_degit_in_list(c):
            return False
    return True


class Window(object):
    def __init__(self):
        self.file_name = ""
        self.direction_objective_function = 0  # 0 - max, 1 - min
        self.tab = False
        self.decision_in = 0  # 0 - Процентах 1 - Количествах
        self.quantity = ["", ""]  # кол-во элементов | кол-во свойств
        self.target_function = []
        self.components = []
        self.select_window = 0
        self.select_button_x = self.select_button_y = 0
        self.step = [0, 0]
        self.no_errors = True

        self.label = {
            0: ["Выбрать файл", "Внести новые данные", "Выйти"],
            1: [0, 0, 0, 0, 0],
            2: [],
            3: [0, 0, 0, 0],
            4: [0],
            5: [],
            6: []
        }

    def window(self, screen):
        clock = pygame.time.Clock()
        while True:
            clock.tick(10)
            if self.tab and (self.select_window in [2, 4, 6] or (self.select_window == 5 and len(self.label[5]) != 1)):
                screen.fill(PURPLE)
            else:
                screen.fill(WHITE)
            font = pygame.font.SysFont('Comic Sans MS', 25)
            y = 720 / 4 + (self.step[0] * 70)
            if self.select_window == 1:
                window_for_text(screen, font, ["Введите название файла", self.file_name], 1200 / 6, y - 20, \
                                self.select_button_y == 0)
                window_for_text(screen, font, ["Введите кол-во элементов", self.quantity[0]], 1200 / 6, y + 50, \
                                self.select_button_y == 1)
                window_for_text(screen, font, ["Введите кол-во свойств", self.quantity[1]], 1200 / 6, y + 120, \
                                self.select_button_y == 2)
                button_with_text(screen, font, "Далее", 1200 / 4, y + 220, 1200 / 2, self.select_button_y == 3)
                button_with_text(screen, font, "Назад", 1200 / 4, y + 290, 1200 / 2, self.select_button_y == 4)
            elif self.select_window == 3:
                radio_buttons(screen, font, "Выберите направление функции", ["MAX", "MIN"], y, \
                              self.select_button_x, self.select_button_y == 0, self.direction_objective_function)
                text_at_center(screen, font, "Введите значения для целевой функции:", 1200 / 2, y + 90)
                x = 1200 / 4
                for i in range(int(self.quantity[0]) + 1):
                    text_at_90_deg(screen, "C" if i > int(self.quantity[0]) - 1 else self.label[2][i], \
                                   x + 15 + self.step[1] * -70, y + 170, \
                                   self.select_button_y == 1 and self.select_button_x == i)
                    button_with_text(screen, font, self.target_function[i], x + self.step[1] * -70, y + 180, 80, \
                                     self.select_button_y == 1 and self.select_button_x == i)
                    x += 80
                button_with_text(screen, font, "Далее", 1200 / 4, y + 260, 1200 / 2, self.select_button_y == 2)
                button_with_text(screen, font, "Назад", 1200 / 4, y + 330, 1200 / 2, self.select_button_y == 3)
            elif self.select_window == 4:
                message = self.label[2] + ["Знак", "Ограничено"]
                x = 110
                for i in range(len(message)):
                    if self.step[1] <= i:
                        text_at_90_deg(screen, message[i], x + 15, 230, not self.tab and self.select_button_x == i)
                        x += 100
                y = 250
                for i in range(int(self.quantity[1])):
                    if self.step[0] <= i:
                        x = 110
                        text_at_left(screen, font, str(i + 1), 30, y + 25, not self.tab and self.select_button_y == i)
                        for l in range(len(self.components[0])):
                            if self.step[1] <= l:
                                button_with_text(screen, font, self.components[i][l], x, y, 100, \
                                                 not self.tab and self.select_button_y == i and self.select_button_x == l)
                                x += 100
                        y += 50
            elif self.select_window == 5:
                mexture = mextures.Mextures('mixtures/' + str(self.file_name) + '.txt')
                self.quantity[0] = str(len(mexture.matrix.elements_name))
                if mexture.create_answer:
                    self.label[5] = [0, 0]
                    y = 180
                    answer = self.create_answer_format(mexture.answer)
                    for i in range(len(mexture.matrix.elements_name)):
                        text_at_center(screen, font, str(mexture.matrix.elements_name[i]) + ' = ' + str(answer[i]), \
                                       1200 / 2, y + self.step[0] * (-40), self.select_button_y == i and not self.tab)
                        y += 40
                    pygame.draw.rect(screen, WHITE if self.tab else PURPLE, (0, 0, 1200, 140))
                    pygame.draw.rect(screen, GREY_BLUE, (-1, -1, 1200 + 1, 140 + 1), 1)
                    text_at_center(screen, font, "Для составления смеси по вашему запросу, потребуется:", 1200 / 2, 100)
                    pygame.draw.rect(screen, WHITE if self.tab else PURPLE, (0, 420, 1200, 500))
                    pygame.draw.rect(screen, GREY_BLUE, (-1, 420, 1200 + 1, 500 + 1), 1)
                    text_at_center(screen, font, "Итоговая сумма будет равна:  " + str(mexture.summ), 1200 / 2, 450)
                    radio_buttons(screen, font, "Вывести ответ в ...", ['Процентах', "Количествах"], 570, \
                                  self.select_button_x, self.tab and self.select_button_y == 0, self.decision_in)
                    button_with_text(screen, font, "Завершить", 1200 / 4, 630, 1200 / 2, \
                                     self.tab and self.select_button_y == 1)
                else:
                    self.label[5] = [0]
                    text_at_center(screen, font, "Задача не имеет решения", 1200 / 2, 720 / 2 - 50)
                    button_with_text(screen, font, "Завершить", 1200 / 4, 630, 1200 / 2, self.select_button_y == 0)
            elif self.select_window in [0, 2, 6]:
                if self.select_window == 0:
                    y = 300
                for i in range(len(self.label[self.select_window])):
                    button_with_text(screen, font, self.label[self.select_window][i], 1200 / 4,
                                     y - 70 + self.step[0] * -140, 1200 / 2, \
                                     i == self.select_button_y and (not self.tab or self.select_window not in [2, 6]))
                    y += 70
            if self.select_window == 0:
                font = pygame.font.SysFont('Comic Sans MS', 40)
            else:
                font = pygame.font.SysFont('Comic Sans MS', 25)
            if self.select_window in [2, 6]:
                pygame.draw.rect(screen, WHITE if self.tab else PURPLE, (0, 0, 1200, 100))
                pygame.draw.rect(screen, GREY_BLUE, (-1, -1, 1200 + 1, 100 + 1), 1)
            window_name = ["Задача о смесях", "Введите данные:", "Введите названия элементов:", \
                           "Введите данные о целевой функции:", "Введите значения для ячеек:", "", \
                           "Выберите файл с данными для повторного расчета"]
            text_at_center(screen, font, window_name[self.select_window], 1200 / 2, 70)

            if self.select_window in [2, 4, 6]:
                pygame.draw.rect(screen, WHITE if self.tab else PURPLE, (0, 625, 1200, 500))
                pygame.draw.rect(screen, GREY_BLUE, (-1, 626, 1200 + 1, 500 + 1), 1)

                if self.select_window != 6:
                    button_with_text(screen, font, "Далее", 1200 / 4 - 20, 650, 1200 / 4, \
                                     self.tab and self.select_button_x == 0)
                    button_with_text(screen, font, "Назад", 1200 / 2 + 20, 650, 1200 / 4, \
                                     self.tab and self.select_button_x == 1)
                else:
                    button_with_text(screen, font, "Назад", 1200 / 4, 650, 1200 / 2, \
                                     self.tab and self.select_button_x == 0)
                font = pygame.font.SysFont('Comic Sans MS', 20)
                text_at_left(screen, font, "Нажмите: Tab для смены слоя", 1200 / 2 + 1200 / 4 - 20, 20)
            font = pygame.font.SysFont('Comic Sans MS', 20)
            if not self.no_errors:
                text = font.render("Данные введены неверно", True, RED)
                text_rect = text.get_rect(center=(0, 20))
                text_rect.left = 20
                screen.blit(text, text_rect)
            if self.select_window == 5:
                text_at_left(screen, font, "Нажмите: Tab для смены слоя", 1200 / 2 + 1200 / 4 - 20, 20)
            pygame.display.update()
            self.button()

    def button(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if self.select_window != 4:
                        self.select_button_x = 0
                if event.key == pygame.K_TAB and self.select_window not in [0, 1, 3]:
                    self.tab = not self.tab
                    self.select_button_y = 0
                    self.select_button_x = 0
                    self.step = [0, 0]
                if event.key == pygame.K_RETURN:
                    if self.select_window == 0:
                        self.file_name = ""
                        self.quantity = ["", ""]
                        if self.select_button_y == 0:
                            self.label[6] = []
                            for i in os.listdir('mixtures'):
                                self.label[6].append(i.replace('.txt', ''))
                            self.select_window = 6
                        elif self.select_button_y == 1:
                            self.select_window += 1
                            self.select_button_y = 0
                        else:
                            quit()
                    elif self.select_window == 1:
                        if self.select_button_y == 4:
                            self.select_window -= 1
                            self.x_y_0
                        elif self.select_button_y == 3:
                            self.no_errors = True
                            if "" == self.file_name or not is_degit_in_list(self.quantity):
                                self.no_errors = False
                            if self.no_errors:
                                self.label[2] = ["" for i in range(int(self.quantity[0]))]
                                self.target_function = ["" for i in range(int(self.quantity[0]))] + [""]
                                self.components = []
                                for i in range(int(self.quantity[1])):
                                    self.components.append(["" for l in range(int(self.quantity[0]))] + ["=", ""])
                                self.select_window += 1
                                self.x_y_0
                    elif self.select_window in [2, 4, 6] and self.tab:
                        if self.select_button_x == 0:
                            if self.select_window == 2:
                                self.no_errors = True
                                if "" not in self.label[2]:
                                    self.select_window += 1
                                    self.x_y_0
                                else:
                                    self.no_errors = False
                            elif self.select_window == 6:
                                self.select_window = 0
                                self.x_y_0
                            else:
                                self.no_errors = True
                                for i in self.components:
                                    elements = i.copy()
                                    elements.pop(-2)
                                    if i[-2] not in ["=", "<=", ">="] or (not is_degit_in_list(elements) and \
                                                                          not is_degit_float_for_list(elements)):
                                        self.no_errors = False
                                if self.no_errors:
                                    self.create_file
                                    self.select_window += 1
                                    self.x_y_0
                        else:
                            self.select_window -= 1
                            self.x_y_0
                    elif self.select_window == 3:
                        if self.select_button_y == 0:
                            self.direction_objective_function = self.select_button_x
                        elif self.select_button_y == 2:
                            self.no_errors = True
                            if not is_degit_in_list(self.target_function) and \
                                    not is_degit_float_for_list(self.target_function):
                                self.no_errors = False
                            if self.no_errors:
                                self.select_window += 1
                                self.x_y_0
                        elif self.select_button_y == 3:
                            self.select_window -= 1
                            self.x_y_0
                    elif self.select_window == 5 and len(self.label[5]) == 1:
                        self.select_window = 0
                        self.x_y_0
                    elif self.select_window == 5 and self.tab:
                        if self.select_button_y == 0:
                            self.decision_in = self.select_button_x
                        if self.select_button_y == 1:
                            self.select_window = 0
                            self.x_y_0
                    elif self.select_window == 6:
                        self.file_name = self.label[6][self.select_button_y]
                        self.select_window = 5
                        self.x_y_0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    text = {pygame.K_UP: "top", pygame.K_DOWN: "bottom"}
                    if self.select_window == 4:
                        self.top_bottom(text[event.key], len(self.components))
                    elif self.select_window == 5 and len(self.label[5]) != 1 and not self.tab:
                        self.top_bottom(text[event.key], int(self.quantity[0]))
                    elif self.select_window != 2 or not self.tab:
                        self.top_bottom(text[event.key], len(self.label[self.select_window]))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    text = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}
                    if self.tab and self.select_window in [2, 4, 5]:
                        self.left_right(text[event.key], 2)
                    elif self.select_window == 4:
                        self.left_right(text[event.key], len(self.components[0]))
                    elif self.select_window == 3:
                        if self.select_button_y == 0:
                            self.left_right(text[event.key], 2)
                        if self.select_button_y == 1:
                            self.left_right(text[event.key], len(self.components[0]) - 1)
                elif event.key == pygame.K_BACKSPACE:
                    if self.select_window == 4 and not self.tab:
                        self.components[self.select_button_y][self.select_button_x] = \
                            self.components[self.select_button_y][self.select_button_x][:-1]
                    elif self.select_window == 2 and not self.tab:
                        self.label[2][self.select_button_y] = self.label[2][self.select_button_y][:-1]
                    elif self.select_window == 1:
                        if self.select_button_y in [1, 2]:
                            self.quantity[self.select_button_y - 1] = self.quantity[self.select_button_y - 1][:-1]
                        elif self.select_button_y == 0:
                            self.file_name = self.file_name[:-1]
                    elif self.select_window == 3 and self.select_button_y == 1:
                        self.target_function[self.select_button_x] = self.target_function[self.select_button_x][:-1]
                elif self.select_window in [1, 2, 3, 4] and event.key != pygame.K_TAB:
                    if self.select_window == 4 and not self.tab \
                            and len(self.components[self.select_button_y][self.select_button_x]) < 7 and ( \
                                    (self.select_button_x != len(self.components[0]) - 2 and str(
                                        event.unicode) in "0123456789.-") or \
                                    (self.select_button_x == len(self.components[0]) - 2 and str(
                                        event.unicode) in ">=<")):
                        self.components[self.select_button_y][self.select_button_x] += str(event.unicode)
                    elif self.select_window == 2 and not self.tab:
                        self.label[2][self.select_button_y] += str(event.unicode)
                    elif self.select_window == 1:
                        if self.select_button_y in [1, 2] and str(event.unicode) in "0123456789":
                            self.quantity[self.select_button_y - 1] += str(event.unicode)
                        elif self.select_button_y == 0:
                            self.file_name += str(event.unicode)
                    elif self.select_window == 3 and self.select_button_y == 1 and str(event.unicode) in "0123456789.-" \
                            and len(self.target_function[self.select_button_x]) < 6:
                        self.target_function[self.select_button_x] += str(event.unicode)

    @property
    def create_file(self):
        with open('mixtures/' + str(self.file_name) + '.txt', 'w', encoding='utf-8') as f:
            f.write(str(" ".join(self.label[2]) + '\n'))
            mm = ["max", "min"]
            f.write(str(" ".join(self.target_function)) + ' -> ' + mm[self.direction_objective_function] + '\n')
            for i in self.components:
                f.write(str(" ".join(i)) + '\n')
            elem = ['1' for l in range(len(self.label[2]))]
            f.write(str(' '.join(elem)) + ' = 1\n')
            for i in range(len(self.label[2])):
                elem = ['0' for l in range(len(self.label[2]))]
                elem[i] = '1'
                f.write(str(' '.join(elem)) + ' <= 1\n')
                f.write(str(' '.join(elem)) + ' >= 0\n')

    @property
    def x_y_0(self):
        self.no_errors = True
        self.select_button_y = 0
        self.select_button_x = 0
        self.step = [0, 0]
        self.tab = False

    def top_bottom(self, orientation, count):
        if orientation == "top":
            self.select_button_y -= 1
            if count > 7 and self.select_button_y < count - 6 and self.step[0] != 0:
                self.step[0] -= 1
            if self.select_button_y < 0:
                self.select_button_y = count - 1
                if count > 7:
                    self.step[0] = count - 7
        else:
            self.select_button_y += 1
            if count > 7 and self.step[0] != count - 7:
                self.step[0] += 1
            if self.select_button_y == count:
                self.select_button_y = 0
                self.step[0] = 0

    def left_right(self, orientation, count):
        if orientation == "left":
            self.select_button_x -= 1
            if count > 10 and self.select_button_x < count - 9:
                self.step[1] -= 1
            if self.select_button_x < 0:
                self.select_button_x = count - 1
                if count > 10:
                    self.step[1] = count - 10
        else:
            self.select_button_x += 1
            if count > 10 and self.step[1] != count - 10:
                self.step[1] += 1
            if self.select_button_x == count:
                self.select_button_x = 0
                self.step[1] = 0

    def create_answer_format(self, mexture):
        if self.decision_in == 1:
            return mexture
        elif self.decision_in == 0:
            for i in range(len(mexture)):
                mexture[i] = str(round(mexture[i] * 100)) + '%'
            return mexture


pygame.init()
WIGHT, HEIGHT = 1200, 720
screen = pygame.display.set_mode((1200, 720), pygame.SCALED)

wind = Window()
wind.window(screen)
