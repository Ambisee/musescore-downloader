FROM python:3.11-alpine

WORKDIR /
COPY . .

RUN apk update
RUN apk upgrade
RUN apk add git
RUN apk add chromium

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["pytest", "tests/"]