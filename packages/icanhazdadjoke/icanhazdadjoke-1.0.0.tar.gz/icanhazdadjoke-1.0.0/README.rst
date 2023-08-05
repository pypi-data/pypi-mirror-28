A Python library for icanhazdadjoke.com
=======================================

A very small project aimed mostly at learning some Python aspects

`The source for this project is available here
<https://github.com/vanakenm/icanhazdadjoke-python>`_.

https://icanhazdadjoke.com is built by Brett Langdon

For now it can only get a random joke:

.. code-block:: python

  from dadjokes import dadjokes
  joke = dadjokes.random

  print(joke)