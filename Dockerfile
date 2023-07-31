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

ENV FLASK_APP=src/main.py
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# for running the container: docker run -d -p 5000:5000 --device /dev/video0 neuroprosthetics_mvp
