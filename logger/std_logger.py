import os
import sys
import datetime


class StdLogger():

    def __init__(self, filename):
        # build up full path to filename
        logfile = "./logs/" + filename
        #self.log = open(logfile, 'w')
        self.terminal = sys.stdout
        self.log = open(logfile, 'a')

    def write(self, message):
        timestamp = datetime.datetime.strftime(datetime.datetime.utcnow(),
                                               '%d-%m-%s-%H:%M:%S.%f')
        # write to screen
        self.terminal.write(message)
        # write to file
        self.log.write(timestamp + ' - ' + message)
        self.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()
        os.fsync(self.log.fileno())

    def close(self):
        self.log.close()


def main(debug=False):
    if debug:
        sys.stdout = StdLogger()
        sys.stderr = sys.stdout


def init_std_logger():
    #sys.stdout = StdLogger(filename)
    #sys.stderr = sys.stdout
    sys.stderr = StdLogger("logfile.log")


if __name__ == '__main__':
    main(debug=True)
