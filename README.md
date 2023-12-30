# README.md

## Описание
Этот проект представляет собой бота для Telegram, который предоставляет информацию о криптовалютах. Бот может отображать самую дешёвую и самую дорогую криптовалюту, а также предоставлять информацию о конкретной криптовалюте. Бот также сохраняет историю запросов пользователя.

## Установка
1. Клонируйте репозиторий на свой локальный компьютер с помощью команды `git clone`.
2. Перейдите в каталог проекта с помощью команды `cd`.
3. Установите все необходимые зависимости, указанные в файле `requirements.txt`, с помощью команды `pip install -r requirements.txt`.

## Запуск
1. Создайте файл `config.py` и добавьте в него свой токен бота:
    ```python
    BOT_TOKEN = 'your_bot_token_here'
    ```
2. Запустите бота, используя команду `python main.py`.

Пожалуйста, обратите внимание, что для работы этого бота вам потребуется активное подключение к Интернету. Бот будет работать, пока его процесс активен в вашем терминале.

## Команды
Бот поддерживает следующие команды:
- `/hello-world`: Бот ответит сообщением "Hello, World!".
- `Привет`: Бот ответит сообщением "Привет!".
- `/low`: Бот покажет самую дешёвую криптовалюту и её цену в рублях. Также будет показан полный список криптовалют.
- `/high`: Бот покажет самую дорогую криптовалюту и её цену в рублях. Также будет показан полный список криптовалют.
- `/custom`: Бот покажет полный список криптовалют.
- `/history`: Бот покажет последние 10 команд, которые вы отправили боту.
- Команда обратного вызова: Если вы выберете криптовалюту из списка, бот покажет её текущую цену в рублях.

Пожалуйста, обратите внимание, что все команды должны начинаться со знака `/`, за исключением команды `Привет` и команд обратного вызова. Команды обратного вызова инициируются при выборе криптовалюты из списка.