JMaster
=======

Parse CodeForces contests and auto test sample.

Install
-------

Using pip
~~~~~~~~~

.. code:: shell

    $ pip3 install JMaster

Manual
~~~~~~

.. code:: shell

    $ git clone https://github.com/palayutm/JMaster.git
    $ cd JMaster
    $ python3 setup.py install

Usage
-----

View contest info
~~~~~~~~~~~~~~~~~

.. code:: shell

    $ JMaster contest

.. figure:: https://github.com/palayutm/JMaster/raw/master/img/contest.png
   :alt: 

Parse contest
~~~~~~~~~~~~~

Parse normal contests
^^^^^^^^^^^^^^^^^^^^^

.. code:: shell

    $ JMaster parse CONTEST_ID

.. figure:: https://github.com/palayutm/JMaster/raw/master/img/parse-contest.png
   :alt: 

Parse gym contests
^^^^^^^^^^^^^^^^^^

.. code:: shell

    $ JMaster parse --gym CONTEST_ID

.. figure:: https://github.com/palayutm/JMaster/raw/master/img/parse-gym.png
   :alt: 

Test sample
~~~~~~~~~~~

.. code:: shell

    $ JMaster test CPP_FILE [SAMPLE_FILE]

sample code (a.cc)

.. code:: cpp

    #include <bits/stdc++.h>

    using namespace std;

    int main(int argc, char *argv[]) {
      int a, b;
      cin >> a >> b;
      assert(a > b);    // test runtime error
      cout << a + b << endl;
      return 0;
    }

test case (a.sample)

::

    -- normal test
    2 1
    --
    3

    -- runtime error test
    1 1
    --
    2

    -- wrong answer test
    2 1
    --
    4

.. figure:: https://github.com/palayutm/JMaster/raw/master/img/test-problem.png
   :alt: 

Further Usage
~~~~~~~~~~~~~

.. code:: shell

    $ JMaster --help
