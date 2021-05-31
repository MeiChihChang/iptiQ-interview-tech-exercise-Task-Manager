import multiprocessing
from datetime import datetime

# prefixed maximum capacity can not over # of cpu core
MAX_CAPACITY = min(multiprocessing.cpu_count(), 6)

class TaskProcess(multiprocessing.Process):
    priority = -1
    timetag = None # record process create time
    """Override init to attach parent_conn pipe as class member for manager to communicate with worker"""
    def __init__(self, priority, group=None, target=None, name=None, args=(), kwargs={}):
        super().__init__(
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs
        )

        self.priority = priority
        self.timetag = datetime.now()

class TaskManager():
    workers = []
    def __init__(self):pass

    def addProcess(self, TaskProcess, mode=None):
        # clear non alive process
        for worker in self.workers:
            if not worker.is_alive():
                self.workers.remove(worker)

        worker_count = len(self.workers)
  
        if mode == None:
            if worker_count >= MAX_CAPACITY:
                return False
            else:
                self.workers.append(TaskProcess)
                worker_count = len(self.workers)
                return True
        elif mode == "force":
            if worker_count < MAX_CAPACITY:
                self.workers.append(TaskProcess)
                return True
            else:
                # remove the first one (FIFO)
                worker = self.workers[0]
                if worker.is_alive():
                    worker.terminate()
                    worker.join()
                self.workers.remove(worker)
                self.workers.append(TaskProcess)
                return True
        elif mode == "priority":
            priority = TaskProcess.priority
            found = -1
            found_priority = -1
            # sort the list by priority
            sorted_index_workers = sorted(range(len(self.workers)), key=lambda k: self.workers[k].priority)
            for idx in sorted_index_workers:
                if self.workers[idx].priority > priority:
                    if self.workers[idx].priority > found_priority:
                        found_priority = self.workers[idx].priority
                        found = idx
            if found >= 0:
                worker = self.workers[found]
                if worker.is_alive():
                    worker.terminate()
                    worker.join()
                self.workers.remove(worker)
                self.workers.append(TaskProcess)
                return True
            else:
                return False
    
    def list(self, mode=None):
        if mode == None:
            return_list = []
            for worker in self.workers:
                return_list.append((worker.pid, worker.priority, worker.timetag.strftime("%m/%d/%Y %H:%M:%S")))
            return return_list
        elif mode == "priority":
            return_list = []
            sorted_index_workers = sorted(range(len(self.workers)), key=lambda k: self.workers[k].priority)
            for idx in sorted_index_workers:
                return_list.append((self.workers[idx].pid, self.workers[idx].priority, self.workers[idx].timetag.strftime("%m/%d/%Y %H:%M:%S")))
            return return_list
        elif mode == "pid":   
            return_list = []
            sorted_index_workers = sorted(range(len(self.workers)), key=lambda k: self.workers[k].pid)
            for idx in sorted_index_workers:
                return_list.append((self.workers[idx].pid, self.workers[idx].priority, self.workers[idx].timetag.strftime("%m/%d/%Y %H:%M:%S")))
            return return_list
        else:
            return None

    def kill(self, pid=None, priority=None):
        if pid == None and priority == None:
            return False
        if pid != None and priority != None:
            return False
        if pid != None:
            for worker in self.workers:
                if worker.pid == pid:
                    if worker.is_alive():
                        worker.terminate()
                        worker.join()
                    self.workers.remove(worker)
                    break
        else:
            for worker in reversed(self.workers):            
                if (priority < 0) or (priority >= 0 and worker.priority == priority):
                    if worker.is_alive():
                        worker.terminate()
                        worker.join()
                    self.workers.remove(worker)