"""
    Container for a number of useful classes that don't warrant creation of 
    an entire category or module.
"""
from contextlib import ContextDecorator

class OpeningContextDecorator(ContextDecorator):
    """
        Assumes that the class being decorated has **open()** and **close()** methods.
        Just a basic convenience to save the need to implement **__enter__** and **__exit__**
        methods.
    """
    def __enter__(self):
        "The generic enter method"
        self.open()
        return self

    def __exit__(self, *_):
        "The generic exit method"
        self.close()
        return False

    def open(self):
        "Abstract open() method"
        pass

    def close(self):
        "Abstract close() method"
        pass
