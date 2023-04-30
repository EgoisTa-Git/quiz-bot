import re

from environs import Env
import redis
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id


def echo(event, api, keyboard):
    api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def handle_new_question_request(event, api, keyboard):
    question = questions_db.randomkey()
    vk_users_db.set(event.user_id, question)
    api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def handle_my_score_request(event, api, keyboard):
    api.messages.send(
        user_id=event.user_id,
        message='Эта функция будет доступна позднее. Надеемся на Ваше понимание.',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def handle_give_up_request(event, api, keyboard):
    question = vk_users_db.get(event.user_id)
    answer = questions_db.get(question)
    api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )
    api.messages.send(
        user_id=event.user_id,
        message='Не расстраивайся! В следующий раз обязательно получится!',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )
    handle_new_question_request(event, api, keyboard)


def handle_solution_attempt(event, api, keyboard):
    question = vk_users_db.get(event.user_id)
    answer = questions_db.get(question).lstrip('Ответ: ').rstrip('.').strip()
    answer = answer.replace('"', '')
    correct_answer = re.sub(r'[\(\[].*?[\)\]]', '', answer).lower()
    if correct_answer == '':
        correct_answer = answer.strip('[]()').lower()
    if event.text.strip('"[]()').lower() == correct_answer:
        api.messages.send(
            user_id=event.user_id,
            message='Правильно! Поздравляю!',
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
        )
        handle_new_question_request(event, api, keyboard)
    else:
        api.messages.send(
            user_id=event.user_id,
            message='Неправильно… Попробуешь ещё раз?',
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
        )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    redis_db_pass = env('REDIS_DB_PASS')
    questions_db = redis.Redis(
        host='localhost',
        port=6379,
        password=redis_db_pass,
        decode_responses=True,
        db=0,
    )
    vk_users_db = redis.Redis(
        host='localhost',
        port=6379,
        password=redis_db_pass,
        decode_responses=True,
        db=2,
    )

    vk_bot_apikey = env('VK_BOT_APIKEY')
    vk_session = vk.VkApi(token=vk_bot_apikey)
    vk_api = vk_session.get_api()
    long_poll = VkLongPoll(vk_session)
    vk_keyboard = VkKeyboard(one_time=True)
    vk_keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    vk_keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    vk_keyboard.add_line()
    vk_keyboard.add_button('Мой счет')
    for vk_event in long_poll.listen():
        if vk_event.type == VkEventType.MESSAGE_NEW and vk_event.to_me:
            if vk_event.text == 'Сдаться':
                handle_give_up_request(vk_event, vk_api, vk_keyboard)
            elif vk_event.text == 'Новый вопрос':
                handle_new_question_request(vk_event, vk_api, vk_keyboard)
            elif vk_event.text == 'Мой счет':
                handle_my_score_request(vk_event, vk_api, vk_keyboard)
            else:
                handle_solution_attempt(vk_event, vk_api, vk_keyboard)
