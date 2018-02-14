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


# Тестовые (начальные) данные для БД
Можно заполнить БД тестовыми данными через главное меню.

# API

# Деплой

1. Затягиваем проект, обеспечиваем окружение
sudo apt-get install python3
sudo apt install python3-pip
apt-get install git
cd /var
git clone https://github.com/ShmakovVA/test_aideco
cd /test_aideco
pip3 install -r requirements.txt

1.1. Создаем в корне файл local_settings.py
--
DEBUG = False
SECRET_KEY = '$n-rn1*khir^n60le#x508w!6nb3fv(=8-watz8je3+prs)sgu'
--

2. БД (миграции, суперпользователь)
python3 manage.py makemigrations airport
python3 manage.py migrate airport
python3 manage.py migrate
python3 manage.py createsuperuser --username worker --email worker@example.me
python3 manage.py collectstatic

3. Ставим и настраиваем апач на раздачу статики (критично только для стилей <zerb foundation>)
apt-get install apache2 libapache2-mod-wsgi-py3

4. Ставим uwsgi и стартуем сервер
pip3 install uwsgi
uwsgi --http :8000 --wsgi-file aideco/wsgi.py


