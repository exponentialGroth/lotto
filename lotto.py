import pygame
import random
from pathlib import Path

WIDTH, HEIGHT = 720, 720
RANDOM_WHEEL_WIDTH, RANDOM_WHEEL_HEIGHT = 360, 360
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DARK_OLIVE_GREEN = (87, 109, 34)
GREEN = (80, 149, 56)
BROWN = (163, 85, 13)
YELLOW = (250, 207, 4)
RECT_ACTIVE = pygame.Color('lightskyblue3')
RECT_PASSIVE = pygame.Color('gray15')

random.seed()
pygame.init()
pygame.font.init()
pygame.mixer.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Lotto")


changingColorR = 0
changingColorG = 0
changingColorB = 0
money = 20
current_number = 14
wheelTurns = 0
status_rotate_wheel = False
status_add_money = True  # False if the money has been added


# Load images
cwd = Path.cwd()
if cwd.name == "lotto":
    image_path = cwd / "images"
elif cwd.name == "oldPyGames":
    image_path = cwd / "lotto" / "images"
else:
    print("Select a correct working directory (.../lotto or .../oldPyGames).")
    exit()

RANDOM_WHEEL_IMAGE = pygame.image.load(image_path / "random_wheel.png")
RANDOM_WHEEL = pygame.transform.scale(RANDOM_WHEEL_IMAGE, (360,360))
RANDOM_WHEEL_RECT = RANDOM_WHEEL.get_rect(center = (360,360))

WHEEL_OF_FORTUNE_SURROUNDING_IMAGE = pygame.image.load(image_path / "wheel_of_fortune_surrounding.png")
WHEEL_OF_FORTUNE_SURROUNDING = pygame.transform.scale(WHEEL_OF_FORTUNE_SURROUNDING_IMAGE, (423,491))
WHEEL_OF_FORTUNE_SURROUNDING_RECT = WHEEL_OF_FORTUNE_SURROUNDING.get_rect(center = (366,401))

WHEEL_POINTER_IMAGE = pygame.image.load(image_path / "pointer.png")

MONEY_IMAGE = pygame.image.load(image_path / "money.png")
MONEY_SYMBOL = pygame.transform.scale(MONEY_IMAGE, (65,50))

BACKGROUND_IMAGE = pygame.image.load(image_path / "sunburst_background.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (720, 720))


INPUT_FONT = pygame.font.Font(None, 32)

class InputField:
    w = 80
    h = 30
    l = 50
    y0 = 200
    padding = 5
    step = 50
    value = None

    def __init__(self, i) -> None:
        self.index = i
        self.rect = pygame.Rect(self.l, self.y0 + self.step * i, self.w, self.h)

    def draw(self):
        isCorrect = wheelTurns > 0 and correct_numbers[:wheelTurns].count(self.value) == 1
        surface = INPUT_FONT.render(f'Zahl {self.index+1}: {self.value if self.value is not None else ""}', True, GREEN if isCorrect else BLACK)
        self.rect.w = surface.get_width() + 2 * self.padding
        WIN.blit(surface, (self.rect.x + self.padding, self.rect.y + self.padding))
        pygame.draw.rect(WIN, RECT_ACTIVE if self.index == activeInput else RECT_PASSIVE, self.rect, width=2)

    def add(self, character):
        code = ord(character)
        if not 48 <= code <= 57: return  # not a digit
        if self.value is None:
            if code == 48: return
            self.value = code - 48
        elif self.value <= 4:
            self.value = 10 * self.value + code - 48

    def delete(self):
        if self.value is None: return
        if self.value <= 9:
            self.value = None
        else:
            self.value = int((self.value - (self.value % 10)) / 10)

    def contains(self, coord):
        return self.rect.collidepoint(coord)
    

inputs = [InputField(i) for i in range(6)]
activeInput = 0


def choose_correct_numbers(): 
    correct_number_1 = random.randint(1, 49)
    correct_number_2 = random.randint(1,49)
    while correct_number_1 == correct_number_2:
        correct_number_2 = random.randint(1,49)
    correct_number_3 = random.randint(1,49)
    while correct_number_3 == correct_number_1 or correct_number_3 == correct_number_2:
        correct_number_3 = random.randint(1,49)
    correct_number_4 = random.randint(1,49)
    while correct_number_4 == correct_number_1 or correct_number_4 == correct_number_2 or correct_number_4 == correct_number_3:
        correct_number_4 = random.randint(1,49)
    correct_number_5 = random.randint(1,49)
    while correct_number_5 == correct_number_1 or correct_number_5 == correct_number_2 or correct_number_5 == correct_number_3 or correct_number_5 == correct_number_4:
        correct_number_5 = random.randint(1,49)
    correct_number_6 = random.randint(1,49)
    while correct_number_6 == correct_number_1 or correct_number_6 == correct_number_2 or correct_number_6 == correct_number_3 or correct_number_6 == correct_number_4 or correct_number_6 == correct_number_5:
        correct_number_6 = random.randint(1,49)

    global correct_numbers
    correct_numbers = [correct_number_1, correct_number_2, correct_number_3, correct_number_4, correct_number_5, correct_number_6]


# Text fields
CORRECT_NUMBER_FONT = pygame.font.Font(None, 50)
CORRECT_NUMBER_HEADING = pygame.font.Font(None, 32).render("Gewinnerzahlen:", True, BLACK)
correctNumSurfaces = []

choose_correct_numbers()

MONEY_FONT = pygame.font.SysFont('comicsans', 55)

button_rotate_wheel_font = pygame.font.Font(None, 50)
button_rotate_wheel_text = "RAD DREHEN"
button_rotate_wheel_polygon = pygame.draw.polygon(WIN, BROWN, ((245, 585), (495, 585), (235, 630), (485, 630)))


def setup():
    global current_number
    global wheelTurns
    global status_rotate_wheel
    global status_add_money
    global activeInput
    global changingColorR, changingColorG, changingColorB
    global correctNumSurfaces

    current_number = 14
    wheelTurns = 0
    status_rotate_wheel = False
    activeInput = 0
    status_add_money = True

    changingColorR = 0
    changingColorG = 0
    changingColorB = 0

    choose_correct_numbers()
    correctNumSurfaces.clear()


def count_correct_guesses():
    correct_guesses = 0
    for guess in (it.value for it in inputs):
        for correctNum in correct_numbers:
            if guess == correctNum:
                correct_guesses += 1
                break

    return correct_guesses


def draw_start_button():
    button_rotate_wheel_font = pygame.font.Font(None, 50)
    button_rotate_wheel_text = "RAD DREHEN"
    button_rotate_wheel_polygon = pygame.draw.polygon(WIN, BROWN, ((245, 585), (495, 585), (235, 630), (485, 630)))
    pygame.draw.polygon(WIN, BROWN, ((245, 585), (480, 585), (485, 630), (235, 630)))
    button_rotate_wheel_surface = button_rotate_wheel_font.render(button_rotate_wheel_text, True, YELLOW)
    WIN.blit(button_rotate_wheel_surface, (button_rotate_wheel_polygon.x + 8, button_rotate_wheel_polygon.y + 12))


def rotate(surface, angle):
    rotated_wheel = pygame.transform.rotozoom(surface, angle, 1)
    rotated_wheel_rect = rotated_wheel.get_rect(center = (360,360))
    return rotated_wheel, rotated_wheel_rect


def rotate_wheel(number_before_rotation, number_after_rotation):
    time = 1 / FPS
    number_of_rotations = 7
    total_time = 7.3469 * (number_after_rotation - number_before_rotation + 49 * number_of_rotations) / (0.5 * 7.3469 * FPS)
    a = (7.3469 * (number_after_rotation - number_before_rotation + 49 * number_of_rotations) - 7.3469 * FPS * total_time) * 2 / (total_time ** 2)
    angle = 7.3469 * (number_before_rotation - 14 + 49 ) + 7.3469
    while time < total_time:
        RANDOM_WHEEL_ROTATED, RANDOM_WHEEL_ROTATED_RECT = rotate(RANDOM_WHEEL, angle)
        WIN.blit(RANDOM_WHEEL_ROTATED, RANDOM_WHEEL_ROTATED_RECT)
        WIN.blit(WHEEL_POINTER_IMAGE, (525, 322))
        pygame.display.update(180, 180, 360, 360)
        time += 1 / FPS
        angle += (7.3469 + (a*time) / FPS)


def draw_final_wheel(number_of_the_wheel):
    FINAL_RANDOM_WHEEL, FINAL_RANDOM_WHEEL_RECT =  rotate(RANDOM_WHEEL, 360/49 * (number_of_the_wheel + 49 - 14.5))
    WIN.blit(FINAL_RANDOM_WHEEL, FINAL_RANDOM_WHEEL_RECT)
    WIN.blit(WHEEL_POINTER_IMAGE, (525, 322) )


def create_correct_num_surfaces():
    global correctNumSurfaces
    for i in range(6):
        color = RED
        for guess in (it.value for it in inputs):
            if guess == correct_numbers[i]:
                color = GREEN
                break
        correctNumSurfaces.append(CORRECT_NUMBER_FONT.render(str(correct_numbers[i]), True, color))
        

def draw_correct_numbers():
    WIN.blit(CORRECT_NUMBER_HEADING, (520, 150))
    for i, s in enumerate(correctNumSurfaces[:wheelTurns]):
        WIN.blit(s, (606, 150 + 50 * (i+1)))


def draw_end_message():
    end_of_round_font = pygame.font.Font(None, 75)
    parts_of_end_of_round_text = ["Du hast " + str(count_correct_guesses()) , "Zahlen richtig geraten.", "SPACE zum erneut spielen"]    
    lines = [end_of_round_font.render(part, 1, (changingColorR, changingColorG, changingColorB)) for part in parts_of_end_of_round_text]
    coords = [(360 - line.get_width()/2, 360 + (i-1) * 60 - line.get_height()/2) for i, line in enumerate(lines)]
    for line, pos in zip(lines, coords):
        WIN.blit(line, pos)


def draw_window():
    global status_rotate_wheel
    global wheelTurns
    global current_number
    global money
    global status_add_money
    global changingColorR
    global changingColorG
    global changingColorB

    WIN.fill((BLACK))
    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(WHEEL_OF_FORTUNE_SURROUNDING, WHEEL_OF_FORTUNE_SURROUNDING_RECT)
    WIN.blit(RANDOM_WHEEL, RANDOM_WHEEL_RECT)
    WIN.blit(WHEEL_POINTER_IMAGE, (525, 322) )

    if status_rotate_wheel and wheelTurns < 6:
        if wheelTurns == 0:
            money -= 5
    money_text = MONEY_FONT.render(" = "+ str(money), 1, GREEN)
    WIN.blit(MONEY_SYMBOL, (278, 45))
    WIN.blit(money_text, (MONEY_SYMBOL.get_width() + 278, 55 ))
    pygame.display.update(250, 5, 200, 100)

    for field in inputs: field.draw()

    if all([it.value for it in inputs]):
        draw_start_button()

    if status_rotate_wheel and wheelTurns < 6:
        rotate_wheel(current_number, correct_numbers[wheelTurns])
        status_rotate_wheel = False
        current_number = correct_numbers[wheelTurns]
        wheelTurns += 1

    if current_number == correct_numbers[wheelTurns - 1]:
        draw_final_wheel(current_number)


    draw_correct_numbers()

    if wheelTurns == 6:
        if status_add_money:    
            money +=  3 * int(count_correct_guesses()) ** 3
            status_add_money = False
        draw_end_message()
            
        if changingColorR < 255:
            changingColorR += 1
        if changingColorR == 255 and changingColorB < 255:
            changingColorB += 1
        if changingColorB == 255 and changingColorG < 255:
            changingColorG += 1

    pygame.display.update()


def main():
    global activeInput
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.MOUSEBUTTONDOWN:             
                if wheelTurns == 0:
                    for i in range(6):
                        if inputs[i].contains(event.pos):
                            activeInput = i
                            break
                    
                if button_rotate_wheel_polygon.collidepoint(event.pos):
                    global status_rotate_wheel
                    status_rotate_wheel = True
                    activeInput = None
                    if wheelTurns == 0:
                        create_correct_num_surfaces()
                    
            if event.type == pygame.KEYDOWN:
                if wheelTurns == 0:
                    if len(event.unicode) == 1:
                        inputs[activeInput].add(event.unicode)
                    if event.key == pygame.K_BACKSPACE:
                        inputs[activeInput].delete()
                    elif event.key == pygame.K_TAB:
                        activeInput = (activeInput + 1) % 6
                elif event.key == pygame.K_SPACE:
                    if wheelTurns == 6:
                        setup()
                        main()

        draw_window()
    
    pygame.quit()


main()
