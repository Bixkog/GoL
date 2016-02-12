import random
from itertools import count
from copy import copy


class GameOfLife:
    # 2.1 statyczne metody
    # printuje plik settings
    @staticmethod
    def print_settings():
        with open("settings") as file:
            print(file.read())

    # 2.1 statyczne metody
    # printuje plik help
    @staticmethod
    def print_help():
        with open("help") as file:
            print(file.read())

    # konstruktor
    def __init__(self, setting, size):
        # zamienia string setting np. 23/3
        self.life_list, self.raise_list = setting.split("/")
        self.raise_list = [int(c) for c in self.raise_list]
        self.life_list = [int(c) for c in self.life_list]
        # dwie listy [2, 3] i [3]
        # zainicjalisuj pusta plansze
        self.board = [["." for i in range(size)] for j in range(size)]
        # zapamietaj wielkosc
        self.size = size

    # losuj plansze
    def init_board(self, n):
        for i in range(self.size):
            for j in range(self.size):
                # wylosuj czy zywa czy martwa komorka
                if random.randint(0, n):
                    self.board[i][j] = '.'
                else:
                    self.board[i][j] = "#"

    # wstaw pattern
    def insert(self, pattern, *args):
        if len(args) == 0:  # nie podano pozycji
            # losuj pozycje
            args = [random.randint(0, self.size - len(pattern)),
                    random.randint(0, self.size - max(
                        [len(x) for x in pattern.body]))]
        if len(args) != 2:  # nie podano dokladnie 2 argumentow pozycji(x, y)
            raise ValueError(
                " insert needs 3 or 1 positional arguments")  # wyjatek
        # wstaw na wybrana pozycje pattern
        print(args)
        print(pattern.body)
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                # x = args[0] y = args[1]
                self.board[args[0] + i][args[1] + j] = pattern[i][j]

    # zwijanie planszy
    # boki i rogi planszy sa polaczone
    # lewy z prawym
    # gorny z dolnym
    # i ukosne rogi
    def join_board(self):
        # zrob kopie planszy
        tempboard = copy(self.board)
        # dla kazdego wiersza
        for i in range(len(tempboard)):
            # dodaj jego koniec na poczatek i poczatek na koniec
            # np [1, 2, 3, 4] na [4, 1, 2, 3, 4, 1]
            tempboard[i] = [tempboard[i][-1]] + \
                tempboard[i] + [tempboard[i][0]]
        # jak na wyzej tylko gora na dol i dol na gore
        tempboard = [self.board[-1]] + tempboard
        tempboard = tempboard + [self.board[0]]

        # jak wyzej tylko z rogami
        tempboard[0] = [tempboard[-2][-2]] + \
            tempboard[0][:] + [tempboard[-2][1]]
        tempboard[-1] = [tempboard[1][-2]] + \
            tempboard[-1][:] + [tempboard[1][1]]
        # zwroc powiekszana
        # ta plansza jest uzywana tylko do wyliczania kolejnych iteracji
        return tempboard

    # dla danej komorki na pozycji (h, w)
    # zwraca (C, q) gdzie
    # C to najczesciej wystepujacy wokol niej kolor
    # q to ilosc zywych komorek wokol niej
    def count_alive(self, h, w):
        # 1.1 wykorzystywanie standardowych zlozonych typow danych
        # dictionary, slownik
        colors_counter = {}
        counter = 0
        # jesli dana komorka nie jest zywa to odejmujemy 1
        # aby nie liczyc jej do ilosci sasiadow
        if self.tempboard[h + 1][w + 1] != ".":
            colors_counter[self.tempboard[h + 1][w + 1]] = -1
            counter = -1
        # dla wszystkich sasiadow danej komorki
        # z nia wlacznie, dlatego ja wczesniej odjelismy
        for i in range(0, 3):
            for j in range(0, 3):
                # jesli sasiad jest zywy
                if self.tempboard[h + i][w + j] != ".":
                    # jesli kolor sasiada jest juz w slowniku
                    if self.tempboard[h + i][w + j] in colors_counter:
                        # dodaj do koloru sasiada 1
                        colors_counter[self.tempboard[h + i][w + j]] += 1
                        # i do calkowitej ilosci 1
                        counter += 1
                    else:  # nie ma tego koloru sasiada
                        # ustaw slownik na tym kolorze na 1
                        colors_counter[self.tempboard[h + i][w + j]] = 1
                        # do calkowitej ilosci 1
                        counter += 1
        # print(h, w , counter)
        # jesli byla zywa lub miala w ogole jakichs sasiadow
        if colors_counter:
            # max po ilosci danego koloru
            # 3.1 definiowanie lambdy
            return (max(list(colors_counter.items()),
                        key=lambda p: p[1])[0],  # to zwroc (C, q)
                    counter)
        else:
            return ("#", 0)

    # podaj nowy stan dla danej komorki
    def next_state(self, x, y, current_state):
        new_state = current_state
        # new_color = C i alive_n = q z poprzedniej funkcji
        new_color, alive_n = self.count_alive(x, y)
        # przepisanie z definicji z wikipedi
        if current_state != "." and alive_n not in self.life_list:
            new_state = "."
        elif current_state == "." and alive_n in self.raise_list:
            new_state = new_color
        elif current_state != "." and alive_n in self.life_list:
            new_state = new_color
        else:
            new_state = "."
        return new_state

    # zmien opcje gry np 23/3 na /2
    # 5.4 dynamiczna zmiana wlasciosci
    def change_setting(self, new_setting):
        # to samo co w konstruktorze tej klasy
        self.life_list, self.raise_list = new_setting.split("/")
        self.raise_list = [int(c) for c in self.raise_list]
        self.life_list = [int(c) for c in self.life_list]

    # 4.1 generatory proste oraz klasy realizujace protokol iteracji
    def __iter__(self):
        # count(0) -> 4.3 modul itertools
        for i in count(0):
            yield i
            self.tempboard = self.join_board()
            for i, x in enumerate(self.board):
                for j, y in enumerate(x):
                    self.board[i][j] = self.next_state(i, j, y)

    # do printowania boarda
    def __str__(self):
        s = ""
        for line in self.board:
            s = s + " ".join(line) + "\n"
        return s[:-1]
