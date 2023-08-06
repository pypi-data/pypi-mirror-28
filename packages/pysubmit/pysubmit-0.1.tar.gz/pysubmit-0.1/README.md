# PySubmit

The versatile computation submission tool.

## Purpose

Scientists who use computational methods often face the problem to test
various parameter values as input for their numerical codes.

Having the power of high performance computer clusters (HPCs) at hand,
it is easy to test up to multiple thousand input parameter values
simultaneously. However, HPCs typically use batch systems that schedule
computation jobs so that special files called start scripts are required
to get your computation running. These start scripts are even useful
for computations on your local workstations.

This tool enables to generate these start scripts with ease and for
arbitrary interfaces to your numerical code. The parameters are supplied
using Python and a boilerplate of your start script that needs to be
filled with values.

## Installation

TODO: Pip and setuptools.

Copy the file ```examples/pysubmitrc``` to your folder ```~/.pysubmitrc```. This
file serves as configuration file for PySubmit.

## Workflow

To generate start scripts with PySubmit, all you need to do is to write
down your desired '''template'''.

1. You write down your boilerplate start script. The values for input
   parameters use the Jinja2 templating syntax and look like this:
   "{{variable}}".
2. You write down a Python function that returns a list with tuples
   in the format: '''(filename, context)''' where '''context''' is a
   dictionary that assigns values to the variables that you use in
   your boilerplate. The following code would be a valid output of
   such a function that generates a start script called **test&#46;sh**
   with the **variable** being set to **42**.
```python
    [ ("test.sh", {"variable": 42}) ]
```
3. Create a folder using your template's desired name and store it
   in your ```{templates}``` directory. Put the boilerplate as ```boilerplate```
   and the function as ```{name}/render.py/render()``` in there. The
   trick of ```__name__=="__main__"``` can be used to debug your function.
4. Call PySubmit to generate the template in ```{output}```

```sh
$ python pysubmit.py generate {name} [-sum]
```

More examples can be found in ```examples/```.

* Start script template
* Write the start script to folder (for backup)
* use qsub straight away; including checking with $?
* "-sim" flag to simulate the submission
* "-view" (or so) flag to view the start scripts
* "-save" flag to save the start scripts to disk only
* forward cli to template and make them dependant on the chosen template
* Option to only execute existing scripts or only save new ones w/o execution

## Implementation

* Write a CLI setup process: Set all the config data.


INSTALLATION
