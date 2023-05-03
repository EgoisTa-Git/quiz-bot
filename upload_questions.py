import argparse
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


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Загрузчик для базы данных Redis'
    )
    parser.add_argument(
        '--qa_path',
        type=Path,
        default='questions',
        help='путь к каталогу с txt-файлами вопросов',
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    parsed_arguments = parse_arguments()
    file_paths = get_file_paths(parsed_arguments.qa_path)
    env = Env()
    env.read_env()
    redis_db_pass = env('REDIS_DB_PASS')
    redis_db_host = env('REDIS_DB_HOST', 'localhost')
    redis_db_port = env.int('REDIS_DB_PORT', 6379)
    questions_db = redis.Redis(
        host=redis_db_host,
        port=redis_db_port,
        password=redis_db_pass,
        decode_responses=True,
        db=0,
    )
    for path in file_paths:
        with open(path, encoding='KOI8-R') as file:
            texts = file.read().split('\n\n')
        for question, answer in get_questions_vs_answers_pairs(texts).items():
            questions_db.set(question, answer)
