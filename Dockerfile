# Title    : Search Engine
# Filename : Dockerfile
# Author   : Adeola Ajala

# Pull baseImage
FROM python:3.9.6
# FROM ubuntu:latest
# RUN apt-get update && apt-get clean && \
#     apt-get install -y gnupg curl python3 python3-pip systemd &&\
#     curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
#     gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
#     --dearmor && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
#     https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
#     tee /etc/apt/sources.list.d/mongodb-org-7.0.list && apt-get update && apt-get install -y mongodb-org && \
#     rm /usr/lib/python3.12/EXTERNALLY-MANAGED

# Create work directory
WORKDIR /home
EXPOSE 8000
EXPOSE 27017

# Install dependencies
# COPY Backend /home/Backend
COPY . /home
# COPY requirements.txt /home/requirements.txt
RUN pip install -r requirements.txt

# Install additional development dependencies
# RUN pip install --no-cache-dir ipython

WORKDIR /home/Backend/
# CMD [ "uvicorn", "--host", "0.0.0.0", "main:app", "--reload"]
CMD ["uvicorn" "main:app" "--host" "0.0.0.0" "--port" "8000" "--lifespan=on" \
 "--use-colors" "--loop" "uvloop" "--http" "httptools" "--reload"] 