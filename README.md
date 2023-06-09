# Quiz Bot

Quiz Bot - чат-бот с каверзными вопросами и единственным правильным вариантом ответа.

## Примеры бота
Доступен по ссылке в Телеграм: [Quiz Bot](https://t.me/dvmn_2023_quiz_bot)

![examination_tg.gif](assets/examination_tg.gif)

Доступен по ссылке в Вконтакте: [Quiz Bot](https://vk.com/club219580914)

![examination_vk.gif](assets/examination_vk.gif)

## Запуск
- Рекомендуется использовать виртуальное окружение для запуска проекта
- Для корректной работы Вам необходим Python версии 3.6 и выше
- Настроить базу Redis (инструкция [тут](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04-ru)).
- API-ключ для работы с Telegram-ботом (инструкция [тут](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)).
- API-ключ для работы с VK-ботом (инструкция [тут](https://vk.com/dev/access_token)) с правами управление сообществом и доступ к сообщениям сообщества.
- Скачайте код (`git clone`)
- Установите зависимости командой
```bash
pip install -r requirements.txt
```
- Перед первым запуском необходимо добавить вопросы в базу данных
- Поместите txt-файлы с вопросами в папку `questions` (папка должна лежать рядом с файлом `upload_questions.py`)
- Пример структуры вопроса в файле:
```text
Вопрос 2:
В своем первоначально узком значении это слово произошло от французского
глагола, означающего "бить". Сейчас же оно может означать любое
объединение в систему нескольких однотипных элементов. Назовите это
слово.

Ответ:
Батарея (от battre).

Источник:
СЭС

Автор:
Вадим Карлинский


```

- Запустите скрипт для наполнения базы данных
```bash
python upload_questions.py
```
- Для запуска Telegram-бота необходимо выполнить команду:
```bash
python tg_bot.py
```

- Для запуска VK-бота необходимо выполнить команду:
```bash
python vk_bot.py
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, 
создайте файл `.env` в корневой директории проекта и запишите туда данные в таком 
формате: `ПЕРЕМЕННАЯ="значение"`.

Доступные переменные:

- `VK_BOT_APIKEY` - API-ключ для работы с VK-ботом
- `TG_BOT_APIKEY` - API-ключ для работы с Telegram-ботом
- `REDIS_DB_PASS` - пароль для базы данных Redis
- `REDIS_DB_HOST` - IP-адрес базы данных Redis (по умолчанию `localhost` - для инстанса базы, запущенного локально)
- `REDIS_DB_PORT` - порт для подключения к базе данных

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).