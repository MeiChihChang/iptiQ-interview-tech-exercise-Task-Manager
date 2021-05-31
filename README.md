# iptiQ-interview-tech-exercise-Task-Manager
iptiQ EMEA P&amp;C interview tech exercise 

Example of a Python multiprocessing implementation to manage worker processes with addprocess, kill and list functions

Consists of 2 classes:

## TaskManager class
This class creates and initialises a set number of workers and managers addprocess, kill and list functions.
MAX_CAPACITY = min(multiprocessing.cpu_count(), 32)
The prefixed maximum capacity :MAX_CAPACITY is the limitation can not have more than a certain number of running processes within the manager

### addprocess(TaskProcess, mode=None)
when mode == None is the default behaviour, that the manager can accept new processes till when there is capacity inside the manager, otherwise it won’t accept any new process.
when mode == "force", the manager accepts all new processes by killing and removing from the manager list the oldest one (First-In, First-Out) when the max size
is reached.
when mode == "priority", when the max capacity is reached, the manager will result into an evaluation: if the new process has a higher priority compared to any of the existing one, the manager removes the lowest priority that is the oldest, otherwise the manager skip it

### list(mode=None)
when mode == None is the default behaviour, the manager list all the running processes, sorting them by time
when mode == "priority", the manager list all the running processes, sorting them by priority
when mode == "pid", the manager list all the running processes, sorting them by pid

### kill(pid=None, priority=None)
when pid is not None, the manager will kill a specific process with pid
when priority>0, the manager will kill all processes with the same priority
when priority<0, the manager will kill all processes

## TaskProcess class
The WorkerProcess class extends the base multiprocessing.Process class to add process's priority (low, medium, high) featue.

## main.py
This is used to test all functions

