from random import randint


class Cell:
    def __init__(self, mine, around_mines=0):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    def __init__(self, N, M):
        self.N, self.M = N, M
        self.pole = [[Cell(mine=0) for _ in range(self.N)] for _ in range(self.N)]
        self.init()

    def init(self):

        self.set_mines()

        indexes = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
        for i in range(self.N):
            for j in range(self.N):
                if not self.pole[i][j].mine:
                    mine_count = sum(self.pole[i+x][j+y].mine for x, y in indexes
                                     if 0 <= i+x <= len(self.pole)-1 and 0 <= j+y <= (len(self.pole))-1
                                     )
                    self.pole[i][j].around_mines = mine_count

    def set_mines(self):
        while self.M != 0:
            i = randint(0, self.N-1)
            j = randint(0, self.N-1)
            if not self.pole[i][j].mine:
                self.pole[i][j].mine = 1
                self.M -= 1

    def show(self):
        for row in self.pole:
            res = []
            for cell in row:
                if cell.mine:
                    res.append('*')
                else:
                    res.append('#')
            print(' '.join(res))


pole_game = GamePole(10, 12)
pole_game.show()
