FPT-cli
=======

*Facilitame los Partidos del Torneo*

Estadísticas de la primera división del fútbol argentino por línea de
comandos.

Instalación
===========

Usando ``pip``
~~~~~~~~~~~~~~

.. code:: bash

    $ pip install fpt-cli

Desde el source
~~~~~~~~~~~~~~~

.. code:: bash

    $ git clone https://github.com/el-ega/fpt-cli.git
    $ cd fpt-cli
    $ python setup.py install

Debería correr en Linux, Mac OS X, NetBSD, FreeBSD y Windows.

Cómo se usa?
============

Ver posiciones del torneo
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ fpt --posiciones

Ver tabla del descenso
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ fpt --descenso

Ver fixture para un equipo particular
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ fpt --equipo=Boca

Ver fecha actual
~~~~~~~~~~~~~~~~

.. code:: bash

    $ fpt --fecha-actual

Ver resultados de partidos en juego
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ fpt --en-juego

Ayuda
~~~~~

.. code:: bash

    $ fpt --help

Licencia
========

Liberado bajo `MIT License`_

*Inspirado en https://github.com/architv/soccer-cli*

.. _MIT License: LICENSE
