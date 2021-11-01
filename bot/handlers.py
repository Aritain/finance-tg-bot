import telegram
import datetime
import pymongo
import os
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

from telegram.ext import ConversationHandler
from settings import (
    ERROR_VALUE_MSG, CATEGORY_ASK_MSG, SUCCESS_MESSAGE,
    CATEGORIES, COMMENT_ASK_MSG, MAX_COMMENT_LEN, ERROR_COMMENT_MSG,
    MONGO_USER, MONGO_PASS, MONGO_ADDR, MONGO_PORT, CANCEL_MESSAGE,
    NO_COMMENT_CAPTION, USERS, REPORT_30_DAYS, REPORT_THIS_MONTH,
    GOOGLE_SPREADSHEET
)
from keyboards import category_keyboard, cancel_keyboard, comment_keyboard
from utils import validate_input, compile_message


def add_start(update, context):
    if update.effective_user.id not in USERS and USERS:
        return ConversationHandler.END
    amount = update.message.text
    amount = validate_input(amount)
    if amount is False:
        update.message.reply_text(ERROR_VALUE_MSG)
        return ConversationHandler.END

    current_date = f'{datetime.datetime.now():%Y.%m.%d}'

    timestamp = str(datetime.datetime.utcnow().timestamp()).replace('.', '')

    context.user_data['entry'] = {
        '_id': timestamp,
        'user_id': update.effective_user.id, 'amount': amount,
        'date': current_date
    }

    update.message.reply_text(
        CATEGORY_ASK_MSG, reply_markup=category_keyboard()
    )

    return get_category


def get_category(update, context):
    category = update.message.text

    if category not in CATEGORIES:
        update.message.reply_text(
            ERROR_CATEGORY_MSG, reply_markup=category_keyboard()
        )
        return get_category

    context.user_data['entry'].update({'category': category})

    update.message.reply_text(COMMENT_ASK_MSG, reply_markup=comment_keyboard())

    return get_comment


def get_comment(update, context):
    comment = update.message.text
    if len(comment) > MAX_COMMENT_LEN:
        update.message.reply_text(
            ERROR_COMMENT_MSG, reply_markup=cancel_keyboard()
        )
        return get_comment

    if comment == NO_COMMENT_CAPTION:
        context.user_data['entry'].update({'comment': ''})
    else:
        context.user_data['entry'].update({'comment': comment})

    transaction_id = collection.insert_one(context.user_data['entry'])

    update.message.reply_text(
        SUCCESS_MESSAGE, reply_markup=telegram.ReplyKeyboardRemove()
    )

    context.user_data.pop('entry', None)

    export_to_google()

    return ConversationHandler.END


def operation_cancel(update, context):
    context.user_data.pop('entry', None)
    update.message.reply_text(
        CANCEL_MESSAGE, reply_markup=telegram.ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def get_last_30(update, context):
    data_array = get_some_db_data()

    output_data = {}
    for elem in CATEGORIES:
        output_data[elem] = 0
    for entry in data_array:
        time_diff = (
            datetime.datetime.today()
            - datetime.datetime.strptime(entry.get('date'), '%Y.%m.%d')
        )
        try:
            days_diff = int(str(time_diff).split()[0])
        except ValueError:
            days_diff = 0
        if days_diff < 30:
            output_data[entry.get('category')] += float(entry.get('amount'))

    message = compile_message(output_data, REPORT_30_DAYS)
    update.message.reply_text(message)


def get_this_month(update, context):
    data_array = get_some_db_data()

    output_data = {}
    for elem in CATEGORIES:
        output_data[elem] = 0
    for entry in data_array:
        this_month = f'{datetime.datetime.now():%Y.%m}'
        entry_month = (
            entry.get('date').split('.')[0]
            + '.'
            + entry.get('date').split('.')[1]
        )
        if this_month == entry_month:
            output_data[entry.get('category')] += float(entry.get('amount'))

    message = compile_message(output_data, REPORT_THIS_MONTH)
    update.message.reply_text(message)


def compile_csv():
    data_array = get_full_db_data()

    csv_columns = ['_id', 'user_id', 'amount', 'date', 'category', 'comment']
    csv_file = "/tmp/report.csv"
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in data_array:
            writer.writerow(data)


def export_to_csv(update, context):
    compile_csv()

    update.message.reply_document(open('/tmp/report.csv', 'rb'))
    os.remove('/tmp/report.csv')


def export_to_google():
    if not os.path.exists('/bot/client_secret.json'):
        return
    credentials = SAC.from_json_keyfile_name('/bot/client_secret.json', SCOPE)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(GOOGLE_SPREADSHEET)

    compile_csv()

    with open('/tmp/report.csv', 'rb') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)

    os.remove('/tmp/report.csv')
    return


def get_full_db_data():
    raw_data = collection.find()
    data_array = []

    for elem in raw_data:
        data_array.append(elem)

    return data_array


def get_some_db_data():
    raw_data = collection.find({}, {
        '_id': 0, 'user_id': 0, 'comment': 0,
    })

    data_array = []
    for elem in raw_data:
        data_array.append(elem)

    return data_array


client = pymongo.MongoClient(
    f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_ADDR}:{MONGO_PORT}'
)
db = client['main']
collection = db['spendings']

SCOPE = (
        [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
    )
