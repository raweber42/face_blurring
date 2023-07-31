FROM python:3.10-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
# set the working directory in the container
WORKDIR /usr/src/app

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .
# COPY datasets ./datasets

ENV FLASK_APP=main.py
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
