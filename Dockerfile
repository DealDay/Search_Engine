# Title    : Search Engine
# Filename : Dockerfile
# Author   : Adeola Ajala

# Pull baseImage
FROM ubuntu:latest
RUN apt-get update && apt-get clean && \
    apt-get install -y gnupg curl python3 python3-pip &&\
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
    gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
    --dearmor && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
    https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
    tee /etc/apt/sources.list.d/mongodb-org-7.0.list && apt-get update && apt-get install -y mongodb-org && \
    rm /usr/lib/python3.12/EXTERNALLY-MANAGED

# Create work directory
WORKDIR /home

# Install dependencies
COPY requirements.txt /home/requirements.txt
RUN pip3 install -r requirements.txt