from handlers import (
    add_start, get_category, get_comment, operation_cancel,
    get_last_30, get_this_month, export_to_csv, export_to_google
)
from settings import CANCEL_CAPTION, TELEGRAM_TOKEN

import telegram

from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters, ConversationHandler
)


def main():
    bot = telegram.Bot(TELEGRAM_TOKEN)
    
    finance_bot = Updater(bot=bot, use_context=True)
    
    bot_dispatcher = finance_bot.dispatcher

    bot_dispatcher.add_handler(CommandHandler('get_last_30', get_last_30))
    bot_dispatcher.add_handler(CommandHandler('get_this_month', get_this_month))
    bot_dispatcher.add_handler(CommandHandler('export_to_csv', export_to_csv))
    
    bot_dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(
            Filters.regex(r'^[0-9.,]+$'), add_start
        )],
        states={
            get_category: [
                MessageHandler(
                    Filters.text & ~Filters.regex(CANCEL_CAPTION), get_category
                )],
            get_comment: [
                MessageHandler(
                    Filters.text & ~Filters.regex(CANCEL_CAPTION), get_comment
                )],
            },
        fallbacks=[
            MessageHandler(
                Filters.regex(CANCEL_CAPTION), operation_cancel
            )]
    ))
    # ^[a-zA-Z0-9\-\_\.]+$
    finance_bot.start_polling()

    finance_bot.idle()


if __name__ == "__main__":
    main()
