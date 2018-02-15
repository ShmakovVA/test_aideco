# test_aideco
Тестовое задание:

Сделать простой веб-сайт для отображения табло рейсов в аэропорту

1. У рейса есть номер, город вылета/прилета, тип самолета, время, фактическое время, статус (вылетел, приземлился, идет посадка, задержан до и т.п.).
2. Возможность получать, добавлять, редактировать, удалять рейсы.
3. Возможность сделать выборку по городу, статусу.
4. Должно быть табло прилета, вылета и интерфейс администратора для управления.
5. Должен быть счетчик рейсов.
6. Должна быть подробная документация о том, как развернуть проект.
7. Проект должен быть готов к тому, чтобы вывесить его на внешнем домене.
8. Оформить все в git-репозитории (включая документацию по API)

Будет оцениваться именно качество готового решения.


# БД
По умолчанию проект сконфигурирован на использование sqlite3.
Для использования другой БД (например, MySQL) необходимо дополнительно:
* Установить модуль mysqlclient==1.3.6
* Заменить в файле settings.py DATABASES на:
```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
```    
и, заполнив конфигурационные параметры, приступить к миграции.
 
Можно заполнить БД тестовыми данными через главное меню.

# API
Доступно выполнение запроса к БД извне посредствам выполнения GET запроса с параметрами фильтрации:
(Если фильтры не пустые, то производится фильтрация по вхождению подстроки)

* arr_or_dep - 'arr', 'dep' (прибытия или отправления соответственно)
* status - статус
* city - направление
* flight - рейс

Нужно установить Content-Type в значение application/json

# Панель администратора

Используется встроенная админ панель Django.

# Деплой

Затягиваем проект, обеспечиваем окружение
--
* apt-get install python3
* apt-get install python3-pip
* apt-get install git
* cd /var
* git clone https://github.com/ShmakovVA/test_aideco
* cd /test_aideco
* pip3 install -r requirements.txt

Создаем в корне файл local_settings.py с содержимым:
--
```
    DEBUG = False
    SECRET_KEY = '$n-rn1*khir^n60le#x508w!6nb3fv(=8-watz8je3+prs)sgu'
```

БД (миграции, суперпользователь)
--

* python3 manage.py makemigrations airport
* python3 manage.py migrate airport
* python3 manage.py migrate
* python3 manage.py createsuperuser --username worker --email worker@example.me
* python3 manage.py collectstatic

Ставим и настраиваем апач на раздачу статики (критично только для стилей <zerb foundation>)
--
* apt-get install apache2 libapache2-mod-wsgi-py3
>P.S.: Нужно собрать конфиг с пробросом /static/ /var/test_aideco/static 

Ставим uwsgi и стартуем сервер
--
* pip3 install uwsgi
* uwsgi --http :8000 --wsgi-file django.wsgi


