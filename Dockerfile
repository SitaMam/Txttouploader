FROM python:3.10.8-slim-buster

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pyrogram
RUN pip3 install --upgrade pip
RUN python3 -m pip install "pymongo[srv]"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py
