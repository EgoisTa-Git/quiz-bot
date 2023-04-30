import re

from environs import Env
import redis
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)

NEW_QUESTION, ANSWER = range(2)


def start(update: Update, context: CallbackContext):
    quiz_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет', ]]
    reply_markup = ReplyKeyboardMarkup(quiz_keyboard)
    update.message.reply_text(
        text='Привет! Я бот для викторин!',
        reply_markup=reply_markup
    )
    return NEW_QUESTION


def handle_new_question_request(update: Update, context: CallbackContext):
    question = questions_db.randomkey()
    update.message.reply_text(question, reply_markup=ReplyKeyboardRemove())
    users_db.set(update.message.chat_id, question)
    return ANSWER


def handle_solution_attempt(update: Update, context: CallbackContext):
    question = users_db.get(update.message.chat_id)
    answer = questions_db.get(question).lstrip('Ответ: ').rstrip('.').strip()
    answer = answer.replace('"', '')
    correct_answer = re.sub(r'[\(\[].*?[\)\]]', '', answer).lower()
    if correct_answer == '':
        correct_answer = answer.strip('[]()').lower()
    if update.message.text.strip('"[]()').lower() == correct_answer:
        update.message.reply_text('Правильно! Поздравляю!')
        handle_new_question_request(update, context)
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')
        return ANSWER


def handle_give_up_request(update: Update, context: CallbackContext):
    question = users_db.get(update.message.chat_id)
    answer = questions_db.get(question)
    update.message.reply_text(answer)
    update.message.reply_text('Не расстраивайся! В следующий раз обязательно получится!')
    handle_new_question_request(update, context)


def handle_my_score_request(update: Update, context: CallbackContext):
    update.message.reply_text('Эта функция будет доступна позднее. Надеемся на Ваше понимание.')


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        'До новых встреч!',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_bot_api_key = env('TG_BOT_APIKEY')
    redis_db_pass = env('REDIS_DB_PASS')
    questions_db = redis.Redis(
        host='localhost',
        port=6379,
        password=redis_db_pass,
        decode_responses=True,
        db=0,
    )
    users_db = redis.Redis(
        host='localhost',
        port=6379,
        password=redis_db_pass,
        decode_responses=True,
        db=1,
    )

    updater = Updater(tg_bot_api_key)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NEW_QUESTION: [
                MessageHandler(Filters.regex(r'^Новый вопрос'), handle_new_question_request),
                MessageHandler(Filters.regex(r'^Мой счет'), handle_my_score_request),
            ],
            ANSWER: [
                MessageHandler(Filters.regex(r'^Сдаться'), handle_give_up_request),
                MessageHandler(Filters.regex(r'^Мой счет'), handle_my_score_request),
                MessageHandler(Filters.text, handle_solution_attempt),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
