from bean import *
from datetime import datetime,timedelta

def today_range():
    #show the current doing task
    today = datetime.now()
    today = datetime(today.year,today.month,today.day)
    yesterday = today 
    today = datetime(today.year,today.month,today.day) + timedelta(days = 1)

    return 

class TaskManager(object):
    NOT_STARTED = 0
    STARTED = 1
    PAUSED = 2
    DONE = 3
    ABORTED = 4

    @staticmethod
    def add_task(**kwargs):
        """add a new task to undone queue
        bean status:
            0 -> not started
            1 -> started
            2 -> paused
            3 -> done
            4 -> aborted
        """
        kwargs["bt"] = "task"
        kwargs["status"] = TaskManager.NOT_STARTED
        return BeanManager.add_bean(**kwargs)

    @staticmethod
    def complete_task(**kwargs):
        """complete a task"""
        kwargs["status"] = TaskManager.DONE
        kwargs["when_done"] = datetime.now()
        TaskManager.modify_task(**kwargs)

    @staticmethod
    def modify_task(**kwargs):
        kwargs["bt"] = "task"
        BeanManager.modify_bean(**kwargs)

    @staticmethod
    def start_task(**kwargs):
        """start a task and start clocking"""
        #start timing
        #notify when time is over
        kwargs["status"] = TaskManager.STARTED
        kwargs["when_started"] = datetime.now()
        TaskManager.modify_task(**kwargs)

    @staticmethod
    def pause_task(**kwargs):
        """pause a current running task"""
        kwargs["status"] = TaskManager.PAUSED
        TaskManager.modify_task(**kwargs)

    @staticmethod
    def resume_task(**kwargs):
        """resume a paused task"""
        kwargs["status"] = TaskManager.STARTED
        kwargs["when_started"] = datetime.now()
        TaskManager.modify_task(**kwargs)

    @staticmethod
    def abort_task(**kwargs):
        """abort a task"""
        kwargs["status"] = TaskManager.ABORTED
        kwargs["when_aborted"] = datetime.now()
        TaskManager.modify_task(**kwargs)
    
    @staticmethod
    def get_tasks(criteria):
        criteria["bt"] = "task"
        return BeanManager.get_beans(criteria)

    def __getattr__(self,attr):
        t_dict = {
            "not_started":{"status":TaskManager.NOT_STARTED},
            "started":{"status":TaskManager.STARTED},
            "paused":{"status":TaskManager.PAUSED},
            "aborted":{"status":TaskManager.PAUSED},
            "done":{"status":TaskManager.DONE},
            "remaining":{"status":{"$in":[TaskManager.NOT_STARTED ,TaskManager.PAUSED]}},
            "abortable":{"status":{"$in":[TaskManager.NOT_STARTED ,TaskManager.PAUSED,TaskManager.STARTED]}},
            "completable":{"status":{"$in":[TaskManager.NOT_STARTED ,TaskManager.PAUSED,TaskManager.STARTED,TaskManager.PAUSED]}},
        }
        def wrapper():
            _,t,_ = attr.split("_")
            criteria = t_dict[t]
            print criteria
            return TaskManager.get_tasks(criteria)
        return wrapper


class TaskFormatter(object):
    status_dict = {
            0 :"not started",
            1 :"started",
            2 :"paused",
            3 :"done",
            4 :"aborted",
    }

    @staticmethod
    def format_not_started(t):
        return "%-20s  %s  %10s  %12s" %( t['content'],\
                                               t["urgent"] + t["important"],\
                                               t['when_created'].strftime("%H:%M"),\
                                               TaskFormatter.status_dict[t["status"]])

    @staticmethod
    def format_started(t):
        return "%-20s  %s  %10s" %( t['content'],\
                                               t["urgent"] + t["important"],\
                                               t['when_started'].strftime("%H:%M"))
    @staticmethod
    def format_abortable(t):
        return "%-20s" %( t['content'] )

    @staticmethod
    def format_remaining(t):
        return "%-20s" %( t['content'] )

    @staticmethod
    def format_completable(t):
        return "%-20s" %( t['content'] )
