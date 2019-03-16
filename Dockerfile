FROM python:3.7-slim
ENV INSTALL_PATH .
WORKDIR $INSTALL_PATH
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python -m database.init_db
CMD gunicorn -b localhost:5000 "app:app"