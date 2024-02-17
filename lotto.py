import pygame
import random
from pathlib import Path

pygame.init()
pygame.font.init()
pygame.mixer.init()
random.seed()

WIDTH, HEIGHT = 720, 720
RANDOM_WHEEL_WIDTH, RANDOM_WHEEL_HEIGHT = 360, 360

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Lotto")

#Farben
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
DARK_OLIVE_GREEN = (87, 109, 34)
MONEY_GREEN = (80, 149, 56)
BROWN = (163, 85, 13)
YELLOW = (250, 207, 4)
RECT_ACTIVE = pygame.Color('lightskyblue3')
RECT_PASSIVE = pygame.Color('gray15')

changingColorR = 0
changingColorG = 0
changingColorB = 0


#WERTE
FPS = 60
money = 20
number_of_button_clicks = 0
current_number = 14
number_of_correct_number = 0
status_rotate_wheel = False
status_add_money = True
frequency = 1000
duration = 16


#Bilder
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

ZEIGER_GLÜCKSRAD_IMAGE = pygame.image.load(image_path / "pointer.png")

GELDSCHEINSYMBOL_IMAGE = pygame.image.load(image_path / "money.png")
GELDSCHEINSYMBOL = pygame.transform.scale(GELDSCHEINSYMBOL_IMAGE, (65,50))

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
        isCorrect = number_of_correct_number > 0 and correct_numbers[:number_of_correct_number].count(self.value) == 1
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
    while correct_number_1 == correct_number_2:     #Zahl darf nicht noch einmal genommen werden
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


#Textfelder

correct_number_font = pygame.font.Font(None, 32)
correct_number_text = "Gewinnerzahlen:"
correct_number_rect = pygame.Rect(520, 150, 150, 33)

choose_correct_numbers()

first_correct_number_font = pygame.font.Font(None,50)
first_correct_number_text = (str(correct_numbers[0]))
first_correct_number_rect = pygame.Rect(606, 200, 10, 30)

second_correct_number_font = pygame.font.Font(None,50)
second_correct_number_text = (str(correct_numbers[1]))
second_correct_number_rect = pygame.Rect(606, 250, 10, 30)

third_correct_number_font = pygame.font.Font(None,50)
third_correct_number_text = (str(correct_numbers[2]))
third_correct_number_rect = pygame.Rect(606, 300, 10, 30)

fourth_correct_number_font = pygame.font.Font(None,50)
fourth_correct_number_text = (str(correct_numbers[3]))
fourth_correct_number_rect = pygame.Rect(606, 350, 10, 30)

fifth_correct_number_font = pygame.font.Font(None,50)
fifth_correct_number_text = (str(correct_numbers[4]))
fifth_correct_number_rect = pygame.Rect(606, 400, 10, 30)

sixth_correct_number_font = pygame.font.Font(None,50)
sixth_correct_number_text = (str(correct_numbers[5]))
sixth_correct_number_rect = pygame.Rect(606, 450, 10, 30)

MONEY_FONT = pygame.font.SysFont('comicsans', 55)

button_rotate_wheel_font = pygame.font.Font(None, 50)
button_rotate_wheel_text = "RAD DREHEN"
button_rotate_wheel_polygon = pygame.draw.polygon(WIN, BROWN, ((245, 585), (495, 585), (235, 630), (485, 630)))


def setup():
    global current_number
    global number_of_correct_number
    global status_rotate_wheel
    global first_correct_number_text
    global second_correct_number_text
    global third_correct_number_text
    global fourth_correct_number_text
    global fifth_correct_number_text
    global sixth_correct_number_text
    global status_add_money
    global activeInput

    current_number = 14
    number_of_correct_number = 0
    status_rotate_wheel = False
    activeInput = 0

    choose_correct_numbers()

    first_correct_number_text = (str(correct_numbers[0]))
    second_correct_number_text = (str(correct_numbers[1]))
    third_correct_number_text = (str(correct_numbers[2]))
    fourth_correct_number_text = (str(correct_numbers[3]))
    fifth_correct_number_text = (str(correct_numbers[4]))
    sixth_correct_number_text = (str(correct_numbers[5]))

    status_add_money = True

    CHANGING_COLOR_R = 0
    CHANGING_COLOR_G = 0
    CHANGING_COLOR_B = 0


def button_rotate_wheel():
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
    total_time = 7.3469 * ( number_after_rotation - number_before_rotation + 49 * number_of_rotations) / (0.5 * 7.3469 * FPS)
    a = (7.3469 * ( number_after_rotation - number_before_rotation + 49 * number_of_rotations) - 7.3469 * FPS * total_time) * 2 / (total_time ** 2)
    angle = 7.3469 * (number_before_rotation - 14 + 49 ) + 7.3469
    while time < total_time:
        RANDOM_WHEEL_ROTATED, RANDOM_WHEEL_ROTATED_RECT = rotate(RANDOM_WHEEL, angle)
        WIN.blit(RANDOM_WHEEL_ROTATED, RANDOM_WHEEL_ROTATED_RECT)
        WIN.blit(ZEIGER_GLÜCKSRAD_IMAGE, (525, 322) )
        pygame.display.update(180, 180, 360, 360)
        time += 1 / FPS
        angle += (7.3469 + (a*time) / FPS)


def draw_final_wheel(number_of_the_wheel):
    FINAL_RANDOM_WHEEL, FINAL_RANDOM_WHEEL_RECT =  rotate(RANDOM_WHEEL, 360/49 * (number_of_the_wheel + 49 - 14.5))
    WIN.blit(FINAL_RANDOM_WHEEL, FINAL_RANDOM_WHEEL_RECT)
    WIN.blit(ZEIGER_GLÜCKSRAD_IMAGE, (525, 322) )


def draw_correct_numbers(number_of_wheel_rotations):
    color_of_correct_number = RED
    correct_number_font = pygame.font.Font(None,50)
    correct_number_rect = pygame.Rect(606, 150 + 50 * number_of_wheel_rotations, 10, 30)
    correct_number_text = (str(eval(f"correct_numbers[{int(number_of_wheel_rotations) - 1}]")))

    if number_of_wheel_rotations == 0:
        correct_number_text = "Gewinnerzahlen:"
        correct_number_font = pygame.font.Font(None, 32)
        correct_number_rect = pygame.Rect(520, 150 + 50 * number_of_wheel_rotations, 150, 33)
        color_of_correct_number = BLACK
    else:
        for guess in (it.value for it in inputs):
            if guess == correct_numbers[number_of_wheel_rotations - 1]:
                color_of_correct_number = MONEY_GREEN
                break
       
    correct_number_surface = correct_number_font.render(correct_number_text, True, color_of_correct_number)
    WIN.blit(correct_number_surface, (correct_number_rect.x + 5, correct_number_rect.y + 5))


def anzahl_correct_guesses():
    correct_guesses = 0
    for guess in (it.value for it in inputs):
        for correctNum in correct_numbers:
            if guess == correctNum:
                correct_guesses += 1
                break

    return correct_guesses


def end_of_round():
    end_of_round_font = pygame.font.Font(None, 75)

    # end_of_round_rect = pygame.Rect(360 - (end_of_round_text.get_width()) / 2, 360 - (end_of_round_text.get_height() / 2),end_of_round_text.get_width(), end_of_round_text.get_height())
    # WIN.blit(end_of_round_text, (250, 250))
    parts_of_end_of_round_text = ["Du hast " + str(anzahl_correct_guesses()) , "Zahlen richtig geraten.", "SPACE zum erneut spielen"]
    if anzahl_correct_guesses == 1:
        parts_of_end_of_round_text = ["Du hast 1 Zahl richtig geraten.", "SPACE zum erneut spielen"]

    
        # text_n = eval(f"end_of_round_text_{n}")
        # rect_n = eval(f"end_of_round_rect_{n}")
        
        # text_n = end_of_round_font.render(parts_of_end_of_round_text[n], 1, BLACK)
        # rect_n = pygame.Rect(360 - (exec(f"end_of_round_text_{n}" + ".get_width()")) / 2, 360 - n * 30- (exec(f"end_of_round_text_{n}" + ".get_height()")) / 2, exec(f"end_of_round_text_{n}" + ".get_width()"), exec(f"end_of_round_text_{n}" + ".get_height()"))
        # WIN.blit(eval(text_n, (eval(f"end_of_round_rect_{n}.x"), eval(f"end_of_round_rect_{n}.y") ) )
    
    text_1 = end_of_round_font.render(parts_of_end_of_round_text[0], 1, (changingColorR, changingColorG, changingColorB))
    text_2 = end_of_round_font.render(parts_of_end_of_round_text[1], 1, (changingColorR, changingColorG, changingColorB))
    text_3 = end_of_round_font.render(parts_of_end_of_round_text[2], 1, (changingColorR, changingColorG, changingColorB))
    rect_1 = pygame.Rect(360 - text_1.get_width() / 2, 360 - 1 * 60- text_1.get_height() / 2, text_1.get_width() , text_1.get_height())
    rect_2 = pygame.Rect(360 - text_2.get_width() / 2, 360 + 0 * 60- text_2.get_height() / 2, text_2.get_width() , text_2.get_height())
    rect_3 = pygame.Rect(360 - text_3.get_width() / 2, 360 + 1 * 60- text_3.get_height() / 2, text_3.get_width() , text_3.get_height())

    WIN.blit(text_1, (rect_1.x, rect_1.y))
    WIN.blit(text_2, (rect_2.x, rect_2.y))
    WIN.blit(text_3, (rect_3.x, rect_3.y))

    status_add_money = False


def draw_window():
    global status_rotate_wheel
    global number_of_correct_number
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
    WIN.blit(ZEIGER_GLÜCKSRAD_IMAGE, (525, 322) )

    if status_rotate_wheel and number_of_correct_number < 6:
        if number_of_correct_number == 0:
            money -= 5
    money_text = MONEY_FONT.render(" = "+ str(money), 1, MONEY_GREEN)
    WIN.blit(GELDSCHEINSYMBOL, (278, 45))
    WIN.blit(money_text, (GELDSCHEINSYMBOL.get_width() + 278, 55 ))
    pygame.display.update(250, 5, 200, 100)

    for field in inputs: field.draw()

    if all([it.value for it in inputs]):
        button_rotate_wheel()

    if status_rotate_wheel and number_of_correct_number < 6:
        rotate_wheel(current_number, eval("correct_numbers[" + str(number_of_correct_number) + "]"))
        status_rotate_wheel = False
        current_number = eval("correct_numbers[" + str(number_of_correct_number) + "]")
        number_of_correct_number += 1

    if current_number == eval("correct_numbers[" + str(number_of_correct_number - 1) + "]"):
        draw_final_wheel(current_number)

    for i in range(number_of_correct_number + 1):
        draw_correct_numbers(i)

    if number_of_correct_number == 6:
        while status_add_money:    
            money +=  3 * int(anzahl_correct_guesses()) ** 3
            status_add_money = False
        end_of_round()
            
        if changingColorR < 255:
            changingColorR += 1
        if changingColorR == 255 and changingColorB < 255:
            changingColorB += 1
        if changingColorB == 255 and changingColorG < 255:
            changingColorG += 1

    pygame.display.update()


def main():
    wheel = RANDOM_WHEEL.get_rect(center = (360,360))

    clock = pygame.time.Clock()
    run = True

    global activeInput

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.MOUSEBUTTONDOWN:               
                #Auswählen der Felder für Zahleneingabe               
                if number_of_correct_number == 0:
                    for i in range(6):
                        if inputs[i].contains(event.pos):
                            activeInput = i
                            break
                    
                if button_rotate_wheel_polygon.collidepoint(event.pos):
                    global status_rotate_wheel
                    status_rotate_wheel = True
                    activeInput = None
                    
            if event.type == pygame.KEYDOWN:
                if number_of_correct_number == 0:
                    if len(event.unicode) == 1:
                        inputs[activeInput].add(event.unicode)
                    if event.key == pygame.K_BACKSPACE:
                        inputs[activeInput].delete()
                    elif event.key == pygame.K_TAB:
                        activeInput = (activeInput + 1) % 6
                elif event.key == pygame.K_SPACE:
                    if number_of_correct_number == 6:
                        setup()
                        main()

        draw_window()
    
    pygame.quit()


main()
