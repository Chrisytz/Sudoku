''''''''''''''''''''''''''''''''''''
###   Sudoku (game and solver)   ###
###            Chris             ###
###       2021 Banff trip        ###
''''''''''''''''''''''''''''''''''''


# imports
import math
import pygame
import copy


class Box(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, row, col, constant):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((x_pos, y_pos, 49, 49))
        self.border = pygame.Rect((x_pos, y_pos, 50, 50))
        self.row = row
        self.col = col
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.border.center = (x_pos + 25, y_pos + 25)
        self.rect.center = (x_pos + 25, y_pos + 25)
        self.onclick = False
        self.constant = constant
        self.numEntered = False


class Guess(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, font, number, colour):
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.font = font
        self.number = number
        self.image = font.render(str(number), True, (50, 50, 50), self.colour)
        self.rect = pygame.Rect((x_pos, y_pos, 49, 49))
        self.rect.center = (x_pos + 25, y_pos + 25)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.onclick = False

    def update_image(self):
        self.image = self.font.render(str(self.number), True, (0, 0, 0), self.colour)


# creates the group of sprites
def create_grid(boxList, grid):
    for i in range(0, 9):
        for j in range(0, 9):
            constant = False
            if grid[j][i] != 0:
                constant = True
            boxList.add(Box(i * 50, j * 50, j, i, constant))


# draws initial grid to the screen
def print_initial_grid(boxList, grid, window, font, gridlineColour):
    for box in boxList:
        number = str(grid[box.row][box.col])

        # if number is not a constant set its colour to grey
        colour = (0, 0, 0)
        if not box.constant:
            colour = (100, 100, 100)

        if number == '0':
            number = ''

        image = font.render(number, True, colour, (255, 255, 255))

        # drawing to screen
        pygame.draw.rect(window, gridlineColour, box.border)
        pygame.draw.rect(window, (255, 255, 255), box.rect)
        window.blit(image, image.get_rect(center=box.rect.center))


# draws numbers to the screen in the solve_grid function to display agorithm in action
def print_number(boxList, row, col, window, number, font):
    for box in boxList:
        if box.row == row and box.col == col:
            image = font.render(str(number), True, (0, 0, 0), (255,255,255))
            pygame.draw.rect(window, (255, 255, 255), box.rect)
            window.blit(image, image.get_rect(center=box.rect.center))


# draws the border of a box
def draw_border(window, colour, box, selectedColour):
    pygame.draw.rect(window, (colour), box.border)
    pygame.draw.line(window, colour, (box.x_pos + 50, box.y_pos), (box.x_pos + 50, box.y_pos + 50), 1)
    pygame.draw.line(window, colour, (box.x_pos, box.y_pos + 50), (box.x_pos + 50, box.y_pos + 50), 1)
    pygame.draw.rect(window, selectedColour, box.rect)


# draws the user entered number onto the screen
def update_grid(number, font, window, box, colour, check, selectedColour, gridlineColour):
    # if computer is not checking values, set all borders to black
    if not check:
        colour = gridlineColour

    grid[box.row][box.col] = number
    image = font.render(str(number), True, (100, 100, 100), selectedColour)
    draw_border(window, colour, box, selectedColour)
    window.blit(image, image.get_rect(center=box.rect.center))
    if not check:
        draw_grid_lines(window)


# draws the user's guess onto the screen (corner of each box)
def print_guess(guessList, window, selectedColour):
    for guess in guessList:
        colour = (255, 255, 255)
        if guess.onclick == True:
            colour = selectedColour

        pygame.draw.rect(window, colour, guess.rect)
        window.blit(guess.image, guess.image.get_rect(topleft=(guess.x_pos + 5, guess.y_pos + 2)))


# deletes all incorrect numbers after x is clicked to toggle checking on (check = True)
def delete_incorrect(solvedGrid, grid, boxList, window, font, gridlineColour):
    for i in range(0, 9):
        for j in range(0, 9):
            if solvedGrid[i][j] != grid[i][j]:
                grid[i][j] = 0
    print_initial_grid(boxList, grid, window, font, gridlineColour)
    pygame.display.flip()


# moving the space selected up/down/right/left
def move_space(boxList, grid, window, font, guessList, y_adj, x_adj, selectedColour, gridlineColour):
    for box in boxList:
        if box.onclick == True:
            for box1 in boxList:

                # checking to see if box is within grid
                if 0 <= box1.x_pos <= 400 and 0 <= box1.y_pos <= 400:

                    # checking to see which box user input is pointing to
                    if box1.x_pos == (box.x_pos + x_adj) and box1.y_pos == (box.y_pos + y_adj):
                        box.onclick = False
                        box1.onclick = True
                        print_initial_grid(boxList, grid, window, font, gridlineColour)
                        draw_grid_lines(window)
                        print_guess(guessList, window, selectedColour)
                        pygame.draw.rect(window, (235, 235, 235), box1.rect)
            break


# draws the back grid lines
def draw_grid_lines(window):
    pygame.draw.line(window, (0, 0, 0), (0, 0), (0, 450), 1)
    pygame.draw.line(window, (0, 0, 0), (150, 0), (150, 450), 1)
    pygame.draw.line(window, (0, 0, 0), (300, 0), (300, 450), 1)
    pygame.draw.line(window, (0, 0, 0), (450, 0), (450, 450), 1)
    pygame.draw.line(window, (0, 0, 0), (0, 0), (450, 0), 1)
    pygame.draw.line(window, (0, 0, 0), (0, 150), (450, 150), 1)
    pygame.draw.line(window, (0, 0, 0), (0, 300), (450, 300), 1)
    pygame.draw.line(window, (0, 0, 0), (0, 450), (450, 450), 1)


# printing the sodoku values in the console
def print_grid(arr):
    for i in range(0, 9):
        print(arr[i])


# checks to see if theres already a value there (aka non 0 value)
def value_exists(arr, current):
    for i in range(0, 9):
        for j in range(0, 9):
            if arr[i][j] == 0:
                current[0] = i
                current[1] = j
                return True
    return False


# checks to see if value repeats in its row
def value_repeat_row(arr, row, num):
    for i in range(0, 9):
        if arr[row][i] == num:
            return True
    return False


# checks to see if value repeats in its column
def value_repeat_col(arr, col, num):
    for i in range(0, 9):
        if arr[i][col] == num:
            return True
    return False


# checks to see if value repeats in its 3x3 square
def value_repeat_square(arr, row, col, num):
    square_row = math.floor(row / 3) * 3
    square_col = math.floor(col / 3) * 3

    for i in range(square_row, square_row + 3):
        for j in range(square_col, square_col + 3):
            if arr[i][j] == num:
                return True
    return False


# if value doesnt exist in its row, column and square then it is safe
def value_safe(arr, row, col, num):
    if not value_repeat_row(arr, row, num) and not value_repeat_col(arr, col, num) and not value_repeat_square(arr, row, col, num):
        return True
    return False


# recursive backtraking algorithm to solve sodoku grid
def solve_grid(arr, boxList, window, font, display):
    current = [0, 0]

    # set current to a 0-value box
    if not value_exists(arr, current):
        return True

    row = current[0]
    col = current[1]

    # checking values from 1-9 to see if they are safe
    for num in range(1, 10):
        if value_safe(arr, row, col, num):
            arr[row][col] = num

            # if display == True draw it in the screen
            if display:
                print_number(boxList, row, col, window, num, font)
                draw_grid_lines(window)
                pygame.display.flip()
                pygame.time.delay(1)

            # recursive part of the function --> if the value is safe continue to the next 0-value
            if solve_grid(arr, boxList, window, font, display) == True:
                return True

            # if value does not work out, set it to back to 0 (empty) and algorithm try new values
            arr[row][col] = 0

    # backtrack
    return False


# running the game (drawing game onto screen)
def game(grid, unsolvedGrid, solvedGrid):
    # init
    pygame.init()
    window = pygame.display.set_mode((450, 450))
    pygame.display.set_caption("Sudoku")
    done = False

    print (pygame.font.get_fonts())

    #possible fonts --> corbel
    font = pygame.font.SysFont('corbel', 30)
    fontSmall = pygame.font.SysFont('corbel', 15)
    solved = False
    check = True
    boxList = pygame.sprite.Group()
    guessList = pygame.sprite.Group()
    selectedColour = (235, 235, 235)
    gridlineColour = (150, 150, 150)

    create_grid(boxList, grid)
    solve_grid(solvedGrid, boxList, window, font, False)

    print_initial_grid(boxList, grid, window, font, gridlineColour)
    draw_grid_lines(window)

    pygame.display.flip()

    # loop for the game
    while not done:
        for event in pygame.event.get():

            # if exit button clicked, stop the code
            if event.type == pygame.QUIT:
                done = True

            # if user or computer has not solved the grid, allow user input
            if not solved:

                # pressing the x key toggles the value checker
                if event.type == pygame.KEYDOWN:
                    if event.unicode == 'x':
                        if check:
                            check = False
                        else:
                            delete_incorrect(solvedGrid, grid, boxList, window, font, selectedColour)
                            check = True

                # on right click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for box in boxList:
                        box.onclick = False
                    pos = pygame.mouse.get_pos()
                    print_initial_grid(boxList, grid, window, font, gridlineColour)
                    print_guess(guessList, window, selectedColour)
                    draw_grid_lines(window)

                    # if box clicked is not one with an initial value, select that box and draw a grey square
                    for box in boxList:
                        if box.constant == False:
                            if box.rect.collidepoint(pos):
                                box.onclick = True
                                pygame.draw.rect(window, selectedColour, box.rect)

                # arrow keys to control which box is being selected
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    move_space(boxList, grid, window, font, guessList, 0, 50, selectedColour, gridlineColour)
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    move_space(boxList, grid, window, font, guessList, 0, -50, selectedColour, gridlineColour)
                elif pygame.key.get_pressed()[pygame.K_UP]:
                    move_space(boxList, grid, window, font, guessList, -50, 0, selectedColour, gridlineColour)
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    move_space(boxList, grid, window, font, guessList, 50, 0, selectedColour, gridlineColour)

                # user input
                for box in boxList:
                    if box.onclick == True and box.constant == False:
                        if event.type == pygame.KEYDOWN:
                            number = ''
                            for i in range(1, 10):

                                # checking if a number between 1-9 is clicked
                                if event.unicode == str(i):
                                    number = i

                                    # if space + number is clicked it recognize it as a 'guess'
                                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                                        guess = Guess(box.x_pos, box.y_pos, fontSmall, number, selectedColour)
                                        guessList.add(guess)
                                        guess.onclick = True

                                        # drawing to screen
                                        draw_border(window, gridlineColour, box, selectedColour)
                                        print_guess(guessList, window, selectedColour)
                                        draw_grid_lines(window)

                                        # resetting onclick to False and updating text background colour to white when box is no longer selected
                                        guess.onclick = False
                                        guess.colour = (255, 255, 255)
                                        guess.update_image()

                                    # when space is not pressed...
                                    else:

                                        # if a number is entered in a box with a guess in it, remove the guess from the group of sprites (no longer printed)
                                        for guess in guessList:
                                            if guess.x_pos == box.x_pos and guess.y_pos == box.y_pos:
                                                guessList.remove(guess)

                                        box.numEntered = True

                                        # border colour is red if wrong and green if right
                                        colour = (168, 0, 17)
                                        if solvedGrid[box.row][box.col] == number:
                                            colour = (0, 168, 84)

                                        draw_grid_lines(window)
                                        update_grid(number, font, window, box, colour, check, selectedColour, gridlineColour)

                                    # update display and wait 50 milliseconds
                                    pygame.display.flip()
                                    pygame.time.delay(50)

                            # if the computer is checking if values are correct...
                            if check:

                                # if number entered is not correct, empty the box
                                if solvedGrid[box.row][box.col] != number and box.numEntered == True:
                                    number = ''
                                    draw_grid_lines(window)
                                    update_grid(number, font, window, box, colour, check, selectedColour, gridlineColour)

                            box.numEntered = False

                # if enter is clicked or user has solved grid, run backtracking algorithm and set solved to true
                if pygame.key.get_pressed()[pygame.K_RETURN] or solvedGrid == grid:
                    print_initial_grid(boxList, grid, window, font, gridlineColour)
                    solve_grid(unsolvedGrid, boxList, window, font, True)
                    solved = True

        # update display
        pygame.display.flip()

    # quit
    pygame.display.quit()


# running file
if __name__ == '__main__':

    # a few grids... I was too lazy to add more oops

    '''
    # easy grid #
    grid = [[4, 2, 0, 0, 0, 8, 9, 0, 0],
            [9, 0, 0, 0, 4, 2, 0, 0, 7],
            [0, 8, 3, 1, 0, 7, 0, 0, 0],
            [0, 3, 2, 6, 0, 5, 4, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 2, 1, 0, 5, 0, 8],
            [0, 7, 1, 0, 0, 6, 0, 4, 0],
            [2, 5, 6, 4, 0, 0, 8, 0, 1],
            [3, 4, 0, 8, 5, 0, 0, 0, 6]]
    '''

    # medium grid #
    grid = [[0, 7, 0, 1, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 5, 7, 4, 0, 6],
            [2, 0, 0, 4, 0, 3, 0, 7, 0],
            [0, 0, 0, 6, 0, 1, 0, 4, 9],
            [3, 6, 0, 9, 4, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 6, 2, 0],
            [7, 0, 8, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 7, 2, 8, 9, 3, 4]]

    '''
    # hard grid #
    grid = [[9, 2, 0, 0, 0, 0, 3, 0, 0],
            [0, 5, 0, 0, 4, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 1, 0],
            [3, 0, 0, 0, 0, 5, 6, 8, 0],
            [0, 0, 0, 0, 8, 3, 0, 0, 4],
            [6, 8, 0, 1, 3, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [0, 1, 9, 0, 0, 0, 5, 0, 0]]
    '''

    '''
    # expert grid #
    grid = [[0, 0, 0, 0, 3, 0, 8, 1, 0],
            [0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 0, 0, 0, 0, 4],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 9, 0, 0, 0, 0],
            [0, 9, 0, 0, 4, 0, 0, 2, 6],
            [4, 2, 0, 0, 0, 6, 0, 0, 0],
            [9, 0, 0, 3, 0, 0, 0, 7, 0],
            [0, 0, 3, 1, 0, 9, 2, 0, 0]]
    '''

    unsolvedGrid = copy.deepcopy(grid)

    solvedGrid = copy.deepcopy(grid)

    game(grid, unsolvedGrid, solvedGrid)