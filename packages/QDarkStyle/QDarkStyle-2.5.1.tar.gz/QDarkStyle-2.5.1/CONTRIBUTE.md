Contribute
==========

This file describes a path to contribute to this project.

Bug Reports and Feature Requests
--------------------------------

If you have encountered a problem with QDarkStyle or have an idea for a new
feature, please submit it to the
[issue tracker](https://github.com/ColinDuquesnoy/QDarkStyleSheet/issues)

Contributing to QDarkStyle
--------------------------

The recommended way for new contributors to submit code to QDarkStyle is to
fork the repository on GitHub and then submit a pull request after
committing the changes.  The pull request will then need to be approved by one
of the manteiners before it is merged into the main repository.

- Check for open issues or open a fresh issue to start a discussion around a
    feature idea or a bug.
- Fork [the repository](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
    on GitHub to start making your changes to the **master** branch.
- Write a test which shows that the bug was fixed or that the feature works
    as expected if its a function, or create a screenshot if you are changing
    the stylesheet evidencing the changes.
- Send a pull request and bug the maintainer until it gets merged and
    published. Make sure to add yourself to
    [AUTHORS](https://github.com/ColinDuquesnoy/QDarkStyleSheet/blob/master/AUTHORS.md)
    and the change(s) to
    [CHANGES](https://github.com/ColinDuquesnoy/QDarkStyleSheet/blob/master/CHANGES.md).


Getting Started
---------------

These are the basic steps needed to start developing on QDarkStyle.

- Create an account on GitHub.

- Fork the main
    [QDarkStyle repository](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
    using the GitHub interface.

- Clone the forked repository to your machine.
    ```bash
       git clone https://github.com/USERNAME/qdarkstyle
       cd qdarkstyle
    ```

- Checkout the appropriate branch.
    ```bash
       git checkout master
    ```

- Setup a virtual environment (highly recommended).
    This is not necessary for unit testing, thanks to `tox`, but it is
    necessary if you wish to run ``sphinx-build`` locally or run unit tests
    without the help of ``tox``. ::
    ```bash
       virtualenv ~/.venv
       . ~/.venv/bin/activate
       pip install -e .
    ```

- Create a new working branch. Choose any name you like.
    ```bash
       git checkout -b feature-xyz
    ```

- Its yout time.
    For tips on working with the code, see the `Coding Guide` and Code Style.

- Test, test, test.

   Testing is best done through ``tox``, which provides a number of targets and
   allows testing against multiple different Python environments:

#. Please add a bullet point to :file:`CHANGES` if the fix or feature is not
   trivial (small doc updates, typo fixes).  Then commit::

       git commit -m '#42: Add useful new feature that does this.'

   GitHub recognizes certain phrases that can be used to automatically
   update the issue tracker.

   For example::

       git commit -m 'Closes #42: Fix invalid markup in docstring of Foo.bar.'

   would close issue #42.

#. Push changes in the branch to your forked repository on GitHub. ::

       git push origin feature-xyz

#. Submit a pull request from your branch to the respective branch (``master``
   or ``stable``) on ``sphinx-doc/sphinx`` using the GitHub interface.

#. Wait for a core developer to review your changes.


Coding Guide
------------

* Try to use the same code style as used in the rest of the project.  See the
  `Pocoo Styleguide`__ for more information.

  __ http://flask.pocoo.org/docs/styleguide/

* For non-trivial changes, please update the :file:`CHANGES` file.  If your
  changes alter existing behavior, please document this.

* New features should be documented.  Include examples and use cases where
  appropriate.  If possible, include a sample that is displayed in the
  generated output.

* When adding a new configuration variable, be sure to document it and update
  :file:`sphinx/quickstart.py` if it's important enough.

* Use the included :program:`utils/check_sources.py` script to check for
  common formatting issues (trailing whitespace, lengthy lines, etc).

* Add appropriate unit tests.


Logging
-------

Inside modules we provided a logging that should be used to inform the user.

Please, follow the levels bellow.

* debug: for debug information, high detailed one, directed to programers.
* info: something important for common user to know.
* warning: something that should net be a big problem or a desicision changed.
* error: some error, but not capable of stop program.
* critical: something that stops the running program.



Guide to QDarkStyle
-------------------

The Qt documentation is a good start:

http://doc.qt.io/qt-5.9/stylesheet.html
http://doc.qt.io/qt-5/stylesheet-reference.html

Now you can use our example to work on the stylesheet, it has all possible
widget provided by Qt - common ones. Feel free to add more to them.

To simplify the structure, there are some separated files in
[example.ui](https://github.com/user/repo/blob/branch/other_file.md) folder.

* `dw_buttons.ui`: all types of buttons;
* `dw_displays.ui`: all types of displays;
* `dw_inputs_fields.ui`: all types of inputs with fields;
* `dw_inputs_no_fields.ui`: all types of inputs without fields;
* `mw_views_widgets_containers.ui`: all types of views, widgets, containers and menus.

Obs.: `dw` stands for dock widget and `mw` for main window. The entire example is
built at runtime, in
[example.py](https://github.com/ColinDuquesnoy/QDarkStyleSheet/blob/master/example/example.py).

Feel free to modify `.ui` files with Qt Designer and recompile UI using scripts
inside script folder:

```bash
python process_ui.py
```

It will generate all `_ui.py` files for PyQt4, PyQt5, PySide, QtPy, PyQtGraph.

If you change just the
[stylesheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet/blob/master/qdarkstyle/style.qss)
, to changes be applyed to qrc, recompile the stylesheet using:

```bash
python process_qrc.py
```

This generates all `_rc.py` files for PyQt4, PyQt5 and PySide.


Unit Testing and Fix Preview
----------------------------

It is a good practice, if you are writing functions to QDarkStyle or fix
something related to those functions (not style), that you provide a test
for it. This will keep our implementation stable.

If you are fixing somethng about style, please, provide an screenshot
before and after the fix to comparison. This could be inserted in the issue
tracker, as a message.
