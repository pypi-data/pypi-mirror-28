easyLDA
-------

|PyPI version|

easyLDA is a library that easily build LDA Topic Models with just a list of docs (e.g. a list of twitter posts in CSV/TXT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

github: https://github.com/shichaoji/easyLDA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  If you have a collection of documents, and what to explore the
   relationship & topics of the docs, easyLDA is a very handy library to
   use. Simply run the commend and you'll get a trained LDA model with
   results visualized

The library pipeline text preprocessing, such as tf-idf, n-grams from Gensim library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Credit to:

https://radimrehurek.com/gensim/

http://pyldavis.readthedocs.io/en/latest/readme.html

.. |PyPI version| image:: https://badge.fury.io/py/easyLDA.svg
   :target: https://badge.fury.io/py/easyLDA

installation
~~~~~~~~~~~~

``$ pip install easyLDA``

usage example
~~~~~~~~~~~~~

simple need a text file (.csv) with each row represents a document (a post, comment, short article etc.), with only one column which is the text
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

text file (csv) sample view
^^^^^^^^^^^^^^^^^^^^^^^^^^^

easy to use, just in a shell window, type: easyLDA, then specify the location of the text document
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. then choose how many topics you want the model to fit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2. choose the topic contains only single word (1) or can be phases (2/3) as well
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the program will be starting to train
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  in shell $ easyLDA

model result
~~~~~~~~~~~~

models folder created by program contains the trained model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

xx.html file is the interactive visulization of the model result
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

visualization live example
~~~~~~~~~~~~~~~~~~~~~~~~~~











