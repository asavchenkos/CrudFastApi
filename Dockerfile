FROM python:latest

WORKDIR /usr/src/fastApiCRUD

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python",  "-m", "app.main" ]

