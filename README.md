# тестовый проект по созданию веб-приложения с поддерживающего реферальную систему
used:
- ubuntu 22.04
- python 3.10.12
- postgreSQL 14.11
- django 5.0.6

## описание процесса и настройки
- django
- postgresql
- тесты

### django
- pip install django
- django-admin startproject project_name .
- python manage.py startapp app_name
#### settings.py
- добавить созданное приложение в installed_apps
- настройки бд:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

### postrgesql
- sudo apt install postgresql
- для запуска тестов нужно выдать полномочия на создание тестовой бд.
```sh
$ sudo -i -u postgres
$ psql
```
```psql
# ALTER USER your_username CREATEDB;
```

###  тесты
- create_user
- test_can_get_referrer_by_ref_code
- test_create_referral_obj
- test_get_user_by_id
- test_can_create_2_referral_obj
- test_cant_craete_referral_obj_to_same_referral
- test_user_is_referrer
- test_user_is_referral
- test_can_get_ref_code_by_user
- test_can_create_user_with_ref_code
- test_can_get_referrals_by_user
- test_get_money_is_work
- test_can_buy_item
- test_cant_buy_item
- test_can_track_referral_purchases
- test_can_give_bonus_for_referrer