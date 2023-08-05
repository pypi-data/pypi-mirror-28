:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Progress Bar
============

The progress bar is a simple widget for showing a percentage progress for task completion.

Usage
-----

.. code-block:: Python

    import toga
    
    p_bar = toga.ProgressBar(max=100, value=1)
    
    # Update progress
    p_bar.value = 10

Supported Platforms
-------------------

.. include:: ../supported_platforms/ProgressBar.rst

Reference
---------

.. autoclass:: toga.widgets.progressbar.ProgressBar
   :members:
   :undoc-members:
   :inherited-members: