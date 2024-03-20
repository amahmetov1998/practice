from random import randint


class Cell:
    def __init__(self, mine: int, around_mines: int = 0) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

    @property
    def around_mines(self) -> int:
        return self.__around_mines

    @around_mines.setter
    def around_mines(self, value: int) -> None:
        if 0 <= value <= 8:
            self.__around_mines = value
        else:
            raise ValueError("Количество мин должно быть в диапазоне от 0 до 9")

    @property
    def fl_open(self) -> bool:
        return self.__fl_open

    @fl_open.setter
    def fl_open(self, value: bool) -> None:
        self.__fl_open = value

    @property
    def mine(self) -> int:
        return self.__mine

    @mine.setter
    def mine(self, value: int) -> None:
        if value in (0, 1):
            self.__mine = value
        else:
            raise TypeError("Значение должно быть целым числом")


class GamePole:
    def __init__(self, N: int, M: int) -> None:
        self._N, self._M = N, M
        self.__pole = [[Cell(mine=0) for _ in range(self._N)] for _ in range(self._N)]
        self.__init()

    def __init(self) -> None:

        self.__set_mines()

        indexes = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
        for i in range(self._N):
            for j in range(self._N):
                if not self.__pole[i][j].mine:
                    mine_count = sum(self.__pole[i+x][j+y].mine for x, y in indexes
                                     if 0 <= i+x <= len(self.__pole)-1 and 0 <= j+y <= (len(self.__pole))-1
                                     )
                    self.__pole[i][j].around_mines = mine_count

    def __set_mines(self) -> None:
        while self._M != 0:
            i = randint(0, self._N-1)
            j = randint(0, self._N-1)
            if not self.__pole[i][j].mine:
                self.__pole[i][j].mine = 1
                self._M -= 1

    def show(self) -> None:
        for row in self.__pole:
            res = []
            for cell in row:
                if cell.mine:
                    res.append('*')
                else:
                    res.append('#')
            print(' '.join(res))


pole_game = GamePole(10, 12)
pole_game.show()
