import curses, sched, time
from random import randint, seed, choice

seed()
FPS = 20
DEBUG = False

def blank_field(dims):
    field = []
    # initialise
    for i in range(dims[1]):
        field.append([' '] * dims[0])
    field[0] = field[-1] = ['-'] * dims[0]
    for row in field: row[0] = row[-1] = "|"
    return field

def make_field(dims):
    field = []
    # initialise
    for i in range(dims[1]):
        field.append([' '] * dims[0])
    # add landscape
    dots = [' '] * 60
    dots.append('.')
    dots.append('.')
    dots.append('$')
    for i in range(dims[1]):
        for j in range(dims[0]):
            field[i][j] = choice(dots)

    # generate lines
    lines = []
    for i in range(10):
        if choice([True, False]) == True: #vertical
            x = randint(0, dims[1]-1)
            y_start = randint(0, dims[0]-4)
            y_end = randint(y_start, dims[0]-1)
            for y in range(y_start, y_end):
                field[x][y] = '-'
        else:
            y = randint(0, dims[0]-4)
            x_start = randint(0, dims[1]-4)
            x_end = randint(x_start, dims[1]-1)
            for x in range(x_start, x_end):
                field[x][y] = '|'

    # clear out start and end areas:
    for x in range(0, 5):
        for y in range(dims[1]-3, dims[1]):
            field[y][x] = ' '

    for x in range(dims[0]-5, dims[0]):
        for y in range(0, 3):
            field[y][x] = ' '

    # add portal
    field[1][dims[0]-2] = '@'

    # add border
    field[0] = field[-1] = ['-'] * dims[0]
    for row in field: row[0] = row[-1] = "|"
    return field

class Field():
    def __init__(self, scr, y, x):
        self.scr = scr
        self.field_dims = [y, x]
        self.monsters = []
        self.field = []
        self.new_field()

    def new_field(self):
        self.monsters = []
        for i in range(0, randint(2, 8)):
            self.monsters.append(Monster(self.scr, self.field_dims[1], self.field_dims[0]))
        self.field = make_field(self.field_dims)

    def remove_monster(self, monster):
        for i, m in enumerate(self.monsters):
            if m.id == monster.id:
                self.monsters.pop(i)

    def make_blank(self):
        self.field = blank_field(self.field_dims)

    def draw(self):
        for y in range(self.field_dims[1]):
            for x in range(self.field_dims[0]):
                pos_char = str(self.field[y][x][0])
                if pos_char in '@':
                    self.scr.addstr(y, x, pos_char, curses.color_pair(2))
                elif pos_char in '$':
                    self.scr.addstr(y, x, pos_char, curses.color_pair(3))
                elif pos_char in '.-|':
                    self.scr.addstr(y, x, pos_char, curses.color_pair(4))
                else:
                    self.scr.addstr(y, x, pos_char)

    def clear_yx(self, y, x):
        if not(y == 0 or y == self.field_dims[1]-1 or x == 0 or x == self.field_dims[0]):
            self.field[y][x] = ' '

class PlayerCharacter():
    def __init__(self, scr, ylim, xlim):
        self.start = True
        self.need_map_rst = True
        self.scr = scr
        self.xlim = xlim - 2
        self.ylim = ylim - 2
        self.icon = '&'
        self.position = [self.ylim, 2]
        self.map = []
        self.ammo = 3
        self.facing = [-1, 0]
        self.just_shot = False
        self.bullets = []
        self.resets = 0
        self.deaths = 0
        self.kill_count = 0

    def need_map_reset(self):
        if self.need_map_rst == True:
            self.need_map_rst = False
            return True
        else:
            return False

    def reset(self):
        self.position = [self.ylim, 2]
        self.facing = [-1, 0]
        self.resets += 1

    def die(self):
        self.deaths += 1
        self.reset()

    def draw(self):
        self.scr.addstr(self.position[0], self.position[1], self.icon, curses.color_pair(1))
        offset = 2
        self.scr.addstr(self.ylim + offset, 0, 'AMMO: ' + str(self.ammo), curses.color_pair(4))
        offset += 1
        self.scr.addstr(self.ylim+offset, 0, 'WORLDS EXPLORED: ' + str(self.resets - self.deaths), curses.color_pair(4))
        offset += 1
        self.scr.addstr(self.ylim+offset, 0, 'DEATH COUNT: ' + str(self.deaths), curses.color_pair(4))
        offset += 1
        self.scr.addstr(self.ylim+offset, 0, 'KILL COUNT: ' + str(self.kill_count), curses.color_pair(4))
        offset += 1
        if DEBUG is True:
            if self.position[0] < 10:
                ystring = '0' + str(self.position[0])
            else:
                ystring = str(self.position[0])
            if self.position[1] < 10:
                xstring = '0' + str(self.position[1])
            else:
                xstring = str(self.position[1])
            position_string = "X: " + xstring + " Y: " + ystring
            self.scr.addstr(self.ylim+offset, 0, position_string)
            offset += 1

    def go_north(self):
        self.facing = [-1, 0]
        if self.map[self.position[0] - 1][self.position[1]] in ' $@':
            self.position[0] -= 1

    def go_south(self):
        self.facing = [1, 0]
        if self.map[self.position[0] + 1][self.position[1]] in ' $@':
            self.position[0] += 1

    def go_east(self):
        self.facing = [0, 1]
        if self.map[self.position[0]][self.position[1] + 1] in ' $@':
            self.position[1] += 1

    def go_west(self):
        self.facing = [0, -1]
        if self.map[self.position[0]][self.position[1] - 1] in ' $@':
            self.position[1] -= 1

    def update_map(self, map):
        self.map = map

    def check_pickup(self):
        on_ammo = False
        if self.map[self.position[0]][self.position[1]] == '$':
            on_ammo = True
        return [on_ammo, self.position[0], self.position[1]]

    def check_shoot(self):
        shoot = self.just_shot
        self.just_shot = False
        return shoot

    def add_ammo(self):
        self.ammo += 1
        if self.ammo > 9: self.ammo = 9

    def shoot(self):
        if self.ammo >=1:
            self.ammo -= 1
            self.just_shot = True

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def remove_bullet(self, bullet):
        for i, b in enumerate(self.bullets):
            if b.id == bullet.id:
                self.bullets.pop(i)

    def on_portal(self):
        if self.map[self.position[0]][self.position[1]] == '@':
            return True
        else:
            return False

    def plus_kill(self):
        self.kill_count += 1


class Bullet():
    def __init__(self, scr, x, y, direction):
        self.scr = scr
        self.x = x
        self.y = y
        self.direction = direction
        self.icon = '*'
        self.id = randint(0, 100)

    def update(self):
        self.x += self.direction[1]
        self.y += self.direction[0]
        return self.x, self.y

    def draw(self):
        self.scr.addstr(self.y, self.x, '*')

class Monster():
    def __init__(self, scr, ylim, xlim):
        self.scr = scr
        self.xlim = xlim
        self.ylim = ylim
        self.x = randint(5, xlim-5)
        self.y = randint(5, ylim-5)
        self.icon = '#'
        self.id = randint(0, 100)

    def draw(self):
        self.scr.addstr(self.y, self.x, self.icon, curses.color_pair(5))

    def update(self):
        chance = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        if  chance == 1:
            self.x += choice([-1, 0, 0, 1])
        elif chance == 2:
            self.y += choice([-1, 0, 0, 1])
        else:
            pass
        if self.x <=1 or self.x >=self.xlim-3:
            self.x = randint(5, self.xlim-5)
        if self.y <=1 or self.y >=self.ylim-3:
            self.y = randint(5, self.ylim-5)

    def check_collide(self, x, y):
        if self.x == x and self.y == y:
            return True
        else:
            return False


def quit(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()

def read_keys(scr, pc):
    k = scr.getch()
    if k == ord('q'):
        quit(scr)
    elif k == ord('w'):
        pc.go_north()
    elif k == ord('s'):
        pc.go_south()
    elif k == ord('a'):
        pc.go_west()
    elif k == ord('d'):
        pc.go_east()
    elif k == ord(' '):
        pc.start = False
        pc.shoot()
    elif k == ord('r'):
        pc.ammo = 3


def update(field, pc):
    #game modes
    if pc.deaths == 3:
        field.scr.clear()
        field.make_blank()
        field.draw()
        offset = 5
        print_in_center(field.scr, field.field_dims[0], offset, "GAME OVER", curses.color_pair(4))
        offset += 2
        my_str = "WORLDS COMPLETED: " + str(pc.resets - pc.deaths)
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(4))
        offset += 2
        my_str = "KILL COUNT: " + str(pc.kill_count)
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(4))
        offset += 2
        my_str = "PRESS Q TO QUIT"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(4))
        offset += 2
    elif pc.start == True:
        field.scr.clear()
        field.make_blank()
        field.draw()
        offset = 2
        print_in_center(field.scr, field.field_dims[0], offset, "WELCOME TO THE PORTAL GAME", curses.color_pair(4))
        offset += 3
        print_in_center(field.scr, field.field_dims[0], offset, 'W', curses.color_pair(4))
        offset += 1
        print_in_center(field.scr, field.field_dims[0], offset, 'A S D', curses.color_pair(4))
        offset += 1
        my_str = "SPACE BAR TO SHOOT"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(4))
        offset += 2

        my_str = "YOU ARE &"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(1))
        offset += 1
        my_str = "PICK UP AMMO $"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(3))
        offset += 1
        my_str = "BLAST THROUGH WALLS - |"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(4))
        offset += 1
        my_str = "KILL THE MONSTERS #"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(5))
        offset += 1
        my_str = "GET TO THE PORTAL @"
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(2))
        offset += 4

        my_str = "PRESS SHOOT TO CONTINUE..."
        print_in_center(field.scr, field.field_dims[0], offset, my_str, curses.color_pair(4))
        offset += 2
    else:
        # game entry
        if pc.need_map_reset() == True:
            field.new_field()
            pc.update_map(field.field)
        # monsters
        for monster in field.monsters:
            monster.update()
            if monster.check_collide(pc.position[1], pc.position[0]) == True:
                pc.die()
        # pickups
        pick_up = pc.check_pickup()
        if pick_up[0] is True:
            pc.add_ammo()
            field.clear_yx(pick_up[1], pick_up[2])
            pc.update_map(field.field)

        # shooting
        shoot = pc.check_shoot()
        if shoot is True:
            pc.add_bullet(Bullet(field.scr, pc.position[1], pc.position[0], pc.facing))
        for bullet in pc.bullets:
            x, y = bullet.update()
            if x == 0 or x == pc.xlim or y == 0 or y == pc.ylim+1:
                pc.remove_bullet(bullet)
            if not (field.field[y][x] in ' $'):
                pc.remove_bullet(bullet)
                field.clear_yx(y, x)
                pc.update_map(field.field)
            for monster in field.monsters:
                if monster.check_collide(x, y) == True:
                    pc.plus_kill()
                    field.remove_monster(monster)

        #portalling
        if pc.on_portal() == True:
            field.new_field()
            pc.update_map(field.field)
            pc.reset()
        #drawing
        for asset in [field, pc]:
            asset.draw()
        for bullet in pc.bullets:
            bullet.draw()
        for monster in field.monsters:
            monster.draw()


def print_in_center(scr, x, offset, my_str, colorpair):
    str_x = int((x - len(my_str))/2)
    scr.addstr(offset, str_x, my_str, colorpair)

def run(dt, field, pc, scheduler):
    while True:
        nextEventTime = scheduler.run(blocking=True);
        scheduler.enter(dt, 1, update, (field, pc))
        read_keys(field.scr, pc)

def load():
  print("hi")
  # time stuff
  dt = 1.0 / FPS
  scheduler = sched.scheduler(time.time, time.sleep)
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
  # game stuff
  field = Field(scr, 40, 20)
  field.new_field()
  pc = PlayerCharacter(scr, 20, 40)
  pc.update_map(field.field)
  run(dt, field, pc, scheduler)


if __name__ == '__main__':
  load()
