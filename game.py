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
