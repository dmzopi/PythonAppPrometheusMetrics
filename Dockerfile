FROM python:3.9

RUN mkdir -p /var/www/
WORKDIR /var/www/

COPY ./server.py /var/www/
COPY ./requirements.txt /var/www/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
EXPOSE 8001
CMD ["python","server.py"]
