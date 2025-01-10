from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN:Final = '7761058642:AAHzg5MoAQiGzVHyYa55rffHP1Cmv52G4u4'
BOT_USERNAME: Final = '@pol2lubot'

async def start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello Thanks for chatting with me! I am banana')

async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('i am a banana! please type somthing so i can respond!')

async def custom_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is command !')


def handle_response(text:str )->str:
    processed:str=text.lower()
    if 'hello' in processed:
        return 'Hey there'
    if 'how are you' in processed:
        return 'I am good!'
    if 'i love python' in processed:
        return 'Remember to subscribe!'
    return 'I do not understand what you wrote...'

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text:str = update.message.text
    print(f'User({update.message.chat.id} in {message_type}:"{text}")')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_txt : str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_txt)
        else:
            return
    else:
        response:str = handle_response(text)
    
    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update: Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot....')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_error_handler(error)

    print('Polling')
    app.run_polling(poll_interval=3)