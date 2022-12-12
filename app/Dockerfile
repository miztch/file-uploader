FROM python:alpine
WORKDIR /app
COPY . /app
RUN apk --update-cache add \
    gcc \
    g++ \
    build-base \
    linux-headers \
    python3-dev \
    pcre-dev
RUN pip install -r requirements.txt