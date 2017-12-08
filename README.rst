What is this?
=============

This is a really thin shiv that lets you run static d3js scripts to produce
SVG / HTML outputs in your Jupyter notebooks. Underneath the covers, 
it uses `d3-node <https://www.npmjs.com/package/d3-node>`_. 

Why is this?
------------

Because it makes writing my dissertation easier. I have some dynamic
visualizations that are d3-based. But, for the write-up, I also have
static snapshots as illustrations. This is my DRY hack. It let's me reuse
the code in a way that isn't terribly intrusive. (Well, that, and I don't
like out-of-Jupyter-core JS in my notebooks.)


Installation
------------

Assuming you have ``node`` and ``yarn``,

.. code-block:: sh

   pip install d3nb

Usage
-----

The following snippet runs the given cell source with 
``my_node_project_dir`` as the working directory, then outputs
the SVG. If that directory doesn't exist, you can run the 
initial cell magic line as, ``%%d3nb_svg my_node_project_dir --init`` 
to set it up.

.. code-block:: javascript

   %%d3nb_svg my_node_project_dir
   var D3Node = require('d3-node')
   var d3 = require('d3')
   var d3n = new D3Node()
   var svg = d3n.createSVG()

   // See: https://www.npmjs.com/package/d3-node
   // ...

   console.log(d3n.svgString())

