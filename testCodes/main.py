import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import telegram

TOKEN = "5727339733:AAGrTLcd74yedbEid42fCBacLiRk4FZz0Dk"
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# logger = logging.getLogger(__name__)
#
#
# def echo(update: Update, context: CallbackContext) -> None:
#     message = update.message.text
#     if message == "안녕":
#         reply = "너도 안녕!"
#     elif message == "바보":
#         reply = "반사!"
#     elif message == "날씨":
#         reply = "좋음!"
#     update.message.reply_text(reply)
#
#
# updater = Updater(TOKEN)
# dispatcher = updater.dispatcher
# dispatcher.add_handler(MessageHandler(Filters.text, echo))
# updater.start_polling()
# updater.idle()

bot = telegram.Bot(token=TOKEN)

updates = bot.getUpdates()

for i in updates:
    print(i)
    print('\n')

bot.sendMessage(chat_id='-1001789099529', text="일어나새꺄")