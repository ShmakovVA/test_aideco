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


# Common comments
1. Implemented as a web-service with a web-client and api.
2. Selected simple shorting link method (not specified in the task)
3. Unit testing was not applied (there is not in the task and too simple task).
4. Deploy work was not performed (not specified in the task).
5. A pre-installed MySQL Server 5.5 database was used: 
	to migrate models and working with db, you need to have a db available according with settings.py:

# Test data for db
You can fill db by pressing button "Fill with test data" on main menu of web-client application or  
by running script "fill_db.py" from project folder.

# For api using
