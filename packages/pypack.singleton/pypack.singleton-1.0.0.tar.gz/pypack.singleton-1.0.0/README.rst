pypack.singleton 1.0.0
======================

**pypack.singleton** is singleton design pattern for python3, 
simple to use and customize

Installation:
-------------
.. code-block:: sh

    pip install pypack.singleton

Import and Example Usage:
-------------------------

.. code-block:: python3

    from pypack.singleton import Singleton

    @Singleton
    class ASingletonClass: pass

    # ASingletonClass now is a singleton

Method List of Singleton:
-------------------------

.. code-block:: python3

    # clear all singleton instances
    Singleton.clear() -> None:

    # remove class i from Singleton
    Singleton.remove(i : Singleton) -> None:

    # get instance of singleton class
    Singleton.get(i : Singleton) -> Union(None, Any)

    # Iterator of each class in singleton
    Singleton.classes() -> Singleton.SingletonClassesIterator:

    # Iterator of each instance in singleton
    Singleton.instances() -> Singleton.SingletonInstancesIteratorL

    # Iterator of Pair<Class, Instance> in singleton
    Singleton.pairs() -> Singleton.SingletonPairsIterator:


Method List of Singleton signed Class:
--------------------------------------

suppose you have marked a class as a Singleton

.. code-block:: python3

    @Singleton
    class MySingleton:
        """Just a custom Singleton class"""

        def __init__ (self, *args, **kwargs):
            pass

        def __call__ (self, *args, **kwargs):
            pass

you can interact with your singleton in this way:

.. code-block:: python3

    # MySingleton in Singleton.classes() == False (Not Created yet)

    s1 = MySingleton() # Singleton is actually created here
                       # and MySingleton.__init__(s1) is called

    # MySingleton in Singleton.classes() == True (Created)

    s2 = MySingleton() # Singleton of MySingleton already
                       # exists so, MySingleton.__call__(s2) is called
                       # if MySingleton.__call__ is missing nothing is called

    # s1 == s2 -> True

    # Retrive already created instance or None
    s3 = MySingleton.get_instance() -> Union (None, Any):

    # s1 == s2 == s3

    

