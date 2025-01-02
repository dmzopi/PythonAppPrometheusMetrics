git clone https://github.com/dmzopi/PythonAppPrometheusMetrics.git
sudo docker build . -t promapp
sudo docker run -d --rm -p 8000:8000 -p 8001:8001 --name promapp promapp
or
docker compose up -d
while true; do curl 127.0.0.1:8000; sleep 0.1; done