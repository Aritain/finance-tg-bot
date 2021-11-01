from telegram import ReplyKeyboardMarkup
from settings import CATEGORIES, CANCEL_CAPTION, NO_COMMENT_CAPTION


def create_category_keyboard():
    if len(CATEGORIES) % 2 == 0:
        row_amount = len(CATEGORIES) // 2
    else:
        row_amount = len(CATEGORIES) // 2 + 1

    keyboard = []
    for i in range(0, row_amount):
        try:
            keyboard.append([CATEGORIES[i*2], CATEGORIES[i*2+1]])
        except IndexError:
            keyboard.append([CATEGORIES[i*2]])

    if len(keyboard[-1]) == 1:
        keyboard[-1].append(CANCEL_CAPTION)
    else:
        keyboard.append([CANCEL_CAPTION])

    return keyboard


def category_keyboard():
    keyboard = create_category_keyboard()
    return ReplyKeyboardMarkup(keyboard, row_width=1, resize_keyboard=True)


def comment_keyboard():
    return ReplyKeyboardMarkup([
        [NO_COMMENT_CAPTION], [CANCEL_CAPTION]
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)


def cancel_keyboard():
    return ReplyKeyboardMarkup([
        [CANCEL_CAPTION]
    ], one_time_keyboard=True, row_width=1, resize_keyboard=True)
