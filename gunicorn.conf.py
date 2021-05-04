import multiprocessing
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = "127.0.0.1:8000"
backlog = 2048                #监听队列
timeout = 60      #超时
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
# worker_connections = 1000
chdir = '/home/ubuntu/djangoProject'

# workers = multiprocessing.cpu_count() * 2 + 1    #进程数
workers = 4
# threads = multiprocessing.cpu_count() * 4    #指定每个进程开启的线程数

pidfile = '/home/ubuntu/djangoProject/logs/gunicorn.pid'
errorlog = '/home/ubuntu/djangoProject/logs/gunicorn.error.log' #发生错误时log的路径
accesslog = '/home/ubuntu/djangoProject/logs/gunicorn.access.log' #正常时的log路径
loglevel = 'info'   #日志等级
proc_name = 'gunicorn_project'   #进程名
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"' 
