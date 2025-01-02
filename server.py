import http.server
import random
import time
from datetime import datetime
from prometheus_client import start_http_server, Counter, Gauge, Summary, Histogram

### Counter metric
# Simple counter w/o labels
#REQUEST_COUNT = Counter('app_requests_count', 'total app http request count')
# Counter with labels, will show counter for each endpoint user hits (/, /home ...)
REQUEST_COUNT = Counter('app_requests_count', 'total app http request count',['app_name', 'endpoint'])
### Gauge metric
REQUEST_IN_PROGRESS = Gauge('app_requests_in_progress', 'number of application requests in progress')
REQUEST_LAST_SERVED = Gauge('app_last_served', 'time the application was last served')
### Summary metrics
REQUEST_RESPOND_TIME = Summary('app_response_latency_seconds', 'Response latency in seconds')
### Histogram metrics
REQUEST_RESPOND_TIME_HIST = Histogram('app_response_latency_seconds_hist', 'Response latency in seconds', buckets=[0.1,0.5,1,2,3,4,5,10])

APP_IP = '0.0.0.0'
APP_PORT = 8000
METRICS_PORT = 8001

class HandleRequests(http.server.BaseHTTPRequestHandler):
    @REQUEST_IN_PROGRESS.track_inprogress() # Option 2 - use decorator
    @REQUEST_RESPOND_TIME.time() # Option 2 - use decorator
    @REQUEST_RESPOND_TIME_HIST.time() # Does the same as summary, but store metrics in different buket depending of execution time taken
    def do_GET(self):
        #start_time=time.time() # Option1 - manual time track
        #REQUEST_COUNT.inc()
        REQUEST_COUNT.labels('prom_python_app', self.path).inc()
        #REQUEST_IN_PROGRESS.inc() # Option 1 - manual decrement
        self.reqdate = datetime.now()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>First Application</title></head><body style='color: #333; margin-top: 30px;'><center><h2>Welcome to our first Prometheus-Python application. " + str(self.reqdate) + "</center></h2></body></html>", "utf-8"))
        self.wfile.flush()  #actually send the response if not already done.
        time.sleep(2) # Mimic the execution time
        #REQUEST_RESPOND_TIME.observe(time.time() - start_time) # Option1 - manual time track
        #REQUEST_LAST_SERVED.set(time.time()) # Option 1 - manual set
        REQUEST_LAST_SERVED.set_to_current_time() # Option 2 - use embedded function
        #REQUEST_IN_PROGRESS.dec() # Option 1 - manual decrement

if __name__ == "__main__":
    # start prometheus server to export metrics
    start_http_server(addr=APP_IP,port=METRICS_PORT)
    # start main web server
    server = http.server.HTTPServer((APP_IP, APP_PORT), HandleRequests)
    server.serve_forever()