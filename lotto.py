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
color_of_rect_1 = RECT_PASSIVE
color_of_rect_2 = RECT_PASSIVE
color_of_rect_3 = RECT_PASSIVE
color_of_rect_4 = RECT_PASSIVE
color_of_rect_5 = RECT_PASSIVE
color_of_rect_6 = RECT_PASSIVE


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


#Auswählen der Felder für Zahleingabe
active_1 = False
active_2 = False
active_3 = False
active_4 = False
active_5 = False
active_6 = False

#nur Eingeben einer maximal zweistelligen Zahl möglich
count_digits_1 = 0
count_digits_2 = 0
count_digits_3 = 0
count_digits_4 = 0
count_digits_5 = 0
count_digits_6 = 0

# Geratene Zahlen
guess = ["0", "0", "0", "0", "0", "0"]

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

first_number_font = pygame.font.Font(None, 32)
first_number_text = "Zahl 1: "
first_number_rect = pygame.Rect(50, 200, 80, 30)

second_number_font = pygame.font.Font(None, 32)
second_number_text = "Zahl 2: "
second_number_rect = pygame.Rect(50, 250, 80, 30)

third_number_font = pygame.font.Font(None, 32)
third_number_text = "Zahl 3: "
third_number_rect = pygame.Rect(50, 300, 80, 30)

fourth_number_font = pygame.font.Font(None, 32)
fourth_number_text = "Zahl 4: "
fourth_number_rect = pygame.Rect(50, 350, 80, 30)

fifth_number_font = pygame.font.Font(None, 32)
fifth_number_text = "Zahl 5: "
fifth_number_rect = pygame.Rect(50, 400, 80, 30)

sixth_number_font = pygame.font.Font(None, 32)
sixth_number_text = "Zahl 6: "
sixth_number_rect = pygame.Rect(50, 450, 80, 30)


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
    global color_of_rect_1
    global color_of_rect_2
    global color_of_rect_3
    global color_of_rect_4
    global color_of_rect_5
    global color_of_rect_6
    global current_number
    global number_of_correct_number
    global status_rotate_wheel
    global count_digits_1
    global count_digits_2
    global count_digits_3
    global count_digits_4
    global count_digits_5
    global count_digits_6
    global guess
    global first_correct_number_text
    global second_correct_number_text
    global third_correct_number_text
    global fourth_correct_number_text
    global fifth_correct_number_text
    global sixth_correct_number_text
    global first_number_text
    global second_number_text
    global third_number_text
    global fourth_number_text
    global fifth_number_text
    global sixth_number_text
    global status_add_money
    
    color_of_rect_1 = RECT_PASSIVE
    color_of_rect_2 = RECT_PASSIVE
    color_of_rect_3 = RECT_PASSIVE
    color_of_rect_4 = RECT_PASSIVE
    color_of_rect_5 = RECT_PASSIVE
    color_of_rect_6 = RECT_PASSIVE

    current_number = 14
    number_of_correct_number = 0
    status_rotate_wheel = False

    count_digits_1 = 0
    count_digits_2 = 0
    count_digits_3 = 0
    count_digits_4 = 0
    count_digits_5 = 0
    count_digits_6 = 0

    guess = ["0", "0", "0", "0", "0", "0"]

    choose_correct_numbers()

    first_number_text = "Zahl 1: "
    second_number_text = "Zahl 2: "
    third_number_text = "Zahl 3: "
    fourth_number_text = "Zahl 4: "
    fifth_number_text = "Zahl 5: "
    sixth_number_text = "Zahl 6: "

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


def del_letter():
    global first_number_text
    global count_digits_1
    global second_number_text
    global count_digits_2
    global third_number_text
    global count_digits_3
    global fourth_number_text
    global count_digits_4
    global fifth_number_text
    global count_digits_5
    global sixth_number_text
    global count_digits_6

    if active_1 and count_digits_1 >= 0:
        first_number_text = first_number_text[0:-1]
        guess[0] = guess[0][:-1]
        count_digits_1 -= 1
    if active_2 and count_digits_2 >= 0:
        second_number_text = second_number_text[0:-1]
        guess[1] = guess[1][:-1]
        count_digits_2 -= 1
    if active_3 and count_digits_3 >= 0:
        third_number_text = third_number_text[0:-1]
        guess[2] = guess[2][:-1]
        count_digits_3 -= 1
    if active_4 and count_digits_4 >= 0:
        fourth_number_text = fourth_number_text[0:-1]
        guess[3] = guess[3][:-1]
        count_digits_4 -= 1
    if active_5 and count_digits_5 >= 0:
        fifth_number_text = fifth_number_text[0:-1]
        guess[4] = guess[4][:-1]
        count_digits_5 -= 1
    if active_6 and count_digits_6 >= 0:
        sixth_number_text = sixth_number_text[0:-1]
        guess[5] = guess[5][:-1]
        count_digits_6 -= 1


def add_letter(event):
    global first_number_text
    global second_number_text
    global third_number_text
    global fourth_number_text
    global fifth_number_text
    global sixth_number_text
    global count_digits_1
    global count_digits_2
    global count_digits_3
    global count_digits_4
    global count_digits_5
    global count_digits_6

    if active_1 and count_digits_1 < 2:
        first_number_text += event.unicode
        guess[0] += str(event.unicode)
        count_digits_1 += 1
    if active_2 and count_digits_2 < 2:
        second_number_text += event.unicode
        guess[1] += str(event.unicode)
        count_digits_2 += 1
    if active_3 and count_digits_3 < 2:
        third_number_text += event.unicode
        guess[2] += str(event.unicode)
        count_digits_3 += 1
    if active_4 and count_digits_4 < 2:
        fourth_number_text += event.unicode
        guess[3] += str(event.unicode)
        count_digits_4 += 1
    if active_5 and count_digits_5 < 2:
        fifth_number_text += event.unicode
        guess[4] += str(event.unicode)
        count_digits_5 += 1
    if active_6 and count_digits_6 < 2:
        sixth_number_text += event.unicode
        guess[5] += str(event.unicode)
        count_digits_6 += 1


def jump_to_next_feld(active_11, active_22, active_33, active_44, active_55, active_66 ):
    if not (active_11 or active_22 or active_33 or active_44 or active_66) and active_55:
        active_1 = False
        active_2 = False
        active_3 = False
        active_4 = False
        active_5 = False
        active_6 = True 

    if not (active_11 or active_22 or active_33 or active_55 or active_66) and active_44:
        active_1 = False
        active_2 = False
        active_3 = False
        active_4 = False
        active_5 = True
        active_6 = False  

    if not (active_11 or active_22 or active_44 or active_55 or active_66) and active_33:
        active_1 = False
        active_2 = False
        active_3 = False
        active_4 = True
        active_5 = False
        active_6 = False  

    if not (active_11 or active_33 or active_44 or active_55 or active_66) and active_22:
        active_1 = False
        active_2 = False
        active_3 = True
        active_4 = False
        active_5 = False
        active_6 = False                    
                        
    if active_11 and not active_22 and not active_33 and not active_44 and not active_55 and not active_66:
        active_1 = False
        active_2 = True
        active_3 = False
        active_4 = False
        active_5 = False
        active_6 = False


def feld_zahl_1(active_1):
    if (correct_numbers[0] == int(guess[0]) and number_of_button_clicks >= 1) or ( correct_numbers[1] == int(guess[0]) and number_of_button_clicks >= 2) \
    or ( correct_numbers[2] == int(guess[0]) and number_of_button_clicks >= 3) or ( correct_numbers[3] == int(guess[0]) and number_of_button_clicks >= 4) \
    or ( correct_numbers[4] == int(guess[0]) and number_of_button_clicks >= 5) or ( correct_numbers[5] == int(guess[0]) and number_of_button_clicks == 6):
        color_of_number_1 = GREEN
    else:
        color_of_number_1 = BLACK

    number_one_surface = first_number_font.render(first_number_text, True, color_of_number_1)
    WIN.blit(number_one_surface, (first_number_rect.x + 5, first_number_rect.y + 5))                       
    if active_1:
        color_of_rect_1 = RECT_ACTIVE
    else:
        color_of_rect_1 = RECT_PASSIVE
    pygame.draw.rect(WIN, color_of_rect_1, first_number_rect, 2)
    first_number_rect.w = max(80, number_one_surface.get_width() + 10)


def feld_zahl_2(active_2):
    if (correct_numbers[0] == int(guess[1]) and number_of_button_clicks >= 1) or ( correct_numbers[1] == int(guess[1]) and number_of_button_clicks >= 2) \
    or ( correct_numbers[2] == int(guess[1]) and number_of_button_clicks >= 3) or ( correct_numbers[3] == int(guess[1]) and number_of_button_clicks >= 4) \
    or ( correct_numbers[4] == int(guess[1]) and number_of_button_clicks >= 5) or ( correct_numbers[5] == int(guess[1]) and number_of_button_clicks == 6):
        color_of_number_2 = GREEN
    else:
        color_of_number_2 = BLACK

    number_two_surface = second_number_font.render(second_number_text, True, color_of_number_2)
    WIN.blit(number_two_surface, (second_number_rect.x + 5, second_number_rect.y + 5))                       
    if active_2:
        color_of_rect_2 = RECT_ACTIVE
    else:
        color_of_rect_2 = RECT_PASSIVE
    pygame.draw.rect(WIN, color_of_rect_2, second_number_rect, 2)
    second_number_rect.w = max(80, number_two_surface.get_width() + 10)


def feld_zahl_3(active_3):
    if (correct_numbers[0] == int(guess[2]) and number_of_button_clicks >= 1) or ( correct_numbers[1] == int(guess[2]) and number_of_button_clicks >= 2) \
    or ( correct_numbers[2] == int(guess[2]) and number_of_button_clicks >= 3) or ( correct_numbers[3] == int(guess[2]) and number_of_button_clicks >= 4) \
    or ( correct_numbers[4] == int(guess[2]) and number_of_button_clicks >= 5) or ( correct_numbers[5] == int(guess[2]) and number_of_button_clicks >= 6):
        color_of_number_3 = GREEN
    else:
        color_of_number_3 = BLACK

    number_three_surface = third_number_font.render(third_number_text, True, color_of_number_3)
    WIN.blit(number_three_surface, (third_number_rect.x + 5, third_number_rect.y + 5))                       
    if active_3:
        color_of_rect_3 = RECT_ACTIVE
    else:
        color_of_rect_3 = RECT_PASSIVE
    pygame.draw.rect(WIN, color_of_rect_3, third_number_rect, 2)
    third_number_rect.w = max(80, number_three_surface.get_width() + 10)

    if active_3:
        color_of_rect_3 = RECT_ACTIVE
    else:
        color_of_rect_3 = RECT_PASSIVE


def feld_zahl_4(active_4):
    if (correct_numbers[0] == int(guess[3]) and number_of_button_clicks >= 1) or ( correct_numbers[1] == int(guess[3]) and number_of_button_clicks >= 2) \
    or ( correct_numbers[2] == int(guess[3]) and number_of_button_clicks >= 3) or ( correct_numbers[3] == int(guess[3]) and number_of_button_clicks >= 4) \
    or ( correct_numbers[4] == int(guess[3]) and number_of_button_clicks >= 5) or ( correct_numbers[5] == int(guess[3]) and number_of_button_clicks >= 6):
        color_of_number_4 = GREEN
    else:
        color_of_number_4 = BLACK

    number_four_surface = fourth_number_font.render(fourth_number_text, True, color_of_number_4)
    WIN.blit(number_four_surface, (fourth_number_rect.x + 5, fourth_number_rect.y + 5))                       
    if active_4:
        color_of_rect_4 = RECT_ACTIVE
    else:
        color_of_rect_4 = RECT_PASSIVE
    pygame.draw.rect(WIN, color_of_rect_4, fourth_number_rect, 2)
    fourth_number_rect.w = max(80, number_four_surface.get_width() + 10)


def feld_zahl_5(active_5):
    if (correct_numbers[0] == int(guess[4]) and number_of_button_clicks >= 1) or ( correct_numbers[1] == int(guess[4]) and number_of_button_clicks >= 2) \
    or ( correct_numbers[2] == int(guess[4]) and number_of_button_clicks >= 3) or ( correct_numbers[3] == int(guess[4]) and number_of_button_clicks >= 4) \
    or ( correct_numbers[4] == int(guess[4]) and number_of_button_clicks >= 5) or ( correct_numbers[5] == int(guess[4]) and number_of_button_clicks == 6):
        color_of_number_5 = GREEN
    else:
        color_of_number_5 = BLACK

    number_five_surface = fifth_number_font.render(fifth_number_text, True, color_of_number_5)
    WIN.blit(number_five_surface, (fifth_number_rect.x + 5, fifth_number_rect.y + 5))                       
    if active_5:
        color_of_rect_5 = RECT_ACTIVE
    else:
        color_of_rect_5 = RECT_PASSIVE
    pygame.draw.rect(WIN, color_of_rect_5, fifth_number_rect, 2)
    fifth_number_rect.w = max(80, number_five_surface.get_width() + 10)


def feld_zahl_6(active_6):
    if (correct_numbers[0] == int(guess[5]) and number_of_button_clicks >= 1) or ( correct_numbers[1] == int(guess[5]) and number_of_button_clicks >= 2) \
    or ( correct_numbers[2] == int(guess[5]) and number_of_button_clicks >= 3) or ( correct_numbers[3] == int(guess[5]) and number_of_button_clicks >= 4) \
    or ( correct_numbers[4] == int(guess[5]) and number_of_button_clicks >= 5) or ( correct_numbers[5] == int(guess[5]) and number_of_button_clicks == 6):
        color_of_number_6 = GREEN
    else:
        color_of_number_6 = BLACK

    number_six_surface = sixth_number_font.render(sixth_number_text, True, color_of_number_6)
    WIN.blit(number_six_surface, (sixth_number_rect.x + 5, sixth_number_rect.y + 5))                       
    if active_6:
        color_of_rect_6 = RECT_ACTIVE
    else:
        color_of_rect_6 = RECT_PASSIVE
    pygame.draw.rect(WIN, color_of_rect_6, sixth_number_rect, 2)
    sixth_number_rect.w = max(80, number_six_surface.get_width() + 10)

    if active_6:
        color_of_rect_6 = RECT_ACTIVE
    else:
        color_of_rect_6 = RECT_PASSIVE


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
        for g in guess:
            if int(g) == correct_numbers[number_of_wheel_rotations - 1]:
                color_of_correct_number = MONEY_GREEN
       
    correct_number_surface = correct_number_font.render(correct_number_text, True, color_of_correct_number)
    WIN.blit(correct_number_surface, (correct_number_rect.x + 5, correct_number_rect.y + 5))


def anzahl_correct_guesses():
    correct_guesses = 0
    for zahl in guess:
        correct_guesses += correct_numbers.count(int(zahl))

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

    feld_zahl_1(active_1)
    feld_zahl_2(active_2)
    feld_zahl_3(active_3)
    feld_zahl_4(active_4)
    feld_zahl_5(active_5)
    feld_zahl_6(active_6)

    if 1 <= int(guess[0]) <= 49 and 1 <= int(guess[1]) <= 49 and 1 <= int(guess[2]) <= 49 and 1 <= int(guess[3]) <= 49 \
                and 1 <= int(guess[4]) <= 49 and 1 <= int(guess[5]) <= 49 :
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

    #Global declarations
    global active_1
    global active_2
    global active_3
    global active_4
    global active_5
    global active_6

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            if event.type == pygame.MOUSEBUTTONDOWN:               
                #Auswählen der Felder für Zahleneingabe               
                if number_of_correct_number == 0:
                    if first_number_rect.collidepoint(event.pos):
                        active_1 = True
                        active_2 = False
                        active_3 = False
                        active_4 = False
                        active_5 = False
                        active_6 = False
                    if second_number_rect.collidepoint(event.pos):
                        active_2 = True
                        active_1 = False
                        active_3 = False
                        active_4 = False
                        active_5 = False
                        active_6 = False                
                    if third_number_rect.collidepoint(event.pos):
                        active_3 = True
                        active_1 = False
                        active_2 = False
                        active_4 = False
                        active_5 = False
                        active_6 = False 
                    if fourth_number_rect.collidepoint(event.pos):
                        active_4 = True
                        active_1 = False
                        active_2 = False
                        active_3 = False
                        active_5 = False
                        active_6 = False
                    if fifth_number_rect.collidepoint(event.pos):
                        active_5 = True
                        active_1 = False
                        active_2 = False
                        active_3 = False
                        active_4 = False
                        active_6 = False
                    if sixth_number_rect.collidepoint(event.pos):
                        active_6 = True
                        active_1 = False
                        active_2 = False
                        active_3 = False
                        active_4 = False
                        active_5 = False
                    
                if button_rotate_wheel_polygon.collidepoint(event.pos):
                    global status_rotate_wheel
                    
                    status_rotate_wheel = True
                    active_6 = False
                    active_1 = False
                    active_2 = False
                    active_3 = False
                    active_4 = False
                    active_5 = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    del_letter()

                if event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 \
                or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 \
                or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                    add_letter(event)

                if event.key == pygame.K_TAB:
                    jump_to_next_feld(active_1, active_2, active_3, active_4, active_5, active_6)

                if event.key == pygame.K_SPACE:
                    if number_of_correct_number == 6:
                        setup()
                        main()

        draw_window()
    
    pygame.quit()


main()
