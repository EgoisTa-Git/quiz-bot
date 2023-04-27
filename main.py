from pathlib import Path


def normalize_text(phrase):
    return phrase.lstrip().replace('\n', ' ')


def get_file_paths(path_to_questions):
    paths = []
    for item in Path(path_to_questions).iterdir():
        paths.append(item)
    return paths


def get_pairs(lines):
    questions = []
    answers = []
    for line in lines:
        if 'Вопрос' in line:
            questions.append(normalize_text(line))
        elif 'Ответ' in line:
            answers.append(normalize_text(line))
    return dict(zip(questions, answers))


if __name__ == '__main__':
    file_paths = get_file_paths('questions')
    pairs = {}
    for path in file_paths:
        with open(path, encoding='KOI8-R') as file:
            text = file.read().split('\n\n')
        pairs.update(get_pairs(text))
