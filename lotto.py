import pygame
import random
from pathlib import Path

random.seed()
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 720, 720
RANDOM_WHEEL_WIDTH, RANDOM_WHEEL_HEIGHT = 360, 360
FPS = 60
COST = 5
NUMBER_OF_ROTATIONS = 5
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DARK_OLIVE_GREEN = (87, 109, 34)
GREEN = (80, 149, 56)
BROWN = (163, 85, 13)
YELLOW = (250, 207, 4)
RECT_ACTIVE = pygame.Color('lightskyblue3')
RECT_PASSIVE = pygame.Color('gray15')
END_MESSAGE_COLOR = (0, 0, 0)

money = 20
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
rotated_wheel = RANDOM_WHEEL
rotated_wheel_rect = RANDOM_WHEEL_RECT

WHEEL_OF_FORTUNE_SURROUNDING_IMAGE = pygame.image.load(image_path / "wheel_of_fortune_surrounding.png")
WHEEL_OF_FORTUNE_SURROUNDING = pygame.transform.scale(WHEEL_OF_FORTUNE_SURROUNDING_IMAGE, (423,491))
WHEEL_OF_FORTUNE_SURROUNDING_RECT = WHEEL_OF_FORTUNE_SURROUNDING.get_rect(center = (366,401))

WHEEL_POINTER_IMAGE = pygame.image.load(image_path / "pointer.png")

MONEY_IMAGE = pygame.image.load(image_path / "money.png")
MONEY_SYMBOL = pygame.transform.scale(MONEY_IMAGE, (65,50))

BACKGROUND_IMAGE = pygame.image.load(image_path / "sunburst_background.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (720, 720))


START_BUTTON_RECT = pygame.rect.Rect(245, 585, 235, 45)
START_BUTTON_SURFACE = pygame.font.Font(None, 50).render("RAD DREHEN", True, YELLOW)
MONEY_FONT = pygame.font.SysFont('comicsans', 55)
INPUT_FONT = pygame.font.Font(None, 32)
CORRECT_NUMBER_FONT = pygame.font.Font(None, 50)
CORRECT_NUMBER_HEADING = pygame.font.Font(None, 32).render("Gewinnerzahlen:", True, BLACK)
END_OF_ROUND_FONT = pygame.font.Font(None, 75)
money_text = MONEY_FONT.render(" = " + str(STARTING_MONEY), True, GREEN)
endMessages = [END_OF_ROUND_FONT.render(part, True, END_MESSAGE_COLOR) for part in ["", "Zahlen richtig geraten.", "SPACE zum erneut spielen"]]
endMessageCoords = []

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
correctNumSurfaces = []


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


def setup():
    global wheelTurns
    global status_rotate_wheel
    global status_add_money
    global activeInput
    global correctNumSurfaces

    wheelTurns = 0
    status_rotate_wheel = False
    activeInput = 0
    status_add_money = True

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
    pygame.draw.rect(WIN, BROWN, START_BUTTON_RECT)
    WIN.blit(START_BUTTON_SURFACE, (WIDTH/2 - START_BUTTON_SURFACE.get_width()/2, 594))


def rotate(surface, angle):
    rotated_wheel = pygame.transform.rotozoom(surface, angle, 1)
    rotated_wheel_rect = rotated_wheel.get_rect(center = (360,360))
    return rotated_wheel, rotated_wheel_rect


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


def create_end_message():
    global endMessageCoords
    endMessages[0] = END_OF_ROUND_FONT.render("Du hast " + str(count_correct_guesses()), 1, END_MESSAGE_COLOR)
    endMessageCoords = [(360 - line.get_width()/2, 330 + (i-1) * 60 - line.get_height()/2) for i, line in enumerate(endMessages)]


def draw_end_message():
    for line, pos in zip(endMessages, endMessageCoords):
        WIN.blit(line, pos)


def update_money_text(money):
    global money_text
    money_text = MONEY_FONT.render(" = " + str(money), True, GREEN)


def draw_window():  # TODO: update only the changed parts of the screen
    WIN.fill((BLACK))
    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(WHEEL_OF_FORTUNE_SURROUNDING, WHEEL_OF_FORTUNE_SURROUNDING_RECT)
    WIN.blit(MONEY_SYMBOL, (278, 45))
    WIN.blit(money_text, (MONEY_SYMBOL.get_width() + 278, 55))
    WIN.blit(rotated_wheel, rotated_wheel_rect)
    WIN.blit(WHEEL_POINTER_IMAGE, (525, 322))

    for field in inputs: field.draw()

    if all([it.value for it in inputs]):
        draw_start_button()

    draw_correct_numbers()

    if wheelTurns == 6:
        draw_end_message()

    pygame.display.update()


def main():
    global activeInput, status_rotate_wheel, rotated_wheel, rotated_wheel_rect, wheelTurns, status_add_money, money
    setup()
    clock = pygame.time.Clock()

    frames_since_rotation_start = 0
    total_frames: float
    a: float
    angle: float

    run = True
    while run:
        clock.tick(FPS)

        if wheelTurns == 6 and status_add_money:    
            money += 3 * count_correct_guesses() ** 3
            update_money_text(money)
            status_add_money = False

        if status_rotate_wheel:
            if frames_since_rotation_start == 0:
                current_number = 14 if wheelTurns == 0 else correct_numbers[wheelTurns-1]
                next_number = correct_numbers[wheelTurns]
                total_frames = (next_number - current_number + 49 * NUMBER_OF_ROTATIONS) / (0.5)
                a = 360/49 * ((next_number - current_number + 49 * NUMBER_OF_ROTATIONS) - total_frames) * 2 / ((total_frames/FPS) ** 2)
                angle = 360/49 * (current_number - 14 + 49 + 1)
                frames_since_rotation_start = 1
            if frames_since_rotation_start < total_frames:
                rotated_wheel, rotated_wheel_rect = rotate(RANDOM_WHEEL, angle)
                frames_since_rotation_start += 1
                angle += 360/49 + a*frames_since_rotation_start/FPS**2
            else:
                rotated_wheel, rotated_wheel_rect = rotate(RANDOM_WHEEL, 360/49 * (correct_numbers[wheelTurns] + 49 - 14.5))
                status_rotate_wheel = False
                frames_since_rotation_start = 0
                wheelTurns += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                continue

            if status_rotate_wheel: continue

            elif event.type == pygame.MOUSEBUTTONDOWN:             
                if wheelTurns == 0:
                    for i in range(6):
                        if inputs[i].contains(event.pos):
                            activeInput = i
                            break
                    
                if START_BUTTON_RECT.collidepoint(event.pos):
                    status_rotate_wheel = True
                    activeInput = None
                    if wheelTurns == 0:
                        money -= COST
                        update_money_text(money)
                        create_correct_num_surfaces()
                        create_end_message()
                    
            elif event.type == pygame.KEYDOWN:
                if wheelTurns == 0:
                    if len(event.unicode) == 1:
                        inputs[activeInput].add(event.unicode)
                    if event.key == pygame.K_BACKSPACE:
                        inputs[activeInput].delete()
                    elif event.key == pygame.K_TAB:
                        activeInput = (activeInput + 1) % 6
                elif event.key == pygame.K_SPACE and wheelTurns == 6:
                    main()

        draw_window()
    
    pygame.quit()



WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Lotto")
main()
