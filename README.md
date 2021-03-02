# Sunrise Test Job


Функционал:

Templates
1. Регистрация через Email
2. Авторизация / Авторизация через Google
3. Изменение профиля без перезагрузки страницы через fetch
4. Добавление карточек
5. Категории товаров 3 уровня вложения
6. Подключена СУБД PostgreSQL
7. Локализация на 2 языках (Также есть modeltranslation в админке)
9. Фильтрация по цене
8. Поиск по всем товарам

API
1. Регистрация через Email
2. Авторизация через JWT token
3. Изменение профиля
\
\
\
\
Запуск

1) Создайте виртуальное окружение (venv/pipenv) 

2) Активируйте его и скачайте всё из requirments.txt

pip install -r requirments.txt

3. Файл 'secret_example.py' переименуйте в 'secret.py', и заполните все поля.

   
4. Проведите все миграции

python manage.py makemigrations \
python manage.py migrate

5. Проведите локализацию

django-admin compilemessages

6. Запустите сервер


\
\
\
\
Ссылки и примеры Json:

\
Регистрация
http://localhost:8000/'api/v1/register/


\
Метод = POST


\
{

"email" : example@example.com,

"passwords": example_password,

"re_password": example_password

}

\
\
\
Авторизация:\
Авторизация через JWT token

http://localhost:8000/api/v1/login/

\
Метод = POST

\
{

"email" : example@example.com,

"passwords": example_password

}

\
access - для авторизации

refresh - для обновления access токена

\
\
Обновление токена\
http://localhost:8000/api/v1/token-refresh/

{
'refresh': refresh_token
}
\
\
\
Изменение профиля\
http://localhost:8000/api/v1/edit/

Метод = PATCH

\
\
BODY:

{

"first_name": new_first_name,

"last_name": new_last_name

}



HEADER (Надо вставить acces токен):

{ "Authorization": JWT (access token) }