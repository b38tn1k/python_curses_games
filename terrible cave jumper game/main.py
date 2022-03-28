import curses, sched, time
from tools.map import Map

FPS = 30

class Controller():
    def __init__(self, height, width, map_height, map_width):
        self.map = Map(map_width, map_height)
        self.map.generate()
        self.x_map = round(map_width/2 - width)
        self.y_map = round(map_height/2 - height)
        self.width = width
        self.height = height
        self.facing = [-1, 0]
        self.offset_y = 1
        self.offset_x = 1
        self.avatar_y = int(self.height/2) + self.offset_y
        self.avatar_x = int(self.width/2) + self.offset_x
        self.screen = []
        self.current_slice = self.map.get_slice(self.y_map, self.x_map, self.height, self.width)
        while self.current_slice[self.avatar_y - 2][self.avatar_x - 2] > 0:
            self.map.generate()
            self.current_slice = self.map.get_slice(self.y_map, self.x_map, self.height, self.width)
        self.jump = False
        self.map.add_floor(height)
        self.fall = True
        self.jump_progress = 0
        self.jump_max = 8
        self.east = False
        self.west = False

    def draw(self, scr):
        borderstring = '▓' * (self.width + 2)
        # map
        offset = self.offset_y
        scr.addstr(offset, self.offset_x, borderstring)
        offset+=1
        for row in self.screen:
            scr.addstr(offset, self.offset_x, '▓' + row + '▓')
            offset+=1
        scr.addstr(offset, self.offset_x, borderstring)
        # avatar
        scr.addstr(self.avatar_y, self.avatar_x, '&', curses.color_pair(2))
        # scr.addstr(self.avatar_y, self.avatar_x, str(self.current_slice[self.avatar_y - 2][self.avatar_x-2]))
        # scr.addstr(int(self.height/2) + self.offset_y, int(self.width/2) + self.offset_x, '*')

    def update(self):
        self.screen = self.map.get_slice_string(self.y_map, self.x_map, self.height, self.width)
        self.current_slice = self.map.get_slice(self.y_map, self.x_map, self.height, self.width)
        if self.current_slice[self.avatar_y - 2][self.avatar_x-2] != 0:
            self.avatar_y -= 1
        self.avatar_y = int(self.height/2) + self.offset_y
        self.avatar_x = int(self.width/2) + self.offset_x
        if self.fall == True:
            self.go_south()
            if self.east == True:
                self.go_east()
            if self.west == True:
                self.go_west()
        if self.jump == True:
            self.jump_progress += 1
            self.go_north()
            if self.east == True:
                self.go_east()
            if self.west == True:
                self.go_west()
        if self.jump_progress >= self.jump_max:
            self.jump = False
            self.fall = True
            self.jump_progress = 0


    def go_north(self):
        tile = self.current_slice[self.avatar_y - 3][self.avatar_x-2]
        if tile == 0:
            self.y_map = max((self.y_map - 1), 0)
        else:
            self.jump_progress = 0
            self.jump = False
            self.fall = True
        self.facing = [-1, 0]

    def go_south(self):
        tile = self.current_slice[self.avatar_y - 1][self.avatar_x-2]
        tile2 = self.current_slice[self.avatar_y - 1][self.avatar_x-1]
        tile3 = self.current_slice[self.avatar_y - 1][self.avatar_x-3]
        if tile == 0 and tile2 == 0 and tile3 == 0:
            self.y_map = min((self.y_map + 1), (self.map.y - self.height))
        else:
            self.fall = False
            self.east = False
            self.west = False
        self.facing = [1, 0]

    def go_east(self):
        if self.west == True:
            self.west = False
        else:
            self.east = True
        tile = self.current_slice[self.avatar_y - 2][self.avatar_x-1]
        if tile == 0: self.x_map = min((self.x_map + 1), (self.map.x - self.width))
        tile = self.current_slice[self.avatar_y - 1][self.avatar_x-2]
        if tile == 0 and self.jump == False:
            self.fall = True
            self.y_map = min((self.y_map + 1), (self.map.y - self.height))
        else:
            self.fall = False
        self.facing = [0, 1]

    def go_west(self):
        if self.east == True:
            self.east = False
        else:
            self.west = True
        tile = self.current_slice[self.avatar_y - 2][self.avatar_x-3]
        if tile == 0: self.x_map = max((self.x_map - 1), 0)
        tile = self.current_slice[self.avatar_y - 1][self.avatar_x-2]
        if tile == 0 and self.jump == False:
            self.fall = True
            self.y_map = min((self.y_map + 1), (self.map.y - self.height))
        else:
            self.fall = False
        self.facing = [0, -1]

    def do_jump(self):
        self.jump = True


def read_keys(scr, controller):
    k = scr.getch()
    if k == ord('q'):
        quit(scr)
    elif k == ord('w'):
        pass
        # controller.go_north()
    elif k == ord('s'):
        pass
        # controller.go_south()
    elif k == ord('a'):
        controller.go_west()
    elif k == ord('d'):
        controller.go_east()
    elif k == ord(' '):
        controller.do_jump()

def update(scr, controller):
    controller.update()

def draw(scr, controller):
    controller.draw(scr)

def run(dt, scr, controller):
    scheduler = sched.scheduler(time.time, time.sleep)
    while True:
        nextEventTime = scheduler.run(blocking=True)
        scheduler.enter(dt, 1, update, (scr, controller))
        scheduler.enter(dt, 1, draw, (scr, controller))
        read_keys(scr, controller)

def loadScreen(scr, height, width):
    offset = 1
    text_pad = int((width - len("TERRRIBLE CAVE JUMPER GAME"))/2)
    borderstring = '▓' * (width + 2)
    scr.addstr(offset, 1, borderstring)
    offset += 1
    for i in range(height):
        scr.addstr(offset, 1, '▓' + ' '*width + '▓')
        offset += 1
    scr.addstr(5, text_pad+1, "TERRRIBLE CAVE JUMPER GAME")

    scr.addstr(offset, 1, borderstring)
    k = scr.getch()

def load():
    dt = 1.0 / FPS
    # screen stuff
    scr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    scr.nodelay(True)
    scr.keypad(True)
    loadScreen(scr, 20, 51)

    c = Controller(20, 51, 200, 400)
    run(dt, scr, c)


if __name__ == '__main__':
  load()
