CooDict
=======

This module provides a simple 'copy-on-write' dictionary-like class to allow you to treat an existing dictionary as a 'constant' and only make modifications to a sideways dictionary.

Features
--------

This class behaves almost exactly like a standard dictionary, with a few important differences:

* The class takes 2 arguments - the `base` dictionary, and an `overlay` dictionary (both default to `{}`)
* All modifications (writes, deletes etc) happen to an `overlay` dictionary.
* All reads (`get`, `keys`, `values` etc) come from the results of merging the `overlay` and `base` dictionaries:
  * If a key is in `overlay`, return it.
  * If not, try to return the key in `base`.
  * If the key is marked as deleted in `overlay`, or absent in `base`, `KeyError` is raised.
* `clear()` only empties the `overlay` dictionary. **Note** this will also undo deletions!
* `copy()` returns a copy of the `CooDict` (in the form of a `CooDict` instance).



Example
-------

```
from coodict import CooDict

original_dict = {'animal': 'cat', 'vegetable': 'carrot'}
cd = CooDict(original_dict)

# Make some modifications
cd['animal'] = 'dog'
cd.pop('vegetable')
cd['mineral'] = 'salt'
cd.items()
# results => {'animal': 'dog', 'mineral': 'salt'}

# check the original
original_dict.items()
# results => {'animal': 'cat', 'vegetable': 'carrot'}

# Clear the overlay (note that popped item 'vegetable' reappears).
cd.clear()
cd.items()
# results => {'animal': 'cat', 'vegetable': 'carrot'}

```
