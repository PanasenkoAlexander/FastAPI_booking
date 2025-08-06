FROM python:3.13

# создаем рабочую директорию
RUN mkdir /booking

# переход в рабочую директорию
WORKDIR /booking

# копирование и затем установка наших зависимостей
COPY requirements.txt .

RUN pip install -r requirements.txt

# копируем наши данные в контейнер
COPY . .

# запуск баш-файла из папки docker (если используем только DOCKERFILE)
# RUN chmod a+x /booking/docker/*.sh

# запуск приложения (если используем только DOCKERFILE)
# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "unicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]


# далее билдим приложение и создаем его образ: docker build .
# затем запускаем образ с прокидыванием портов: docker run -p 9000:8000 <ID-образа>
# по портам: первый идет который будет использоваться локально, второй указываем для докера