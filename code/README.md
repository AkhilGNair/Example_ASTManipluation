# AST Manipulation Example

Example repo showing show to do some simple AST manipulation.

The script `alter.py` with pick up the keys in `yaml/5.yaml` and print to stdout the code defined in `src/models/original.py`, where the class definition will have the additional property constructers defined in the `yaml`.

For example, for the yaml

```
✔ ~/sandbox/jsonschema/example
11:48 $ cat yaml/5.yaml
a: hi
b: there
c: this
d: is
e: yaml
```

and the original class definition

```
✔ ~/sandbox/jsonschema/example
11:50 $ cat src/models/original.py
class Klass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        p = ", ".join(prop for prop in self.__dir__() if not prop.startswith("_"))
        return f"My props are {p}"
```

We can run

```
python src/alter.py src/modules/original.py
```

To output

```
✔ ~/slides/jsonschema/example
11:51 $ python src/alter.py src/modules/original.py
class Klass:

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def __repr__(self):
        p = ', '.join(prop for prop in self.__dir__() if not prop.
            startswith('_'))
        return f'My props are {p}'
```

If like me, when you use a `for` loop in python to indent code you lose, check out `src/alter-lenses.py`, where the same results are achieved in using a functional library.