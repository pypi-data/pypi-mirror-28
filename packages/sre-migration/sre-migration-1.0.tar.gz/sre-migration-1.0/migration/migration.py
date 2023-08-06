import os
import sys
import shelve
import cx_Oracle
from datetime import datetime

class Migration:

    def __init__(self, options):
        self.startTime = datetime.now()
        self.dir = options.dir
        self.db = options.db
        self.range = options.range

    def run(self):
        if self.db == None:
            print ("DB connection is required -d user/pwd@//host:port/service")
            print (datetime.now() - self.startTime)
            quit()
        if self.dir == None:
            self.dir = os.getcwd()
        else:
            if os.path.exists(self.dir) == False:
                print ("Directory does not exist")
                print (datetime.now() - self.startTime)
                quit()
        if self.range == None:
            print ("Range is required -r 1000")
            print (datetime.now() - self.startTime)
            quit()
        self.dir = os.path.abspath(self.dir)
        self.shelve = shelve.open(os.path.join(self.dir, self.dir.replace("/", "_")), writeback = False)
        self.ids()
        self.send()
        print ("\n" + str(datetime.now() - self.startTime))

    def ids(self):
        dirs = os.walk(self.dir).next()[1]
        read = 0
        for dir in dirs:
            try:
                job = self.shelve[dir]
                if job["status"] == 0:
                    read += 1
            except KeyError:
                root = os.path.join(self.dir, dir)
                files = filter(lambda file: file.endswith(".wsq"), os.walk(root).next()[2])
                wsqs = [None, None, None, None, None, None, None, None, None, None]
                for file in files:
                    try:
                        number = int(file.replace(".wsq", "").split("_").pop())
                        if number <= len(wsqs):
                            wsqs[number - 1] = os.path.join(root, file)
                    except ValueError:
                        error = "Error format " + file
                        sys.stdout.write('\r' + error + '\n')
                        sys.stdout.flush()
                self.shelve[dir] = {"status" : 0, "wsqs" : wsqs}
                read += 1
            log = "Read " + str(read) + " of " + str(self.range) + " Jobs"
            sys.stdout.write('\r' + log)
            sys.stdout.flush()
            if read == self.range:
                break

    def send(self):
        print("\n")
        #jobs = dict(filter(lambda (a,(b,c)): self.shelve[a][b] == 0, self.shelve.items())[:self.range])
        jobs = dict(filter(lambda dic: self.shelve[dic[0]][dic[1][0]] == 0, self.shelve.items())[:self.range])
        for key, job in jobs.iteritems():
            self.request(key, job)

    def request(self, id, job):
        connection = cx_Oracle.connect(self.db)
        cursor = connection.cursor()
        wsqsBytes = list()
        varchar = cursor.var(cx_Oracle.STRING)
        varchar.setvalue(0, id)
        wsqsBytes.append(varchar)
        for wsq in job["wsqs"]:
            blob = cursor.var(cx_Oracle.BLOB)
            if wsq == None:
                blob.setvalue(0, None)
            else:
                try:
                    in_file = open(wsq, "rb")
                    data = in_file.read()
                    in_file.close()
                    blob.setvalue(0, data)
                except (TypeError, IOError) as exception:
                    print (exception)
                    blob.setvalue(0, None)
            wsqsBytes.append(blob)
        result = cursor.var(cx_Oracle.NUMBER)
        wsqsBytes.append(result)
        call = cursor.callproc("DMA_SRE2.P_IO_INSERT_TRM", wsqsBytes)
        cursor.close()
        if result.getvalue() == 0.0:
            job["status"] = 1
            self.shelve[id] = job
            print ("Saved " + id + " successfully")
        else:
            print ("An error occurred while saving " + id)
