class BaseEntity(object):
    
    def __init__(self, *args, **kwargs):
        self._base = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

