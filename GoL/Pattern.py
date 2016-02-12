# 1.4 importowanie biblioteka standardowa
from functools import total_ordering


# 2.1 definiowanie klas, 2.4 zastosowanie dekoratorow
@total_ordering  # dekorator klasy , z == i < robi wszystkie porownania
class Pattern:

    def __init__(self, board, **kwargs):  # konstruktor
        self._color = "#"  # podstawowy kolor #
        self.cells_count = 0  # liczba komorek
        # jesli konstruktor wygladal np new_pattern = Pattern(board, color="R")
        if "color" in kwargs:
            self._color = kwargs["color"]  # to _color = "R"
        self.body = [[self._color if c == "#" else "." for c in line]
                     for line in board]  # ustawianie schematu w obiekcie
        #  zliczanie zywych komorek
        for line in self.body:
            for c in line:
                if c == self._color:
                    self.cells_count += 1
    # 2.2 metody realizujace operatory
    #  wywolywana przy np print(moj_pattern[3][2])

    def __getitem__(self, index):
        return self.body[index]

    #  wywolywana przy np moj_pattern[3, 2] = "."
    def __setitem__(self, index, val):
        if len(index) == 2:  # moj_pattern[3,2]
            if val != "." and val != self._color:
                raise ValueError()
            #  ponizsze ify sa do wyliczenia nowej ilosci zywych komorek
            if val == "." and self.body[index[0]][index[1]] != ".":
                self.cells_count -= 1
            elif val != "." and self.body[index[0]][index[1]] == ".":
                self.cells_count += 1
            # zamien wartos tablicy na nowa
            self.body[index[0]][index[1]] = val
        elif len(index) == 1:  # moj_pattern[3]
            # bedziemy zamieniac caly wiersz
            if len(self.body[index[0]]) != len(val) or \
                    any(map(lambda x: x != "." and x != self.color, val)):
                # jesli wiersz posiada zle znaki to rzuc wyjatek
                raise ValueError()
            # wyliczenie nowej ilosci komorek
            for c, n in zip(self.body[index[0]], val):
                if c != n:
                    if c == ".":
                        self.cells_count += 1
                    else:
                        self.cells_count -= 1
            # zamiana wiersza
            self.body[index[0]] = val

    # 2.3 properties
    # getter
    @property
    def color(self):
        return self._color

    # setter
    @color.setter
    def color(self, new_color):
        # nastepuje przy np. moj_pattern.color = "R"
        # zmienia wartos self._color
        # oraz wszystkie znaki w body na odpowiedni kolor
        for i in range(len(self.body)):
            for j in range(len(self.body[i])):
                if self.body[i][j] != ".":
                    self.body[i][j] = new_color
        self._color = new_color

    # deleter
    @color.deleter
    def color(self):
        # zamiast usuwac ustawiamy na default
        self.color = "#"

    # 2.1 metody klas
    # 1.2 rozne sposoby przekazywania parametrow
    # 5.2 klasy jako argumenty (do tworzenia instancji)(cls to klasa)
    # metody konstruuja obiekt odpowiednio z
    # pliku
    @classmethod
    def fromfile(cls, file, **kwargs):
        # 3.3 listy skladane
        board = [list(line) for line in file.readlines()]
        return cls(board, **kwargs)

    # stringa
    @classmethod
    def fromstr(cls, in_str, **kwargs):
        # 3.3 listy skladane
        board = [list(line)[:-1] for line in in_str.split("\n")]
        return cls(board[:-1], **kwargs)

    # len(moj_pattern)
    def __len__(self):
        return len(self.body)

    # pattern1 == pattern2
    def __eq__(self, other):
        # 5.3 badanie typow argumentow
        if type(self) == type(other):
            return self.cells_count == other.cells_count
        else:
            raise NotImplementedError()

    # pattern1 < pattern2
    def __lt__(self, other):
        # 5.3 badanie typow argumentow
        if type(self) == type(other):
            return self.cells_count < other.cells_count
        else:
            raise NotImplementedError()
    # total_ordering generuje reszte porownan

    # print moj_pattern
    def __str__(self):
        s = ""
        for x in self.body:
            s = s + "".join(x) + "\n"
        return s
