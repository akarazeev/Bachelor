Создать виртуальное окружение через `virtualenv` и установить необходимые python-зависимости:
  ```
    pip install -r requirements.txt
  ```

#### Установка и создание базы данных
1. Установить PostreSQL, качать тут https://www.postgresql.org/download/linux/ubuntu/
2. Создать в установленном приложении сервер с любым именем и дефолтными настройками(путь, прот 5432, 11 версия)
3. Запустить скрипт ```create_db.sh```

#### Запуск flask приложения
  ```
    python run.py
  ```
После чего приложение запустится на 5000 порту
