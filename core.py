from typing import Final
from uuid import uuid4
from html import escape
from telegram import Update, InlineQueryResultPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, InlineQueryHandler
from telegram.constants import ParseMode

import requests

TOKEN:Final = '7761058642:AAHzg5MoAQiGzVHyYa55rffHP1Cmv52G4u4'
BOT_USERNAME: Final = '@pol2lubot'

async def start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=fact)

async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=fact)


async def custom_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=update.effective_message.sticker,
        reply_to_message_id=update.effective_message.id,
    )

async def fact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=fact)

def delete_facts_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(name)
    if not jobs:
        return False
    for job in jobs:
        job.schedule_removal()
    return True
async def facts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        a = int(context.args[0])
        if a < 10:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="please enter a number greater than 10")
            return
        job_name = str(update.effective_user.id)
        job_exists = delete_facts_job_if_exists(job_name, context)
        if job_exists:
            context.job_queue.run_repeating(
                job_facts_handler,
                interval=a,
                chat_id=update.effective_chat.id,
                name=job_name
            )
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="your previous job were delete and you will receive a fact every {} seconds".format(
                                               a))
        else:
            context.job_queue.run_repeating(
                job_facts_handler,
                interval=a,
                chat_id=update.effective_chat.id,
                name=job_name
            )
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="you will receive a fact every {} seconds".format(
                                               a))
    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="please enter a number greater than 10 not anything else")

async def unset_facts_job_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(str(update.effective_user.id))
    for job in jobs:
        job.schedule_removal()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="you will no more receive facts")

async def job_facts_handler(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=job.chat_id, text=fact)

async def unset_handler(update: Update,context:ContextTypes.DEFAULT_TYPE):
    job = context.job_queue.get_jobs_by_name(str(update.effective_chat.id))   
    for n in jobs:
        n.schedule_removal()
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

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        n, m = map(float, context.args)
        result = n + m
        await update.message.reply_text(f"{n} + {m} = {result}")
    except (ValueError, IndexError):
        await update.message.reply_text("Usage: /add <n> <m>\nExample: /add 2 3")

# Command to handle multiplication
async def mult_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        n, m = map(float, context.args)
        result = n * m
        await update.message.reply_text(f"{n} * {m} = {result}")
    except (ValueError, IndexError):
        await update.message.reply_text("Usage: /mult <n> <m>\nExample: /mult 2 3")

# Command to handle arbitrary calculations
async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        expression = ' '.join(context.args)
        result = eval(expression, {"__builtins__": {}})  # Restrict built-in functions for safety
        await update.message.reply_text(f"{expression} = {result}")
    except Exception:
        await update.message.reply_text("Invalid expression. Usage: /calc <expression>\nExample: /calc 1 + 3 * 2")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    data = requests.get("https://thronesapi.com/api/v2/Characters")
    data = data.json()
    characters = {}
    for character in data:
        characters[character["fullName"]] = character["imageUrl"]
    if not query:
        results = []

        for name, url in characters.items():
            newItem = InlineQueryResultPhoto(
                id=str(uuid4()),
                photo_url=url,
                thumbnail_url=url,
                caption=name
            )
            results.append(newItem)
    else:
        results = []
        for name, url in characters.items():
            if query in name:
                newItem = InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=url,
                    thumbnail_url=url,
                    caption=name
                )
                results.append(newItem)
    await update.inline_query.answer(results,auto_pagination=True)


if __name__ == '__main__':
    print('Starting bot....')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    app.add_handler(CommandHandler('fact', fact_handler))
    app.add_handler(CommandHandler("facts", facts_handler))
    app.add_handler(CommandHandler("unset", unset_facts_job_handler))
    app.add_handler(CommandHandler("add", add_command))
    app.add_handler(CommandHandler("mult", mult_command))
    app.add_handler(CommandHandler("calc", calc_command))
    app.add_handler(InlineQueryHandler(inline_query))

    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_error_handler(error)

    print('Polling')
    app.run_polling(poll_interval=3)