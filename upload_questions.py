from pathlib import Path
import re

from environs import Env
import redis


def normalize_text(phrase):
    return phrase.lstrip().replace('\n', ' ')


def get_file_paths(path_to_questions):
    paths = []
    for item in Path(path_to_questions).iterdir():
        paths.append(item)
    return paths


def get_questions_vs_answers_pairs(lines):
    questions = []
    answers = []
    for line in lines:
        if re.match(r'Вопрос \d+:', line):
            questions.append(normalize_text(line))
        elif 'Ответ:' in line:
            answers.append(normalize_text(line))
    return dict(zip(questions, answers))


if __name__ == '__main__':
    file_paths = get_file_paths('questions')
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
    for path in file_paths:
        with open(path, encoding='KOI8-R') as file:
            texts = file.read().split('\n\n')
        for question, answer in get_questions_vs_answers_pairs(texts).items():
            questions_db.set(question, answer)
