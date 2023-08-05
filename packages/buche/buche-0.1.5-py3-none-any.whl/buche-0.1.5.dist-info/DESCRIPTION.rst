
Buche
=====

Helper package to pretty-print and interact with Python objects using the Buche_ logger.

Requires Python >= 3.6


Usage
-----

You must install Buche_ through npm first (``npm install -g buche``). This package helps interact with Buche, but it is not the application itself. Once you have written your script, use it as follows:

.. code:: bash

    buche python -u yourscript.py

Sample script:

.. code:: python
    from buche import buche

    buche(1234)
    buche([x * x for x in range(100)])
    buche(avocado="green", banana="yellow", cherry="red")

    buche['second_tab']("Hello")
    buche['third_tab/one'].html('<b>Hello!</b>')
    buche['third_tab/two'].markdown('**Hello!!**')

    buche.require('bokeh', channels='bokeh')
    plot = buche.open_bokeh('plot', title="Polynomials")
    for i in range(100):
        plot['square'].log_data(x=i, y=i*i)
        plot['cube'].log_data(x=i, y=i*i*i)


.. _Buche: https://github.com/breuleux/buche


