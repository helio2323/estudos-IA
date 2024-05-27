FROM python:3.12.3

RUN pip install --upgrade pip

WORKDIR /ESTUDOS-IA

ADD . /ESTUDOS-IA

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
