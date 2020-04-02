# -*- coding: utf-8 -*-

import threading
from threading import Thread
import sys
import time
import random
from queue import Queue

class ThreadPoolManger():
  def __init__(self, thread_num):
    self.work_queue = Queue()
    self.thread_num = thread_num
    self.__init_threading_pool(self.thread_num)

  def __init_threading_pool(self, thread_num):
    for i in range(thread_num):
      thread = ThreadManger(self.work_queue)
      thread.start()

  def add_job(self, func, args):
    self.work_queue.put((func, args))

class ThreadManger(Thread):
  def __init__(self, work_queue):
    Thread.__init__(self)
    self.work_queue = work_queue
    self.daemon = True

  def run(self):
    while True:
      target, args = self.work_queue.get()
      a, b = args
      target(a, b)
      self.work_queue.task_done()