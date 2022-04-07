# Dockerfile, Image, Container
FROM python:3.10

ADD algos/ .
ADD classes/ .
ADD helpers/ .
ADD run_algos.ipynb .
ADD main.py .


# List packages here
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        file        \
        gcc         \
        libwww-perl && \
    apt-get autoremove -y && \
    apt-get clean

# Upgrade pip
RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]