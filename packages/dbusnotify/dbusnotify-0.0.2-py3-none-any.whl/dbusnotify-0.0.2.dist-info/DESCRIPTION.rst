#+TITLE: dbusnotify - freedesktop.org notifications library

* Overview
/dbusnotify/ is a python library for creating desktop notifications using the freedesktop.org notification specification.

* Usage
The following example shows how to create a simple notification with an icon
#+BEGIN_SRC python
  import dbusnotify
  dbusnotify.write(
      'Volume is <u>muted</u>',
      title='Audio Status',
      icon='audio-volume-muted',
      poptime=20,
  )
#+END_SRC

[[file:examples/images/dbusnotify_readme_example.png]]

- [[file:examples][Additional examples]]

* Installation
You can install from pypi using pip
#+BEGIN_SRC sh
pip install --user dbusnotify
#+END_SRC

Alternatively, you can get the development version from github
#+BEGIN_SRC sh
git clone https://github.com/frostidaho/python-dbusnotify.git
pip install --user ./python-dbusnotify
#+END_SRC



