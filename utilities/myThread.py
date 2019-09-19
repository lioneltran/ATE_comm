
import time
import threading
#from utilities.log import Log
from configuration import ateConfig


class MyThread(threading.Thread):
    '''
    General thread class to support and simplify creation of Python threads
    Note - all threads are of equal priority
    '''

    def __init__(self, thread_id: object, name: object, counter: object, thread_function: object) -> object:
        '''
        MyThread object instance initializer
        :param thread_id: 
        :param name: 
        :param counter: 
        :param thread_function: 
        '''
        self.__stop_event = threading.Event()
        threading.Thread.__init__(self)

        self.thread_id = thread_id
        self.name = name
        self.counter = counter
        self.thread_function = thread_function

    def run(self):
        '''
        Run this instance's thread until completion
        :return: 
        '''
        ateConfig.log.logger.debug( "Starting " + self.name)
        # self.logger.info(_time(self.name, self.counter, 5)
        self.thread_function()
        ateConfig.log.logger.debug( "Exiting " + self.name)

    def join(self, timeout=None):
        '''
        Stop the thread and wait for it to end
        :param timeout (optional param) 
        :return: none
        '''
        self.__stop_event.set()
        threading.Thread.join(self, timeout)

    def print_time(self, thread_name, delay, counter):
        '''
        Print the thread's time statistics
        :param thread_name: 
        :param delay: 
        :param counter: 
        :return: 
        '''
        exitFlag = False
        while counter:
            if exitFlag:
                thread_name.exit()
            time.sleep(delay)
            ateConfig.log.logger.debug( "%s: %s" % (thread_name, time.ctime(time.time())))
            counter -= 1
