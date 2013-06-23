con-array-test
==============

``con-array-test`` is utility for checking -- how is working a HTTP-server
in situation with big array of connections.


Status
------

Beta branch version.


Example of using
----------------

    $ sudo -i
    # ulimit -n 100000
    # ./con-array-test www.example.org 1200 0.001

this command -- makes array of 1200 connections with delay 0.001 seconds.
