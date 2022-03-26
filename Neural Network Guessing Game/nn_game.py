import curses
from numpy import exp, array, random, dot
from time import sleep

def calc_out(t_in, weights):
  return 1 / (1 + exp(-(dot(t_in, weights))))

def print_outputs(scr, y, c_out, t_out, p_out):
    lines = ' ' + ('|' + ' ' * 7) * 4 + '\n'
    mystring = ''
    for i in range(t_out.shape[0]):
        arr_string = "[{:.3f}]".format(t_out[i][0])
        mystring += arr_string + ' '
    mystring += '...TARGET\n'
    mystring += lines
    o_string = '...OUTPUT (CPU)\n'
    e_string = '...ERROR (CPU)\n' + lines
    for out in [c_out, p_out]:
        for i in range(out.shape[0]):
            arr_string = "[{:.3f}]".format(out[i][0])
            mystring += arr_string + ' '
        mystring += o_string
        for i in range(t_out.shape[0]):
            if t_out[i][0] - out[i][0] > 0:
                arr_string = "[{:.3f}]".format(t_out[i][0] - out[i][0])
            else:
                arr_string = "[{:.2f}]".format(t_out[i][0] - out[i][0])
            mystring += arr_string + ' '
        mystring += e_string
        o_string = '...OUTPUT (PLAYER)\n'
        e_string = '...ERROR (PLAYER)\n'
    x_off = 5
    cav_error = 0
    pav_error = 0
    for i in range(t_out.shape[0]):
        cav_error += t_out[i][0] - c_out[i][0]
        pav_error += t_out[i][0] - p_out[i][0]
    mystring += ' \\' + ' ' * x_off + '  |' + ' ' * x_off + '  |' + ' ' * x_off + '  /'
    mystring += '\n  \\' + '_' * x_off + '_|' + '_' * x_off + '__|' + '_' * x_off + '_/'
    mystring += '\n' + ' '*5 + '________|________\n'
    mystring += " " * 4 + "| " + " "* (2*len(arr_string) + 1) + " |\n"
    mystring += " " * 4 + "| CPU     PLAYER  |"

    if (cav_error / 4) > 0:
        mystring += '\n' + ' '*4 + '| ' + "{:.5f}".format(cav_error / 4) + ' '
    else:
        mystring += '\n' + ' '*4 + '| ' + "{:.4f}".format(cav_error / 4) + ' '
    if (pav_error / 4) > 0:
        mystring += "{:.5f}".format(pav_error / 4) + ' |'
    else:
        mystring += "{:.4f}".format(pav_error / 4) + ' |'
    if abs(cav_error) > abs(pav_error):
        mystring += '\n' + ' '*4 + '|  PLAYER LEADS!  |'
    else:
        mystring += '\n' + ' '*4 + '|   CPU LEADS!    |'
    mystring += '\n' + ' '*4 + '|_________________|\n'

    scr.addstr(y, 0, mystring)



def print_weights(scr, x, y, weights, pw):
    offset = y
    mystring = ''
    arr_string = "{:.4f}".format(weights[0][0])
    if weights[0][0] >= 0: arr_string = ' ' + arr_string
    mystring += " " * x + "| " + " "* (2*len(arr_string) + 1) + " |\n"
    mystring += " " * x + "| CPU     PLAYER  |\n"
    mystring += " " * x + "| " + " "* (2*len(arr_string) + 1) + " |\n"
    for i in range(weights.shape[0]):
        offset += 2
        arr_string = "{:.4f}".format(weights[i][0])
        pstring = "{:.4f}".format(pw[i][0])
        if (pw[i][0] >= 0):
            pstring = ' ' + pstring
        if weights[i][0] >= 0:
            arr_string = ' ' + arr_string
        mystring += " " * x + "| " + arr_string + ' ' + pstring
        if i < weights.shape[0]-1:
            mystring += ' |\n' + " " * x + "| " + " "* (2*len(arr_string) + 1) + " |\n"
        else:
            mystring += " |\n" + " " * x + "|_" + "_"* (2*len(arr_string) + 1) + "_|\n"
    scr.addstr(y, 0, mystring)
    return offset + 3


def quit(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()

def read_keys(scr, x_weights, y_weights, weights, player_weights):
    k = scr.getch()
    if k == ord('q'):
        quit(scr)

    if k == ord('w'):
        player_weights[0] += 0.001
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('s'):
        player_weights[0] -= 0.001
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('e'):
        player_weights[1] += 0.001
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('d'):
        player_weights[1] -= 0.001
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('r'):
        player_weights[2] += 0.001
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('f'):
        player_weights[2] -= 0.001
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)

    if k == ord('W'):
        player_weights[0] += 0.1
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('S'):
        player_weights[0] -= 0.1
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('E'):
        player_weights[1] += 0.1
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('D'):
        player_weights[1] -= 0.1
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('R'):
        player_weights[2] += 0.1
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
    if k == ord('F'):
        player_weights[2] -= 0.1
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)

    if k == ord(' '):
        return True, player_weights
    return False, player_weights

def go():
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    scr.nodelay(True)
    scr.keypad(True)
    random.seed(1)
    t_in = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    t_out = array([[0, 1, 1, 0]]).T
    weights = 2 * random.random((3, 1)) - 1
    player_weights = 2 * random.random((3, 1)) - 1
    offset = 1
    scr.addstr(offset, 0, "NEURAL NET WEIGHT GUESSING GAME")
    offset += 1
    scr.addstr(offset, 0, "SPACE TO PROGRESS, Q TO QUIT")
    offset += 1
    scr.addstr(offset, 0, "INCREASE PLAYER WEIGHTS: 0.001: w e r \t0.1: W E R")
    offset += 1
    scr.addstr(offset, 0, "DECREASE PLAYER WEIGHTS: 0.001: s d f \t-0.1: S D F")
    offset += 2
    old_offset = offset
    x_off = 5
    my_string = ''
    for i in range(t_in.shape[1]):
        for j in range(t_in.shape[0]):
            my_string += '['
            my_string += str(t_in[j][i])
            my_string += ']' + ' '*x_off
        my_string += '\n'
        offset += 1
    scr.addstr(old_offset, 0, my_string)
    my_string = ' \\' + ' ' * x_off + '  |' + ' ' * x_off + '  |' + ' ' * x_off + '  /'
    my_string += '\n  \\' + '_' * x_off + '_|' + '_' * x_off + '__|' + '_' * x_off + '_/'
    my_string += '\n' + ' '*5 + '________|________'
    old_offset = offset
    offset += 3
    scr.addstr(old_offset, 0, my_string)
    old_offset = offset
    x_weights = 4
    y_weights = old_offset
    old_offset = print_weights(scr, x_weights, y_weights, weights, player_weights)

    my_string = ' '*3 + '__________|__________'
    my_string += '\n  /' + ' ' * x_off + ' |' + ' ' * x_off + '  |' + ' ' * x_off + ' \\'
    my_string += '\n /' + ' ' * x_off + '  |' + ' ' * x_off + '  |' + ' ' * x_off + '  \\'
    scr.addstr(old_offset, 0, my_string)
    offset = old_offset
    offset += 3
    for iteration in range(100):
        out = calc_out(t_in, weights)
        pout = calc_out(t_in, player_weights)
        weights += dot(t_in.T, (t_out - out) * out * (1 - out))
        _ = print_weights(scr, x_weights, y_weights, weights, player_weights)
        _ = print_outputs(scr, offset, out, t_out, pout)
        go = False
        while go == False:
            go, player_weights = read_keys(scr, x_weights, y_weights, weights, player_weights)

if __name__ == '__main__':
  go()
