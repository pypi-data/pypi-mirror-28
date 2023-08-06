=========
Agstream
=========

Agriscope data interface for python

This module allows to get data from yours Agribases programmatically
Data are retreived as an Pandas Datagrams

The development map will introduce data computing capabilities, to enhance
data analysis comming from agricultural field.


What's New
===========
- First version (02 / 2018)

Dependencies
=============

Agstream is written to be use with python 2.7
It requires `Pandas`_ (>= 0.12.0)::

    pip install pandas

Installations
=============
    pip install agstream


Uses cases
==========    


    >>> from agstream.session import AgspSession
    >>> session = AgspSession()
    >>> session.login('masnumeriqueAgStream', '1AgStream', updateAgribaseInfo=True)
    >>> for abs in session.agribases :
    >>>     df = session.getAgribaseDataframe(abs)
    >>>     print df.tail()


