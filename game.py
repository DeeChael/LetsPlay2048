from enum import IntEnum
from random import choice, randrange
from typing import Dict, Tuple, Union


class Game2048:
    field: Dict[int, Dict[int, int]] = dict()
    owner: str

    def __init__(self, owner: str = None):
        self.owner = owner
        for x in range(0, 4):
            self.field[x] = dict()
            for y in range(0, 4):
                self.field[x][y] = 0
        self.spawn()

    def can_go_on(self) -> bool:
        emptys = self._empties()
        if emptys > 0:
            return True
        for x in range(4):
            p1 = self.field[x][0]
            p2 = self.field[x][1]
            p3 = self.field[x][2]
            p4 = self.field[x][3]
            if p1 == p2:
                return True
            elif p2 == p3:
                return True
            elif p3 == p4:
                return True
        self.rotate_left()
        for x in range(4):
            p1 = self.field[x][0]
            p2 = self.field[x][1]
            p3 = self.field[x][2]
            p4 = self.field[x][3]
            if p1 == p2:
                self.rotate_right()
                return True
            elif p2 == p3:
                self.rotate_right()
                return True
            elif p3 == p4:
                self.rotate_right()
                return True
        self.rotate_right()
        self.rotate_right()
        for x in range(4):
            p1 = self.field[x][0]
            p2 = self.field[x][1]
            p3 = self.field[x][2]
            p4 = self.field[x][3]
            if p1 == p2:
                self.rotate_left()
                return True
            elif p2 == p3:
                self.rotate_left()
                return True
            elif p3 == p4:
                self.rotate_left()
                return True
        self.rotate_left()
        return False

    def move_left(self):
        for x in range(4):
            p1 = self.field[x][0]
            p2 = self.field[x][1]
            p3 = self.field[x][2]
            p4 = self.field[x][3]
            if p1 > 0 and p2 > 0:
                if p1 == p2:
                    p1 = p1 * 2
                    p2 = 0
                    if p3 > 0 and p4 > 0:
                        if p3 == p4:
                            p2 = p3 * 2
                            p3 = 0
                            p4 = 0
                        else:
                            p2 = p3
                            p3 = p4
                            p4 = 0
                    elif p3 > 0:
                        p2 = p3
                        p3 = 0
                        p4 = 0
                    elif p4 > 0:
                        p2 = p4
                        p3 = 0
                        p4 = 0
                else:
                    if p2 == p3:
                        p2 = p2 * 2
                        p3 = p4
                        p4 = 0
                    else:
                        if p3 > 0 and p4 > 0:
                            if p3 == p4:
                                p3 = p3 * 2
                                p4 = 0
                        elif (not p3 > 0) and p4 > 0:
                            if p2 == p4:
                                p2 = p2 * 2
                                p3 = 0
                                p4 = 0
                            else:
                                p3 = p4
                                p4 = 0
            elif p1 > 0:
                if p3 > 0:
                    if p1 == p3:
                        p1 = p1 * 2
                        p2 = p4
                        p3 = 0
                        p4 = 0
                    else:
                        if p3 == p4:
                            p2 = p3 * 2
                            p3 = 0
                            p4 = 0
                        else:
                            p2 = p3
                            p3 = p4
                            p4 = 0
                else:
                    if p1 == p4:
                        p1 = p1 * 2
                        p2 = 0
                        p3 = 0
                        p4 = 0
                    else:
                        p2 = p4
                        p3 = 0
                        p4 = 0
            elif p2 > 0:
                if p3 > 0:
                    if p2 == p3:
                        p1 = p2 * 2
                        p2 = p4
                        p3 = 0
                        p4 = 0
                    else:
                        if p3 == p4:
                            p1 = p2
                            p2 = p3 * 2
                            p3 = 0
                            p4 = 0
                        else:
                            p1 = p2
                            p2 = p3
                            p3 = p4
                            p4 = 0
                else:
                    if p2 == p4:
                        p1 = p2 * 2
                        p2 = 0
                        p3 = 0
                        p4 = 0
                    else:
                        p1 = p2
                        p2 = p4
                        p3 = 0
                        p4 = 0
            else:
                if p3 > 0 and p4 > 0:
                    if p3 == p4:
                        p1 = p3 * 2
                        p2 = 0
                        p3 = 0
                        p4 = 0
                    else:
                        p1 = p3
                        p2 = p4
                        p3 = 0
                        p4 = 0
                elif p3 > 0:
                    p1 = p3
                    p2 = p4
                    p3 = 0
                    p4 = 0
                else:
                    p1 = p4
                    p2 = 0
                    p3 = 0
                    p4 = 0
            self.field[x][0] = p1
            self.field[x][1] = p2
            self.field[x][2] = p3
            self.field[x][3] = p4
        self.spawn()

    def move_up(self):
        self.rotate_left()
        self.move_left()
        self.rotate_right()

    def move_down(self):
        self.rotate_right()
        self.move_left()
        self.rotate_left()

    def move_right(self):
        self.rotate_left()
        self.rotate_left()
        self.move_left()
        self.rotate_right()
        self.rotate_right()

    def can_move_left(self) -> bool:
        for x in range(4):
            p1 = self.field[x][0]
            p2 = self.field[x][1]
            p3 = self.field[x][2]
            p4 = self.field[x][3]
            if p1 == 0:
                return p2 != 0 or p3 != 0 or p4 != 0
            elif p2 == 0:
                return p3 != 0 or p4 != 0
            elif p3 == 0:
                return p4 != 0
        return False

    def can_move_up(self) -> bool:
        self.rotate_left()
        result = self.can_move_left()
        self.rotate_right()
        return result

    def can_move_down(self) -> bool:
        self.rotate_right()
        result = self.can_move_left()
        self.rotate_left()
        return result

    def can_move_right(self) -> bool:
        self.rotate_left()
        self.rotate_left()
        result = self.can_move_left()
        self.rotate_right()
        self.rotate_right()
        return result

    def rotate_left(self):
        new_field = dict()
        for x in range(0, 4):
            new_field[x] = dict()
            for y in range(0, 4):
                new_field[x][y] = 0
        for x in range(0, 4):
            for y in range(0, 4):
                new_field[x][y] = self.field[y][3 - x]
        self.field = new_field

    def rotate_right(self):
        new_field = dict()
        for x in range(0, 4):
            new_field[x] = dict()
            for y in range(0, 4):
                new_field[x][y] = 0
        for x in range(0, 4):
            for y in range(0, 4):
                new_field[x][y] = self.field[3 - y][x]
        self.field = new_field

    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        position = self._random_emtpy_position()
        if position is None:
            return
        (i, j) = position
        self.field[i][j] = new_element

    def _random_emtpy_position(self) -> Union[Tuple, None]:
        if self._empties() == 0:
            return None
        return choice([(i, j) for i in range(4) for j in range(4) if self.field[i][j] == 0])

    def _empties(self) -> int:
        empties = 0
        for x in range(0, 4):
            for y in range(0, 4):
                if self.field[x][y] == 0:
                    empties += 1
        return empties

    def has_2048(self) -> bool:
        for x in range(0, 4):
            for y in range(0, 4):
                if self.field[x][y] == 2048:
                    return True
        return False


class GameTicTacToe:
    field: Dict[int, Dict[int, int]] = dict()
    circle: str
    cross: str
    turn: int = 1

    def __init__(self, circle: str, cross: str):
        self.circle = circle
        self.cross = cross
        for x in range(0, 3):
            self.field[x] = dict()
            for y in range(0, 3):
                self.field[x][y] = 0

    def has_winner(self) -> bool:
        p1 = self.field[0][0]
        p2 = self.field[0][1]
        p3 = self.field[0][2]
        p4 = self.field[1][0]
        p5 = self.field[1][1]
        p6 = self.field[1][2]
        p7 = self.field[2][0]
        p8 = self.field[2][1]
        p9 = self.field[2][2]
        if p1 == p2 == p3:
            return p1 == 1 or p1 == 2
        if p4 == p5 == p6:
            return p4 == 1 or p4 == 2
        if p7 == p8 == p9:
            return p7 == 1 or p7 == 2
        if p1 == p4 == p7:
            return p1 == 1 or p1 == 2
        if p2 == p5 == p8:
            return p2 == 1 or p2 == 2
        if p3 == p6 == p9:
            return p3 == 1 or p3 == 2
        if p1 == p5 == p9:
            return p1 == 1 or p1 == 2
        if p3 == p5 == p7:
            return p3 == 1 or p3 == 2
        return False

    def is_end(self) -> bool:
        for x in range(0, 3):
            for y in range(0, 3):
                if self.field[x][y] == 0:
                    return False
        return True

    def get_winner(self) -> int:
        p1 = self.field[0][0]
        p2 = self.field[0][1]
        p3 = self.field[0][2]
        p4 = self.field[1][0]
        p5 = self.field[1][1]
        p6 = self.field[1][2]
        p7 = self.field[2][0]
        p8 = self.field[2][1]
        p9 = self.field[2][2]
        if p1 == p2 == p3 > 0:
            return p1
        if p4 == p5 == p6 > 0:
            return p4
        if p7 == p8 == p9 > 0:
            return p7
        if p1 == p4 == p7 > 0:
            return p1
        if p2 == p5 == p8 > 0:
            return p2
        if p3 == p6 == p9 > 0:
            return p3
        if p1 == p5 == p9 > 0:
            return p1
        if p3 == p5 == p7 > 0:
            return p3
        return 0

    def set_circle(self, position: int):
        x = position // 3
        y = position - (3 * (position // 3))
        self.field[x][y] = 1
        self.turn = 2

    def set_cross(self, position: int):
        x = position // 3
        y = position - (3 * (position // 3))
        self.field[x][y] = 2
        self.turn = 1

    def next_clicker(self) -> int:
        return self.turn


class GameFiveInRow:
    field: Dict[int, Dict[int, int]] = dict()

    def __init__(self):
        for x in range(0, 19):
            for y in range(0, 19):
                self.field[x][y] = 0

    def has_winner(self):

        ...


class ChineseChessPiecesType(IntEnum):
    NONE = 0
    SHUAI = 11
    JIANG = 12
    BING = 101
    ZU = 102
    PAO_RED = 111
    PAO_BLACK = 112
    JU_RED = 121
    JU_BLACK = 122
    MA_RED = 131
    MA_BLACK = 132
    XIANG_RED = 141
    XIANG_BLACK = 142
    SHI_RED = 151
    SHI_BLACK = 152


class ChineseChessPieces:
    type: ChineseChessPiecesType
    x: int
    y: int

    def __init__(self, type: ChineseChessPiecesType, x: int, y: int):
        self.type = type

    def can_go_to(self, dx: int, dy: int) -> bool:
        ...


class GameChineseChess:
    field: Dict[int, Dict[int, ChineseChessPieces]] = dict()

    def __init__(self):
        for x in range(0, 9):
            for y in range(0, 9):
                self.field[x][y] = ChineseChessPieces(ChineseChessPiecesType.NONE, x, y)

    def can_go_to(self, ox, oy, dx, dy):
        ...


