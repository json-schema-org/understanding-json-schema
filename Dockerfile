FROM python:3.6-alpine

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /doc

CMD ["sphinx-build", "-b", "html", "source", "build"]
