FROM python:3.11.0-slim-bullseye AS env

RUN python3 -m venv /opt/env
RUN . /opt/env/bin/activate

COPY requirements.txt requirements.txt
RUN /opt/env/bin/pip install -r requirements.txt


FROM python:3.11.0-slim-bullseye AS prod

RUN adduser --home /app --shell /bin/sh --uid 1000 --disabled-password appuser
USER appuser

WORKDIR /app

COPY --from=env /opt/env /app/env
COPY . .

CMD ["/app/env/bin/python", "main.py"]
