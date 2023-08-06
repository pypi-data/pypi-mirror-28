=======
acrilib
=======

----------------------------------------------------
Independent programming idioms and utilities library
----------------------------------------------------

.. contents:: Table of Contents
   :depth: 2

Overview
========

    **acrilib** is a python library providing useful programming patterns and tools. **acrilib** started as Acrisel's internal idioms and utilities for programmers. The main key is that this library is completely independent. It does not use any external packages beside what provided by Python.
    
    It includes:
        1. programming idioms that are repeatedly used by programmers.
        #. helpers functions for logging and other utilities.
    
    We decided to contribute this library to Python community as a token of appreciation to
    what this community enables us.
    
    We hope that you will find this library useful and helpful as we find it.
    
    If you have comments or insights, please don't hesitate to contact us at support@acrisel.com
    
Programming Idoms
=================

threaded
--------

    decorator for methods that can be executed as a thread.  RetriveAsycValue callable class used in the example below provide means to access results.  One can provide their own callable to pass results. 

example
~~~~~~~

    .. code-block:: python

        from acris import threaded, RetriveAsycValue
        from time import sleep

        class ThreadedExample(object):
            @threaded
            def proc(self, id_, num, stall):
                s = num
                while num > 0:
                    print("%s: %s" % (id_, s))
                    num -= 1
                    s += stall
                    sleep(stall)
                print("%s: %s" % (id_, s))  
                return s

          
example output
~~~~~~~~~~~~~~

    .. code-block:: python

        print("starting workers")
        te1 = ThreadedExample().proc('TE1', 3, 1)
        te2 = ThreadedExample().proc('TE2', 3, 1)
    
        print("collecting results")
        te1_callback = RetriveAsycValue('te1')
        te1.addCallback(te1_callback)
        te2_callback = RetriveAsycValue('te2')
        te2.addCallback(te2_callback)
    
        print('joining t1')
        te1.join()
        print('joined t1')
        print('%s callback result: %s' % (te1_callback.name, te1_callback.result))
        result = te1.syncResult()
        print('te1 syncResult : %s' %result)
    
        result = te2.syncResult()
        print('te2 syncResult : %s' % result)
        print('%s callback result: %s' % (te2_callback.name, te2_callback.result))

    will produce:

    .. code-block:: python

        starting workers
        TE1: 3
        TE2: 3
        collecting results
        joining t1
        TE1: 4
        TE2: 4
        TE1: 5
        TE2: 5
        TE1: 6
        TE2: 6
        joined t1
        te1 callback result: 6
        te1 syncResult : 6
        te2 syncResult : 6
        te2 callback result: 6
        
Singleton and NamedSingleton
----------------------------

    meta class that creates singleton footprint of classes inheriting from it.

Singleton example
~~~~~~~~~~~~~~~~~

    .. code-block:: python

        from acris import Singleton

        class Sequence(Singleton):
            step_id=0
    
            def __call__(self):
                step_id = self.step_id
                self.step_id += 1
                return step_id  

example output
~~~~~~~~~~~~~~

    .. code-block:: python
 
        A=Sequence()
        print('A', A())
        print('A', A())
        B=Sequence()
        print('B', B()) 

    will produce:

    .. code-block:: python

        A 0
        A 1
        B 2
    
NamedSingleton example
~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: python

        from acris import Singleton

        class Sequence(NamedSingleton):
            step_id = 0
            
            def __init__(self, name=''):
                self.name = name
    
            def __call__(self,):
                step_id = self.step_id
                self.step_id += 1
                return step_id  

example output
~~~~~~~~~~~~~~

    .. code-block:: python
 
        A = Sequence('A')
        print(A.name, A())
        print(A.name, A())
        B = Sequence('B')
        print(B.name, B()) 

    will produce:

    .. code-block:: python

        A 0
        A 1
        B 0
    
Sequence
--------

    meta class to produce sequences.  Sequence allows creating different sequences using name tags.

example
~~~~~~~

    .. code-block:: python

        from acris import Sequence

        A = Sequence('A')
        print('A', A())
        print('A', A())
        B = Sequence('B')
        print('B', B()) 
    
        A = Sequence('A')
        print('A', A())
        print('A', A())
        B = Sequence('B')
        print('B', B()) 

example output
~~~~~~~~~~~~~~

    .. code-block:: python
     
        A 0
        A 1
        B 0
        A 2
        A 3
        B 1

TimedSizedRotatingHandler
-------------------------
	
    TBD

        
Decorators
----------

    Useful decorators for production and debug.
    
traced_method
~~~~~~~~~~~~~

    logs entry and exit of function or method.
    
    .. code-block :: python
    
        from acris import traced_method

        traced = traced_method(print, print_args=True, print_result=True)

        class Oper(object):
            def __init__(self, value):
                self.value = value
        
            def __repr__(self):
                return str(self.value)
        
            @traced
            def mul(self, value):
                self.value *= value 
                return self   
    
            @traced
            def add(self, value):
                self.value += value
                return self
    
        o=Oper(3)
        print(o.add(2).mul(5).add(7).mul(8))
        
    would result with the following output:
    
    .. code-block :: python
        
        [ add ][ entering][ args: (2) ][ kwargs: {} ][ trace_methods.py.Oper(39) ]
        [ add ][ exiting ] [ time span: 0:00:00.000056][ result: 5 ][ trace_methods.py.Oper(39) ]
        [ mul ][ entering][ args: (5) ][ kwargs: {} ][ trace_methods.py.Oper(34) ]
        [ mul ][ exiting ] [ time span: 0:00:00.000010][ result: 25 ][ trace_methods.py.Oper(34) ]
        [ add ][ entering][ args: (7) ][ kwargs: {} ][ trace_methods.py.Oper(39) ]
        [ add ][ exiting ] [ time span: 0:00:00.000007][ result: 32 ][ trace_methods.py.Oper(39) ]
        [ mul ][ entering][ args: (8) ][ kwargs: {} ][ trace_methods.py.Oper(34) ]
        [ mul ][ exiting ] [ time span: 0:00:00.000008][ result: 256 ][ trace_methods.py.Oper(34) ]
        256
	
Data Types
----------

    varies derivative of Python data types

MergeChainedDict
~~~~~~~~~~~~~~~~

    Similar to ChainedDict, but merged the keys and is actually derivative of dict.

    .. code-block:: python

        a={1:11, 2:22}
        b={3:33, 4:44}
        c={1:55, 4:66}
        d=MergedChainedDict(c, b, a)
        print(d) 

    Will output:

    .. code-block:: python

    	{1: 55, 2: 22, 3: 33, 4: 66}

        
Mediator
--------
    
    Class interface to generator allowing query of has_next()
    
Example 
~~~~~~~

    .. code-block:: python

        from acris import Mediator

        def yrange(n):
            i = 0
            while i < n:
                yield i
                i += 1

        n = 10
        m = Mediator(yrange(n))
        for i in range(n):
            print(i, m.has_next(3), next(m))
        print(i, m.has_next(), next(m))

Example Output
~~~~~~~~~~~~~~

    .. code-block:: python

        0 True 0
        1 True 1
        2 True 2
        3 True 3
        4 True 4
        5 True 5
        6 True 6
        7 True 7
        8 False 8
        9 False 9
        Traceback (most recent call last):
          File "/private/var/acrisel/sand/acris/acris/acris/example/mediator.py", line 19, in <module>
            print(i, m.has_next(), next(m))
          File "/private/var/acrisel/sand/acris/acris/acris/acris/mediator.py", line 38, in __next__
            value=next(self.generator)
        StopIteration   
        

setup tools
===========
    
Methods to use in standard python environment
     
Change History
==============

Version 1.0
------------

    1. Initial publication to open source



    