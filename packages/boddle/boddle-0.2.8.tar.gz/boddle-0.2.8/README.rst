.. figure:: https://cloud.githubusercontent.com/assets/2049665/21398745/27452db6-c76e-11e6-8605-8e5f3301472b.png
   :alt: image

   image

Boddle
======

A unit testing tool for Python's bottle library. We wrote this for our
own testing purposes at https://www.hvst.com. Thanks
`brenguyen711 <https://github.com/brenguyen711>`__ for the great name!

Install
-------

::

    sudo pip install boddle

Usage
-----

Assuming you have a bottle route like this:

.. code:: python

    @bottle.get('/woot')
    def woot():
      return bottle.request.params['name']

You can unit test it like:

.. code:: python

    import unittest
    from boddle import boddle

    class TestIt(unittest.TestCase):
      def testWoot(self):
        with boddle(params={'name':'derek'}):
          self.assertEqual(woot(), 'derek')

See ```example.py`` <example.py>`__.

Options
~~~~~~~

The Bottle-specific params that are supported are:

+-------------+----------+
| Argument    | Notes    |
+=============+==========+
| ``params``  | Populate |
|             | s        |
|             | ``reques |
|             | t.params |
|             | ``.      |
|             | Takes a  |
|             | ``dict`` |
|             | or list  |
|             | of       |
|             | pairs.   |
|             | Useful   |
|             | for both |
|             | POST and |
|             | GET      |
|             | params.  |
+-------------+----------+
| ``path``    | The path |
|             | componen |
|             | t        |
|             | of the   |
|             | url.     |
|             | Populate |
|             | s        |
|             | ``reques |
|             | t.path`` |
|             | ,        |
|             | which    |
|             | always   |
|             | has a    |
|             | preceedi |
|             | ng       |
|             | ``/``.   |
+-------------+----------+
| ``method``  | POST,    |
|             | GET,     |
|             | etc.     |
|             | Bottle   |
|             | will     |
|             | uppercas |
|             | e        |
|             | the      |
|             | value.   |
+-------------+----------+
| ``headers`` | Any HTTP |
|             | headers. |
|             | Takes a  |
|             | ``dict`` |
|             | .        |
+-------------+----------+
| ``json``    | Takes    |
|             | anything |
|             | that can |
|             | be       |
|             | consumed |
|             | by       |
|             | ``json.d |
|             | umps()`` |
|             | .        |
|             | Also     |
|             | sets the |
|             | content  |
|             | type of  |
|             | the      |
|             | request. |
+-------------+----------+
| ``url``     | The full |
|             | URL,     |
|             | protocol |
|             | ,        |
|             | domain,  |
|             | port,    |
|             | path,    |
|             | etc.     |
|             | Will be  |
|             | parsed   |
|             | until    |
|             | its      |
|             | ``urlpar |
|             | ts``     |
|             | before   |
|             | populati |
|             | ng       |
|             | ``reques |
|             | t.url``. |
+-------------+----------+
| ``body``    | The raw  |
|             | body of  |
|             | the      |
|             | request. |
|             | Takes    |
|             | either a |
|             | ``str``  |
|             | or a     |
|             | file-lik |
|             | e        |
|             | object.  |
|             | ``str``\ |
|             |  s       |
|             | will be  |
|             | converte |
|             | d        |
|             | into     |
|             | file-lik |
|             | e        |
|             | objects. |
|             | Populate |
|             | d        |
|             | ``reques |
|             | t.body`` |
|             | .        |
+-------------+----------+
| ``query``   | Populate |
|             | s        |
|             | ``reques |
|             | t.query` |
|             | `.       |
|             | Takes a  |
|             | ``dict`` |
|             | .        |
+-------------+----------+

All other keyword arguments will be assigned to the request object. For
instance, we often do:

.. code:: python

    with boddle(current_user=someone):
      # code that accesses bottle.request.current_user

You can also nest ``boddle`` calls. For instance:

.. code:: python

    with boddle(path='/woot'):
      with boddle(params={'name':'derek'}):
        # both path and params are set here
      # only path is set here

**ALL CHANGES TO ``bottle.request`` ARE REVERTED WHEN THE WITH BLOCK
ENDS.**

Testing
-------

.. figure:: https://api.travis-ci.org/keredson/boddle.svg?branch=master
   :alt: image

   image

::

    $ git clone https://github.com/keredson/boddle.git
    $ cd boddle
    $ python tests.py 
    ............
    ----------------------------------------------------------------------
    Ran 12 tests in 0.001s

    OK
