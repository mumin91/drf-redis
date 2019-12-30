FROM python:3.8.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /drf_redis
WORKDIR /drf_redis
COPY Pip* /drf_redis/
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy --ignore-pipfile
COPY . /drf_redis/