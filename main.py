from taskmgr import TaskProcess, TaskManager
import os
import time

PROCESS_PRIORITY_LEVEL = range(0,3)  # process priority level range from 0 to 2. Level 0 is the highest.

def info(title):
    print(title)
    print('process id: {} \n'.format(os.getpid()))

def long_test_task(name):
    info('function f' + name)  
    time.sleep(100) 

if __name__ == '__main__' :
    manager = TaskManager()
    p_list = []
    for idx in reversed(range(6)):
        p = TaskProcess(target=long_test_task, priority=idx % 3, args=(str(idx),))
        p_list.append(p)
        result = TaskManager().addProcess(p)
        if result == True:
            p.start()
        time.sleep(1)   
    
    ####################################################################################################
    ## TEST addprocess functions     
    
    p7 = TaskProcess(target=long_test_task, priority=2, args=(str(7),))
    p_list.append(p7)
    
    # addprocess sould be rejected with default mode: accept new processes till when there is capacity
    result = manager.addProcess(p7)
    print("add process {} with defailt mode, result = {}".format(p7, result))  

    print("####################\npid   priority time")  
    task_list = manager.list()      
    for item in task_list:
        print("{} {}        {}".format(item[0], item[1], item[2]))  

    # addprocess sould be not rejected with "force" mode: accept new processes with killing and removing from the TM list the oldest one (First-In, First-Out) when the max size is reached
    result = manager.addProcess(p7, mode="force")
    if result == True:
        p7.start()
        time.sleep(1)  
         
    print("add process {} result = {} with force mode,".format(p7.pid, result))   
    
    print("####################\npid   priority time")  
    task_list = manager.list()      
    for item in task_list:
        print("{} {}        {}".format(item[0], item[1], item[2]))  

    # a process with higher priority should be added by addprocess with priority mode, which the lowest priority and the oldest one is removed
    p8 = TaskProcess(target=long_test_task, priority=1, args=(str(8),)) 
    p_list.append(p8)
    result = manager.addProcess(p8, mode="priority")
    if result == True:
        p8.start()
        time.sleep(1)   
    print("add process {} priority: {} result = {} with priority mode,".format(p8.pid, p8.priority, result))  

    print("####################\npid   priority time")  
    task_list = manager.list()      
    for item in task_list:
        print("{} {}        {}".format(item[0], item[1], item[2]))   

    ####################################################################################################
    ## TEST kill & list functions       

    print("####################\nkill the process: pid = {}".format(p_list[2].pid))       
    manager.kill(p_list[2].pid)

    print("####################\npid   priority time")  
    task_list = manager.list()      
    for item in task_list:
        print("{} {}        {}".format(item[0], item[1], item[2]))  

    print("####################\nkill priority = {}".format(1))       
    manager.kill(priority=1)   

    task_list = manager.list(mode="priority") 
    print("####################list by priority order\npid   priority time")       
    for item in task_list:
        print("{} {}        {}".format(item[0], item[1], item[2]))  

    print("####################\nkill all")       
    manager.kill(priority=-1) 

    task_list = manager.list() 
    print("####################\npid   priority time")       
    for item in task_list:
        print("{} {}        {}".format(item[0], item[1], item[2]))   

    # wait for all task finished
    for task in task_list:
        task.join()              

        