FROM python:3.10.9 as base

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install python3-dev gcc musl-dev

RUN useradd -rms /bin/bash transactions_admin && chmod 777 /opt /run

WORKDIR /transactions_project

RUN mkdir /transactions_project/static && mkdir /transactions_project/media && chown -R transactions_admin:transactions_admin /transactions_project && chmod 777 /transactions_project

COPY --chown=transactions_admin:transactions_admin . .

RUN pip install -r requirements.txt

USER transactions_admin

RUN chmod +x wait-for-postgres.sh

CMD ["./wait-for-postgres.sh"]

CMD ["python3 manage.py runserver 0.0.0.0:8000"]