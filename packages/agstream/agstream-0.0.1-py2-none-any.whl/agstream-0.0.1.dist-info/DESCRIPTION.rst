# agstream
Agriscope data interface for python

2018 01 20 : First version
Agstream Lib - Agriscope data inferface for python
==================================================

This module allows to get data from yours Agribases programmatically
Data are retreived as an Pandas Datagrame

You can install it bye pip:

    pip install agstream

Use case:

    >>> from agstream.session import AgspSession
    >>> session = AgspSession()
    >>> session.login('masnumeriqueAgStream', '1AgStream', updateAgribaseInfo=True)
    >>> for abs in session.agribases :
    >>>     df = session.getAgribaseDataframe(abs)
    >>>     print df.tail()


