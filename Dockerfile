FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

ENV USER "xxx"
ENV PASSWORD "xxx"
ENV HOST "11.8.33.11"
ENV PORT "1234"
ENV DATABASE "xxx"

COPY flask_service.py .
COPY postgre_backend.py .
COPY learnsupport_service.py .

EXPOSE 5000

CMD ["python3", "flask_service.py"]