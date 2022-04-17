import multiprocessing

bind = '192.168.9.128:9999'
worker_class = 'gevent'
# workers = 2 * multiprocessing.cpu_count() + 1
workers = 4
daemon = True
loglevel = 'info'
errorlog = './gunicorn.log'
accesslog = './access.log'
capture_output = True
