# 1.3 definiowanie modulow i paczek modulow
from GoL.Pattern import Pattern
from GoL.GameOfLife import GameOfLife


# 3.4 definiowanie dekoratorow
def coloredPattern(constructor, set_color):
    # 3.1 definiowanie funkcji wewnetrznych
    def new_constructor(board):
        return constructor(board, color=set_color)
    return new_constructor

# utworzenie defaultowych konstruktorow dzieki dekoratorowi
# uzywane kiedy nie podamy koloru wzorca
defaultPatternStr = coloredPattern(Pattern.fromstr, "#")
defaultPatternFile = coloredPattern(Pattern.fromfile, "#")

# cos jak int main(){ w c++
if __name__ == "__main__":
    # stworzenie gry, 23/3 to zasady, 56 to rozmiar planszy
    game = GameOfLife("23/3", 56)
    # slownik do zapamietywania stworzonych patternow
    patterns = {}
    # iteracja po grze
    # kazde przejscie po forze skutkuje jej zmiana
    for x in game:
        # printuj numer iteracji
        print(x)
        # pokaz plansze
        print(game)
        command = raw_input("Command: ")
        # dopoki komenda nie jest pusta, samym enterem
        while command:
            # try do lapania wyjatkow
            try:
                # dzielimy komende na liste slow
                # nizej ify szukaja jaka komende wpisalismy
                # najpierw musimy sprawdzic ilosc slow w komendzie
                # czy jest odpowiednia
                # pozniej jakie to slowa
                # \ sluzy do lamania lini, zeby nie bylo dlugich linijek
                # " ".join(command[:2]) laczy odpowiednio dwa pierwsze slowa
                # len(command) in (4, 5) ilosc slow nalezy do {4, 5}
                command = command.split()
                if len(command) == 3 and \
                        " ".join(command[:2]) == "change setting":
                    # change setting 12345/3
                    # najciekawsza komenda
                    game.change_setting(command[2])

                elif len(command) in (2, 4) and \
                        command[0] == "insert":
                    # insert glider
                    if len(command) == 2:
                        game.insert(patterns[command[1]])
                    # insert glider 10 10
                    else:
                        game.insert(patterns[command[1]],
                                    int(command[2]), int(command[3]))
                    # pokaz plansze(zmieniona tylko o dodany pattern)
                    print(game)
                elif len(command) in (4, 5) and \
                        " ".join(command[:2]) == "create pattern" and \
                        (command[3] == "string" or command[3] == "file"):
                    # create pattern glider string
                    if command[3] == "string":
                        # wpisywanie wzorca
                        s = ""
                        # x to linijka
                        x = raw_input()
                        while x != "b":
                            s = s + x + "\n"
                            x = raw_input()
                        # create pattern glider string R
                        if len(command) == 5:
                            patterns[command[2]] = Pattern.fromstr(
                                s, color=command[4])
                        # create pattern glider string
                        else:
                            patterns[command[2]] = defaultPatternStr(s)
                    # create pattern glider file
                    else:
                        # podaj nazwe pliku
                        file_name = raw_input("File name: ")
                        # bezpieczne otwieranie pliku = fh
                        with open(file_name) as fh:
                            # create pattern glider file R
                            if len(command) == 5:
                                patterns[command[2]] = Pattern.fromfile(
                                    fh, color=command[4])
                            # create pattern glider file
                            else:
                                patterns[command[2]] = defaultPatternFile(fh)

                elif len(command) == 2 and command[0] == "random":
                    # random 4
                    game.init_board(int(command[1]))
                    print(game)
                elif len(command) == 3 and \
                        " ".join(command[:2]) == "default color":
                    # default color R
                    # stworz nowe konstruktory z nowym kolorem
                    defaultPatternStr = coloredPattern(
                        Pattern.fromstr, command[2])
                    defaultPatternFile = coloredPattern(
                        Pattern.fromfile, command[2])
                elif len(command) == 1 and command[0] == "settings":
                    # settings
                    GameOfLife.print_settings()
                elif len(command) == 1 and command[0] == "help":
                    # help
                    GameOfLife.print_help()
                elif len(command) == 1 and command[0] == "q":
                    # q
                    break
                else:
                    # wpisana komenda nigdzie nie pasuje
                    print("Wrong Command: See help")
            except Exception as e:
                # lapie wyjatek jezeli jakies argumenty(nie komendy) byly zle
                # np. random rower (string a nie liczba)
                print(e)
                print("Wrong arguments")
            finally:
                if len(command) == 1 and command[0] == "q":
                    break
                # wpisz nowa komende
                command = raw_input("Command: ")
        if len(command) == 1 and command[0] == "q":
            break
