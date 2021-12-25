FROM python:3.9.2-slim-buster
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git wget python3-dev ffmpeg python3
COPY . .
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt
# Starting Worker
CMD ["python3","-m","bot"]
