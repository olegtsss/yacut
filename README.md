# Cсылка на развернутый проект

https://yacut.git.olegtsss.ru

# Описание проекта YaCut:

Сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

Ключевые возможности:
- генерация коротких ссылок и связь их с исходными длинными ссылками;
- переадресация на исходный адрес при обращении к коротким ссылкам.

### Используемые технологии:

Python 3.7, Flask 2.0.

### Как запустить проект:
Клонировать репозиторий, перейти в него в командной строке:

```
git clone https://github.com/olegtsss/yacut.git
cd yacut
python -m venv venv
. venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
flask db upgrade
flask run
```

### Пользовательский интерфейс:
одна страница с формой, состоящей из двух полей:
- обязательного для длинной исходной ссылки;
- необязательного для пользовательского варианта короткой ссылки;
- если пользователь не заполнит поле со своим вариантом короткой ссылки, то сервис сгенерирует её автоматически. 


### Формат для ссылки:
по умолчанию — шесть случайных символов:
- большие латинские буквы;
- маленькие латинские буквы;
- цифры в диапазоне от 0 до 9.
Пользовательский вариант короткой ссылки не должен превышать 16 символов.

### API:
настроены эндпоинты:

```
/api/id/ (POST): запрос на создание новой короткой ссылки;
/api/id/{short_id}/ (GET): запрос на получение оригинальной ссылки по указанному короткому идентификатору.
```

## Примеры запросов:
Запрос

```
POST http://127.0.0.1:5000/api/id/
Content-Type: application/json

{
   "url": "https://yandex.ru",
   "custom_id": "ya"
}
```

Ответ

```
{
  "short_link": "http://127.0.0.1:5000/ya",
  "url": "https://yandex.ru"
}
```

Запрос

```
GET http://127.0.0.1:5000/api/id/ya/
```

Ответ

```
{
  "url": "https://yandex.ru"
}
```

## Шаблон наполнения env-файла:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=AAAAAAAAAAAAAAAAAAAAAAAA
```

### Разработчик:
[olegtsss](https://github.com/olegtsss)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=whte)
