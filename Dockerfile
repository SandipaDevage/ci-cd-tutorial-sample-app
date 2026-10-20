# The original image (ubuntu:18.04) is end-of-life and its pip3 targets Python 3.6.
# The official Python 3.8 image is smaller and installs the app's dependencies cleanly.
FROM python:3.8-slim

WORKDIR /sample-app

COPY requirements.txt requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-server.txt

COPY . .

ENV FLASK_APP=bootstrap.py \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PORT=8000

EXPOSE 8000

# Create/upgrade the database, seed it, then start the server.
# Hosting platforms such as Render pass the port to listen on in $PORT.
CMD ["/bin/sh", "-c", "flask db upgrade && python seed.py && gunicorn app:app -b 0.0.0.0:${PORT}"]
