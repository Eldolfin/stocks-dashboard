FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# TODO: remove --debug before deploying!
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

