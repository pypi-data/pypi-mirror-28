=============================
worker
=============================

simple worker

**Note**: this package is still in alpha. Use with caution !


Quickstart
----------

Install worker::

    pip install worker


Use worker:

.. code-block:: python

    data = [
               {'hello': 'world'},
           ] * 40
    info = {
        'worker': 'xxx.yyy.worker_do_sth'
    }
    worker = Worker(mode='thread')
    resp = worker.work(data, info)
    print(resp)




