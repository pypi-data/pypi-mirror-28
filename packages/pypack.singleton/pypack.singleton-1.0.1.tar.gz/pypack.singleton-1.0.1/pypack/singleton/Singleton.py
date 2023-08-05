class Singleton:

    __instances = {}

    def __init__ (self, cls):
        if not isinstance(cls, type): raise TypeError('Only class can be decorated as Singleton')

        self._cls = cls

    def __call__ (self, *arg, **kwarg):
        if not self._cls in self.__instances:
            self.__instances[self._cls] = self._cls(*arg, **kwarg)
        else:
            if '__call__' in dir(self.__instances[self._cls]):
                self.__instances[self._cls](*arg, **kwarg)

        return self.__instances[self._cls]

    
    def get_instance (self):
        if isinstance(self, Singleton) and self._cls in list(self.__instances.keys()):    
            return self.__instances[self._cls]
        
        return None

    @classmethod
    def clear (cls):
        del Singleton.__instances
        Singleton.__instances = {}

    @classmethod
    def remove (cls, r):
        if r in cls.classes():
            del cls.__instances[r]

    @classmethod
    def pairs (cls):
        return cls.SingletonPairsIterator(cls.__instances)

    @classmethod
    def classes (cls):
        return cls.SingletonClassesIterator(list(cls.__instances.keys()))


    @classmethod
    def instances (cls):
        return cls.SingletonInstancesIterator(list(cls.__instances.values()))


    @classmethod
    def get (cls, g):
        if isinstance(g, Singleton) and g._cls in list(Singleton.__instances.keys()):
            return Singleton.__instances[g._cls]

        return None


    class SingletonIterator:

        def __init__ (self, l):
            self.l = l

        def __len__ (self):
            return len(self.l)

        def __iter__ (self):
            self.index = -1
            return self

        def __next__ (self):
            self.index += 1
            if self.index >= len(self.l): raise StopIteration
            return self.l[self.index]

        

    class SingletonClassesIterator (SingletonIterator):
        
        def __contains__ (self, e):
            if not isinstance(e, Singleton): return False

            for i in self:
                if i == e._cls: return True

            return False


    class SingletonInstancesIterator (SingletonIterator): pass


    class SingletonPairsIterator (SingletonIterator): pass