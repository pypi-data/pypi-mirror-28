
class Debug():
    def __init__(self,level=None):
        self.__LOG__ = False 
        pass
    def enable(self):
        self.__LOG__ = True 
    def disable(self):
        self.__LOG__ = False 
        
    def get_logger(self):
        def logger(line):
            if self.__LOG__:
                print line 
        return logger 

