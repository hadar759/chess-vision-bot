import pytesseract
from PIL import ImageGrab
from pynput.mouse import Button, Controller
import time
import keyboard

SCREENSHOT_LOCATION = r"monitor-1.png"
SQUARE_SIZE = 113
squares = {}
CLICK_NUM = 500
run = True


def exit_():
    global run
    run = False


def main():
    # So we're able to quit if the game finished before the bot
    keyboard.add_hotkey("f8", exit_)
    mouse = Controller()
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # Crop the image
    for i in range(1, 9):
        squares[i] = 120 + (8 - i + 1) * SQUARE_SIZE - 50
    # Create an array of letters and numbers representing the squares on the screen
    for i in range(0, 8):
        bruh = ord("a") + i
        squares[chr(bruh)] = 315 + (bruh - ord("a") + 1) * SQUARE_SIZE - 50
    global CLICK_NUM
    clicks = 0
    while run:
        # Parse the image and see where to click
        square = get_square_location(pytesseract.image_to_string(get_image(),
                                           config='-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=abcdefgh012345678'))[:2]
        mouse.position = square
        for i in range(CLICK_NUM):
            mouse.click(Button.left)
        clicks += 1
        # The game gets stuck after so many clicks (it clicks 500 times
        # at once on a single block)
        if clicks == 3:
            CLICK_NUM = 250
        # Typical time it takes the website to respond
        time.sleep(4 + clicks / 2)


def fix_edge_cases(square_cords):
    """Tesseract misinterprets the blocks sometimes, so this manually fixes it"""
    if square_cords[1] == "g":
        square_cords = "a8"
    elif square_cords[1] == "c":
        square_cords = "c5"
    elif square_cords[1] == "\n":
        if square_cords[0] == "a":
            square_cords = "a1"
        elif square_cords[0] == "4":
            square_cords = "f4"
        else:
            square_cords = "c" + square_cords
    return square_cords

def get_square_location(square_cords):
    square_cords = fix_edge_cases(square_cords)
    return squares[square_cords[0]], squares[int(square_cords[1])]


def get_image():
    """Crop the image so only the relevant info stays"""
    left = 1500
    upper = 146
    right = 1550
    bottom = 175
    return ImageGrab.grab().crop((left, upper, right, bottom))


if __name__ == '__main__':
    main()
