# Title:     Search ENgine
# Filename : Dockerfile
# Author   : Adeola Ajala

# Pull baseImage
FROM python:latest

# Create work directory
WORKDIR /home/app

# Install dependencies
COPY requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt
