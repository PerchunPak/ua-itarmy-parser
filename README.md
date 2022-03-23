# [@itarmyofukraine2022](https://t.me/itarmyofukraine2022) [виклали](https://t.me/itarmyofukraine2022/229) свій додаток для автоматизованних атак. [Дивіться інструкцію.](https://telegra.ph/Death-by-1000-needles-03-17)

Проект архівовано, рекомендую користуватися додатком з офіційного джерела.

# [@itarmyofukraine2022](https://t.me/itarmyofukraine2022) [post](https://t.me/itarmyofukraine2022/229) their own DDOS utility for performing automated attacks. [See guide.](https://telegra.ph/Death-by-1000-needles-03-18)

Project archived, I recommend using utility from official source.

# ua-itarmy-parser

[![Build Status](https://github.com/PerchunPak/ua-itarmy-parser/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/PerchunPak/ua-itarmy-parser/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/PerchunPak/ua-itarmy-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/PerchunPak/ua-itarmy-parser)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Парсить офіційний телеграм канал @itarmyofukraine2022 и запускає DDOS на сайти.

Цей скрипт не здійснює DDOS чи DOS атаки, тільки запускає їх за наказом офіційного телеграмм каналу.

Якщо розписати роботу цієї програми за кроками, то буде ось так:

1. Нас запускають і ми чекаємо повідомлення з телеграм каналу.

2. Повідомлення приходить.

3. Ми вилучаємо IPv4 і посилання з повідомлення.

4. Відправляємо всі цілі в вашу програму для DDOS атак, дивіться [налаштування конфігурації](https://github.com/PerchunPak/ua-itarmy-parser#налаштування%20конфігурації).

## Встановлення

```sh-session
git clone ...
cd ua-itarmy-parser
```

Ми використовуємо `poetry` для керування залежностями.
Зверніть увагу, що він автоматично створює та налаштовує віртуальне оточення.

### Спочатку встановимо poetry [рекомендованим шляхом](https://python-poetry.org/docs/master/#installation).

Якщо ви на платформі Linux, використайте команду:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Якщо ви на Windows, відкрийте PowerShell від імені адміністратора та використовуйте:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Увага: На момент написання тексту (03.3.2022) існує помилка, яка викликає попередження при використанні будь-якої команди. Якщо ви з таким зіткнулися, можете встановити poetry іншим шляхом:

```bash
pip install poetry
```

Але враховуйте, що це не рекомендований шлях, ви, можливо, не зможете використовувати деякі функції (наприклад `poetry self update`).

### Встановимо всі залежності у віртуальне оточення:

```bash
poetry install
```

Налаштуйте конфіг у файлі `config.ini`. [Детальніше тут](https://github.com/PerchunPak/ua-itarmy-parser#налаштування%20конфігурації).

Запустіть скрипт:
```session
python run.py
```

## Налаштування конфігурації

### [app]

Секція для авторизаційних даних Telegram. Обліковий запис бота не може дивитися повідомлення навіть публічного каналу. 
Також візьміть до уваги що Telethon (бібліотека для підключення до Telegram) кешує данні для входу.

`id` і `hash`: Ці данні потрібні для авторизації в телеграмі. Є 4 простих кроки для їх отримання:

1. [Увійдіть в ваш телеграм обліковий запис тут](https://my.telegram.org/) з допомогою номера телефона.

2. Натисніть `API development tools`.

3. З'явиться вікно `Create application`. Заповніть данні вашого додатку, немає ніякої необхідності вводити будь-який URL,
тільки два перших поля (`App title` і `API development tools`), які можуть бути зміненими потім.

4. Натисніть `Create application` в кінці. Пам'ятайте що ваш **хеш API секретний** і телеграм не дозволить його скинути. 
Не публікуйте його ніде!

[Детальніше тут](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in).

`phone`: Ваш номер телефону до якого прив'язаний телеграмм обліковий запис. Не пугайтеся коли воно попросить код,
це авторизація в ваш обліковий запис. Хочу також зауважити що саме у ваш, не в бот-аккаунт.

### [ddos.together]

`links_and_ipv4_together`: Записувати IPv4 і посилання в один файл? Також використовує одну команду для запуску. 
Можливі значення: `true` (так) або `false` (ні).

`file_to_write`: Файл куди записуються всі цілі. Рекомендується записувати абсолютний шлях. Кожна ціль 
записується з нової строки. На кожне повідомлення, файл перезаписується. Працює тільки якщо `links_and_ipv4_together`
ввімкнена.

`command`: Команда для запуска атаки. Не має ніяких можливих змінних. Також усвідомте, що ви не можете 
зупинити цю команду не зупинивши скрипт, встановлюйте час протягом якого потрібно виконувати DDOS. Працює тільки якщо 
`links_and_ipv4_together` ввімкнена.

### [ddos.links]

`enable`: Вмикає слухання посилань та всі інші функції цієї секції. Якщо встановлено `false`, посилання будуть 
ігноруватися. Можливі значення: `true` (так) або `false` (ні).

`file_to_write`: Файл куди записувати нові сайти для DDOS атаки. Рекомендується записувати абсолютний шлях.
Кожен сайт записується з нової строки. На кожне повідомлення, файл перезаписується. Не працює якщо 
`links_and_ipv4_together` ввімкнена.

`command`: Команда для запуска атаки. Не має ніяких можливих змінних. Також усвідомте, що ви не можете зупинити цю
команду не зупинивши скрипт, встановлюйте час протягом якого потрібно виконувати DDOS. Не працює якщо 
`links_and_ipv4_together` ввімкнена.

`remove_http_before_pass_to_tool`: Видаляє `http://` і `https://` з посилання перед тим як записати його в файл.
Можливі значення: `true` (так) або `false` (ні).

### [ddos.ipv4]

`enable`: Вмикає опрацювання IPv4. Якщо встановлено `false`, IPv4 будуть ігноруватися. Можливі значення: `true` (так) 
або `false` (ні).

`file_to_write`: Файл куди записувати нові адреси для DDOS атаки. Рекомендується записувати абсолютний шлях.
Кожна адреса записується з нової строки. На кожне повідомлення, файл перезаписується. Не працює якщо 
`links_and_ipv4_together` ввімкнена.

`command`: Команда для запуска атаки. Не має ніяких можливих змінних. Також усвідомте, що ви не можете зупинити цю
команду не зупинивши скрипт, встановлюйте час протягом якого потрібно виконувати DDOS. Не працює якщо 
`links_and_ipv4_together` ввімкнена.

### ENV змінні

Змінні з конфігу в форматі `ITARMY_<SECTION>_<PARAMETER>`, тобто префікс `ITARMY_`, потім ім'я секції (те що в []) і ім'я
опції великими літерами. Також візьміть до уваги що при зупинці скрипту, в конфіг будуть записані значення з ENV 
змінних. Вони перезапишуть те що було в конфігу до того.

`ITARMY_CONFIG_PATH`: Шлях до файла з конфігом, відносно папки з `README.md` файлом.

`ITARMY_LOG_LEVEL`: Допустимі значення `debug, info, warning, error, critical`, рекомендуємо `info`.

`ITARMY_LOG_PATH`: Путь до папки з логами, відносно папки з `README.md` файлом.

### Післямова

Ви можете змінювати як завгодно проєкт під свої бажання, але поширювати можете тільки як open-source проєкт,
дивіться [нашу ліцензію](https://github.com/PerchunPak/ua-itarmy-parser/blob/master/LICENSE).

## TODO

- [ ] Придумати TODO. Ні, реально. Все що я придумав, вже виконав.

## Дякуємо

Цей проєкт був згенерований з допомогою [`autodonate-plugin-template`](https://github.com/fire-squad/autodonate-plugin-template).
Поточна версія прикладу: [6c3ec0d643f76745f533ed2eaf6c364adb51b393](https://github.com/fire-squad/autodonate-plugin-template/tree/6c3ec0d643f76745f533ed2eaf6c364adb51b393).
Дивіться що [оновилося](https://github.com/fire-squad/autodonate-plugin-template/compare/6c3ec0d643f76745f533ed2eaf6c364adb51b393...master) з того часу.
