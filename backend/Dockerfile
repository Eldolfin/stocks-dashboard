FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install .
RUN pip install ipython

ENV FLASK_APP=src.app:create_app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

HEALTHCHECK CMD curl -f -o /dev/null http://localhost:5000/openapi/openapi.json
