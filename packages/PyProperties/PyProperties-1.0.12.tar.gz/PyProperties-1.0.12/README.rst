PyProperties
===================

install
-------------------

python -m pip install PyProperties

usage
-------------------

There are two main methods in **PyProperties**, **load** and **save**, both take a properties's file path as parameter.

load
*******************
**load** method is in most circumstances redundant, for the __init__ of **PyProperties** has already called it when you parse a path to it.

**load** method parses the properties file's key-values into the **PyProperties** object.
::

  properties = PyProperties(os.path.abspath('./') + '/resources/test.properties')

or call it directly, and do not forget, **load** will erase current **PyProperties** object.
::

  properties = PyProperties()
  properties.load(os.path.abspath('./') + '/resources/test.properties')

save
*******************

**save** method save current **PyProperties** object to the parameter path.

remember nothing will happened if one of current **PyProperties** is empty or path parameter is **None**
::

  properties.save(os.path.abspath('./') + '/resources/test_1.properties')

read and write properties
****************************

The **PyProperties** object is a like dict object, you can use it as every dict object if you may.

You can use
::

  properties['key_wa']

to read key_wa

and you can use
::

  properties['key_wa'] = '123'

to write new value of key_wa.

most importantly, call
::

  properties.save(path)

to save your properties in the file system.
