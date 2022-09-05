from copy import deepcopy
from re import S
from threading import Lock
import random
from functools import reduce
import maze_generator

Rooms = list[list[int]]

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class House(metaclass=SingletonMeta):

    def __init__(self, height=3, width=3, gen_type=0) -> None:
        self.dim = [height, width]
        self.__ruined = 0
        self.rooms = self.generate_rooms() if gen_type == 0 else self.generate_maze()

    def generate_rooms(self,

                       ruin_percent: float = 0.6

                       ) -> Rooms:
        '''
        function generates field of ones and zeros
        field of dim size surrounded by wall of zeros
        then, part of ones is transformed into zeros
        main rule is all ones should be connected
        to each other
        '''
        dim = self.dim
        rooms = self.__generate_all_rooms_with_walls(dim)
        for i in range(len(rooms)):
            for j in range(len(rooms[0])):
                # rooms[row][column]
                if rooms[i][j]:
                    self.__randomly_destroy_room(
                        [i, j], rooms, ruin_percent=ruin_percent
                    )
        return rooms

    @staticmethod
    def __generate_all_rooms_with_walls(

        dim: list[int, int]

    ) -> Rooms:
        '''
        if dim(2, 3) ->
        [[0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]]
        dim = [row, column]
        '''
        return [[0] * (dim[1] + 2)] + [
            [0] + [1 for i in range(dim[1])] + [0] for j in range(dim[0])
        ] + [[0] * (dim[1] + 2)]

    @staticmethod
    def __get_neighbours(

        pos: list[int, int],
        rooms: Rooms

    ) -> int:
        '''
        function returns the number of non-zero rooms
        up, down, left and right to the room
        '''
        neigh_cords = (
            (-1, 0), (0, -1), (1, 0), (0, 1)
        )
        neigh_num = 0
        for i in neigh_cords:
            if rooms[pos[0] + i[0]][pos[1] + i[1]]:
                neigh_num += 1
        return neigh_num

    def __randomly_destroy_room(self,

                                dim: list[int, int],
                                rooms: Rooms,
                                ruin_percent: float

                                ) -> None:
        '''
        function replaces 1 rooms with 0 rooms
        randomly using ruin_percent as a probability
        no more than field size * ruin_percent times
        '''
        forbidden_matrix_pos = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1)
        )
        forbidden_patterns = [
            [[1, 0, 0, 1], [1, 2, 3], [1, 2, 3]],
            [[0, 1, 0, 1], [2, 3, 4], [1, 2]],
            [[0, 0, 1, 1], [2, 3], [1, 2]],
            [[0, 1, 0, 0], [2, 3], [1, 2]],
            [[1, 1, 0, 1], [2, 3], [1, 2, 3]],
            [[0, 0, 0, 1], [2], [1, 2]],
            [[1, 0, 1, 1], [2], [1, 2, 3]],
            [[0, 1, 1, 1], [3, 4], [2, 3]],
            [[0, 1, 1, 0], [3], [2]],
            [[1, 1, 0, 0], [2], [3]]
            # [[0, 0, 0, 0],[0], [2]]
        ]
        allow_destruction = True

        real_pattern = []
        for pos in forbidden_matrix_pos:
            real_pattern.append(
                rooms[dim[0] + pos[0]][dim[1] + pos[1]]
            )

        real_neigh_num = self.__get_neighbours([dim[0], dim[1]], rooms=rooms)
        real_neigh_num_up = self.__get_neighbours([dim[0] - 1, dim[1]], rooms=rooms)

        for pattern, neigh_num, neigh_num_up in forbidden_patterns:
            if pattern == real_pattern and real_neigh_num in neigh_num and real_neigh_num_up in neigh_num_up:
                allow_destruction = False
                break
        destruction_conditions_justified = [
            random.random() < ruin_percent,
            self.__ruined < int((dim[0] * dim[1]) * ruin_percent),
            allow_destruction
        ]
        if all(destruction_conditions_justified):
            rooms[dim[0]][dim[1]] = 0
            self.__ruined += 1

    def generate_maze(self):
        maze = maze_generator.get_maze(self.dim[1] + 2, self.dim[0] + 2)
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 'w' or i in [0, len(maze) - 1] or j in [0, len(maze[0]) - 1]:
                    maze[i][j] = 0
                elif maze[i][j] in ['u', 'c']:
                    maze[i][j] = 1
        return maze


class RoomNameGenerator(House, metaclass=SingletonMeta):
    def __init__(self, height: int =3, width: int =3, gen_type=0) -> None:
        super().__init__(height, width, gen_type)
        self.named_rooms = self.generate_room_names()
        self.how_many_generate = 0

    def generate_room_names(self) -> list[list[str | int]]:
        tokens = [
            'Спальня',
            'Цех',
            'Кухня',
            'Коридор',
            'Склад грязи'
        ]
        self.how_many_generate = reduce(
            lambda x, y: x + y,
            [reduce(lambda x, y: x + y, row) for row in self.rooms]
        )

        list_of_names = []
        for i in range(self.how_many_generate):
            count = 1
            name = random.choice(tokens)
            while name in list_of_names:
                count += 1
                name = f'{random.choice(tokens)} #{count}'
            list_of_names.append(name)
        named_rooms = deepcopy(self.rooms)
        counter = 0
        for i in range(len(named_rooms)):
            for j in range(len(named_rooms[0])):
                if named_rooms[i][j]:
                    named_rooms[i][j] = list_of_names[counter]
                    counter += 1
        
        named_rooms[0][0] = 'той же комнате' # [0, 0] are cords when you tried to go in wall

        return named_rooms



class GameGenerator(RoomNameGenerator, metaclass=SingletonMeta):
    def __init__(self, height: int = 3, width: int = 3, gen_type=0) -> None:
        super().__init__(height, width, gen_type)
        self.start_location = self.__set_start_location(self.rooms)
        self.player_location = deepcopy(self.start_location)
        self.end_location = self.__set_end_location(self.rooms)
        self.list_of_events = self.generate_events()
    

    @staticmethod
    def __set_start_location(rooms: Rooms) -> list[int, int]:
        while True:
            y, x = random.randint(
                1, len(rooms) - 1), random.randint(1, len(rooms[0]) // 2)
            if rooms[y][x]:
                return [y, x]

    @staticmethod
    def __set_end_location(rooms: list[list[int]]) -> list[int, int]:
        while True:
            y, x = random.randint(
                1, len(rooms) - 1), random.randint(len(rooms[0]) // 2, len(rooms[0]) - 1)

            if rooms[y][x]:
                return [y, x]


    def generate_events(self):
        events_in_rooms: list[list[dict]] = deepcopy(self.rooms)
        event_list = {
            'random': {
                'Empty event' : {
                    'name': '',
                    'cords': [],
                    'conditions': [],
                    'description': '',
                    'action': ''
                    },
                'Monster' : {
                    'name': 'Монстр',
                    'cords': [],
                    'conditions': [],
                    'description': '',
                    'action': ''
                    },
                'Heal' : {
                    'name': 'Лечение',
                    'cords': [],
                    'conditions': [],
                    'description': '',
                    'action': ''
                }
        },
            'default' : {
                0: 'Вы уперлись в глухую стену',
                1: 'Вы прошли игру'
            }
        }
        pass

class Renderer():
    def __init__(self):
        pass

    def render_game(self,
        rooms: Rooms,
        start_pos: list[int, int], end_pos: list[int, int], player_pos: list[int, int],
        visited_rooms: list[list[int, int]]
        ) -> list[list[str]]:
        rooms = deepcopy(rooms)
        rooms = self.__draw_rooms_and_walls(rooms)
        rooms = self.__draw_startend(rooms, start_pos, end_pos)
        rooms = self.__draw_path(rooms, visited_rooms)
        rooms = self.__draw_player(rooms, player_pos)
        return rooms

    @staticmethod
    def __draw_rooms_and_walls(
        rooms: Rooms, 
        wall: str ='🞓', room: str ='⧠'
        ) -> list[list[str]]:

        for i in range(len(rooms)):
            for j in range(len(rooms[0])):
                if rooms[i][j]:
                    rooms[i][j] = room
                else:
                    rooms[i][j] = wall
        return rooms

    @staticmethod
    def __draw_startend(
        rooms: Rooms,
        start_pos: list[int, int], end_pos: list[int, int],
        start: str ='▥', end: str ='🞖'
        ) -> list[list[str]]:
        rooms[start_pos[0]][start_pos[1]] = start
        rooms[end_pos[0]][end_pos[1]] = end
        return rooms

    @staticmethod
    def __draw_path(
        rooms: Rooms, visited_rooms: list[list[int, int]], path: str ='X'
        ) -> list[list[str]]:
        for room in visited_rooms:
            if sum(room[:2]) != 0: # !!!!!
                rooms[room[0]][room[1]] = path
        return rooms

    @staticmethod
    def __draw_player(
        rooms: Rooms, player_pos: list[int, int], player: str ='⯐'
        ) -> list[list[str]]:
        rooms[player_pos[0]][player_pos[1]] = player
        return rooms


class Game(GameGenerator, Renderer, metaclass=SingletonMeta):
    def __init__(self,
        height: int =3,
        width: int =3,
        controls: int =0,
        gen_type=0
        ) -> None:
        super().__init__(height, width, gen_type)
        rooms = self.rooms
        self.visited_rooms = [] # movement changes this variable
        # if you go in wall == visited_rooms.append([0, 0, 0])

        self.controls = controls
        self.gen_type = gen_type

    def movement(self,
        direction: str,
        distance: int,
        get_named: bool =True
        ) -> list[list[int, int, int] | int] | list[dict[str:str]]:

        directions = {
            'Север': (-1, 0),
            'Восток': (0, 1),
            'Юг': (1, 0),
            'Запад': (0, -1)
        }
        list_of_visited_rooms = [] # [row, col, event code]
        for _ in range(distance):
            self.player_location[0] += directions[direction][0]
            self.player_location[1] += directions[direction][1]
            if self.rooms[self.player_location[0]][self.player_location[1]]:
                list_of_visited_rooms.append(
                    deepcopy(self.player_location)
                )
            else:
                self.player_location[0] -= directions[direction][0]
                self.player_location[1] -= directions[direction][1]
                list_of_visited_rooms.append(
                    [0, 0]
                )
                break
            if self.player_location == self.end_location:
                break

        self.visited_rooms.extend(list_of_visited_rooms)

        if get_named:
            return self.__get_named_list_of_visited_rooms_with_events(
                list_of_visited_rooms
                )
        else:
            return list_of_visited_rooms


    def __get_named_list_of_visited_rooms_with_events(self,
        list_of_visited_rooms: list[list[int, int, int]]
        ) -> list[dict[str:str]]:

        named_list_of_visited_rooms_with_events = []
        for room in list_of_visited_rooms:
            named_list_of_visited_rooms_with_events.append(
                {
                    'roomname': self.named_rooms[room[0]][room[1]],
                    'event': 0# !!!!!!!
                }
            )
        return named_list_of_visited_rooms_with_events


    def render_game(self) -> list[list[str]]:
        return super().render_game(
                        self.rooms,
                        self.start_location,
                        self.end_location,
                        self.player_location,
                        self.visited_rooms
                        )