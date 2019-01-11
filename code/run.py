import yaml

from src.models.original import Klass as OldKlass

with open("yaml/2.yaml") as f:
    old = OldKlass(**yaml.load(f))

print(old)

from src.models.new import Klass as NewKlass

with open("yaml/5.yaml") as f:
    new = NewKlass(**yaml.load(f))

print(new)
