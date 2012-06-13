from bean import *
from datetime import datetime,timedelta

class IdeaManager(object):
    UNFOCUSED = 0
    FOCUSED = 1
    GIVEN_UP= 2
    FINISHED = 3

    @staticmethod
    def add_idea(**kwargs):
        """add a new idea to undone queue
        bean status:
            0 -> not focused
            1 -> being focused
            2 -> given up
            3 -> finished
        """
        kwargs["bt"] = "idea"
        kwargs["status"] = IdeaManager.UNFOCUSED
        return BeanManager.add_bean(**kwargs)

    @staticmethod
    def focus_idea(**kwargs):
        """focus a idea"""
        kwargs["status"] = IdeaManager.FOCUSED
        kwargs["when_focused"] = datetime.now()
        IdeaManager.modify_idea(**kwargs)

    @staticmethod
    def giveup_idea(**kwargs):
        """giveup a idea"""
        kwargs["status"] = IdeaManager.GIVEN_UP
        kwargs["when_givenup"] = datetime.now()
        IdeaManager.modify_idea(**kwargs)

    @staticmethod
    def finish_idea(**kwargs):
        """finish a idea"""
        kwargs["status"] = IdeaManager.FINISHED
        kwargs["when_finished"] = datetime.now()
        IdeaManager.modify_idea(**kwargs)

    @staticmethod
    def modify_idea(**kwargs):
        kwargs["bt"] = "idea"
        BeanManager.modify_bean(**kwargs)
    
    def __getattr__(self,attr):
        t_dict = {
            "unfocused":{"status":IdeaManager.UNFOCUSED},
            "focused":{"status":IdeaManager.FOCUSED},
            "givenup":{"status":IdeaManager.GIVEN_UP},
            "finished":{"status":IdeaManager.FINISHED},
            "remaining":{"status":{"$in":[IdeaManager.FOCUSED,IdeaManager.UNFOCUSED]}},
        }
        def wrapper():
            _,t,_ = attr.split("_")
            criteria = t_dict[t]
            return IdeaManager.get_ideas(criteria)
        return wrapper

    @staticmethod
    def get_ideas(criteria):
        criteria["bt"] = "idea"
        return BeanManager.get_beans(criteria)

class IdeaFormatter(object):
    status_dict = {
            0 :"not focused",
            1 :"focused",
            2 :"given up",
            3 :"finished",
    }

    @staticmethod
    def format_unfocused(t):
        return "%-20s  %10s" %( t['content'],t['when_created'].strftime("%H:%M"))

    @staticmethod
    def format_focused(t):
        return "%-20s  %10s" %( t['content'],t['when_focused'].strftime("%H:%M"))

    @staticmethod
    def format_givenup(t):
        return "%-20s  %10s" %( t['content'],t['when_givenup'].strftime("%H:%M"))

    @staticmethod
    def format_finished(t):
        return "%-20s  %10s" %( t['content'],t['when_finished'].strftime("%H:%M"))

    @staticmethod
    def format_remaining(t):
        return "%-20s %10s" %( t['content'],IdeaFormatter.status_dict[t["status"]])
