from PIL import Image
import os
import uuid


FONT = "default_font"
PDF_NAME = "final_output.pdf"
OUTPUT_FILE = "text.txt"
BG = Image.open(f"{FONT}/bg.png")
sizeOfSheet = BG.width
gap, _ = 0, 0
allowedChars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.-?!() 1234567890'


def reset():
    global gap, _, BG, sizeOfSheet
    gap, _ = 0, 0
    BG = Image.open(f"{FONT}/bg.png")
    sizeOfSheet = BG.width


def writer(letter):
    global gap, _
    if letter == '\n':
        pass
    else:
        letter.lower()
        if letter == "":
            return
        cases = Image.open(f"{FONT}/{letter}.png")
        cases = cases.resize((90, 120))
        BG.paste(cases, (gap, _))
        size = cases.width
        gap += size
        del cases


def letter_writer(word):
    global gap, _
    if gap > sizeOfSheet - 70 * (len(word)):  # 95
        gap = 0
        _ += 200
    if gap == 0:
        writer("space")
    for letter in word:
        special_symbols = {
            ".": "fullstop",
            "!": "exclamation",
            "?": "question",
            "(": "circlebraketopen",
            ")": "circlebraketclose",
            "-": "hiphen",
            ",": "comma",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "0": "0"
        }
        if letter in allowedChars:
            if letter.islower():
                pass
            elif letter.isupper():
                letter = letter.lower()
                letter += 'upper'
            else:
                letter = special_symbols.get(letter, '`')

            if letter[-1] == "`":
                letter = letter[0:-2]

            writer(letter)


def word_input(input):
    word_list = input.split(' ')
    for data in word_list:
        letter_writer(data)
        writer('space')


def pdf_creation(png_file, flag=False):
    pil_img = Image.open(png_file)
    rgb = Image.new('RGB', pil_img.size, (255, 255, 255))  # white background
    rgb.paste(pil_img, mask=pil_img.split()[3])  # paste using alpha channel as mask
    rgb.save(f'{PDF_NAME}', append=flag)  # Now save multiple images in same pdf file


def converter(font="font"):
    global BG, sizeOfSheet, allowedChars, gap, FONT
    FONT = font
    p = 0
    export_path = str(uuid.uuid4())
    if not os.path.exists(export_path):
        os.mkdir(export_path)
    try:
        with open(f'{OUTPUT_FILE}', 'r') as file:
            data = file.read().replace('\n', ' ')

        nn = len(data) // 600
        chunks, chunk_size = len(data), len(data) // (nn + 1)
        p = [data[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

        for i in range(0, len(p)):
            word_input(p[i])
            writer('\n')
            BG.save(f'{export_path}/{i}_exported.png')
            bg_prev = Image.open(f"{FONT}/bg.png")
            BG = bg_prev
            gap = 0
            _ = 0
    except ValueError as E:
        print("{}\nTry again".format(E))

    image_list = []
    for i in range(0, len(p)):
        image_list.append(f'{export_path}/{i}_exported.png')

    returning_list = image_list.copy()

    # First create a pdf file if not created
    pdf_creation(image_list.pop(0))

    # # Now I am opening each images and converting them to pdf
    # # Appending them to pdfs
    #
    for PNG_FILE in image_list:
        pdf_creation(PNG_FILE, flag=True)

    reset()
    return returning_list


if __name__ == '__main__':
    _ = converter()
