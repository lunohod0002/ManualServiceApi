# ManualServiceApi
Инструкция по запуску приложения
1)	Скачайте Docker Dekstop  с официального сайта и запустите приложение https://www.docker.com/products/docker-desktop/
2)	Склонируйте репозиторий проекта на рабочую машину и перейдите в рабочий каталог:

    git clone https://github.com/lunohod0002/ManualServiceApi.git

    cd ManualServiceApi

3)	Далее создайте файл .env-not-dev, в котором укажите настройки базы данных для приложения, пример:
   <p align="center">
  <img src="https://github.com/user-attachments/assets/f587a089-9332-426b-9169-94a0de8f010d" />
</p>
<p align="center"> Рисунок 1 – Файл .env-not-dev</p>

4)	В корневой директории проекта выполните следующую команду : docker-compose up --build
5)	Теперь для доступа к приложению перейдите по адресу : http://127.0.0.1:8000/docs
6)	Чтобы воспользоваться эндпоинтами приложения введите статический API ключ : 12345678 


