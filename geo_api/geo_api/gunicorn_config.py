import os
import multiprocessing

loglevel = 'debug'
log_file = 'log/debug.log'
bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day
capture_output = True
