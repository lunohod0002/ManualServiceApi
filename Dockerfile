FROM python:3.12

RUN mkdir /organizations

WORKDIR /organizations

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .


RUN chmod a+x start_fastapi.sh

CMD ["sh", "-c", "gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"]