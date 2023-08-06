Jupyjet
=======

Jupyjet is a IPython notebook extension to facilitate:

* [Literate programming](https://en.wikipedia.org/wiki/Literate_programming)
* Separate a big notebook into several smaller notebooks / modules.

Practically speaking, for each notebook a python file is dynamically created:<br>
*ie - it generate python modules based of notebook content.*



Usage
--------

3 magics commands are exposed: `%jet_beg`, `%jet` and `%jet_end`

* **jet_beg**: save all the content of the current cell and place it at the top of the file.<br>
It is supposed to contains imports / global variables.<br>
*NB: Only one init is allowed and it must be the last line of the cell.*

* **jet** decl1 decl2 ...: save or update the declaration in the file.<br>
Classes, function and decorators are supported.<br>
Comments will be stripped.<br>
The file content is updated everytime the magic runs.

* **jet_end**: save all the content of the current cell and place it at the bottom of the file.<br>
It is supposed to contain for example a ifmain block.<br>
*NB: Only one init is allowed and it must be the last line of the cell.*


Example
------------


**my_super_notebook.ipynb**

*Cell 1 - We declare here the header of the file*

```
import numpy as np
pi = 3.14

%jet_beg
```
*And save it as raw content*

<hr>

*Cell 2 - We create a few functions*

```
def circle_perim(r):
	return 2 * pi * r

def circle_area(r):
	return pi * r**2

%jet circle_perm circle_area
```
*And save them*

<hr>

*Cell 3 - in the context of the notebook, we can run some experiement*<br>
*We can then use these functions normally*
```
print circle_perim(2.)
print circle_area(2.2)
```
*The results won't be saved into the file*

<hr>

The coresponding generated file is:

**my_super_notebook.py**
```
import numpy as np
pi = 3.14

# --- JET BEG --- #

def circle_perim():
    return 2 * pi * r


def circle_area():
    return pi * r ** 2


# --- JET END --- #


```

So this python generated module can be called from other notebooks.

*NB: comments are not saved in the genrated files.*


Install
---------
Jupyjet is available on pip:

```
pip install jupyjet
pip3 install jupyjet
```


#### Enable the extension

Here is a small guide to activate the extension.

##### 1. Create a jupyter profile

`$ ipython profile create`

It will generate a default profile file at: `~/.ipython/profile_default/ipython_config.py`.


##### 2. Register Jupyjet as an extension (and other cool ones like [line-profiler](https://github.com/rkern/line_profiler)).

To do so add the following lines.

```
c.TerminalIPythonApp.extensions = [
    'jupyjet',
    'line_profiler',
]
c.InteractiveShellApp.extensions = [
    'jupyjet',
    'line_profiler',
]
```

##### 3. Enjoy =)
