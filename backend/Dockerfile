FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install .
RUN pip install ipython

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

HEALTHCHECK CMD curl -o /dev/null http://localhost:5000/openapi/openapi.json
