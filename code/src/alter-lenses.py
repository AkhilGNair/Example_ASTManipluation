import ast
import astor
import yaml
from lenses import lens

with open("src/models/original.py") as f:
    original = f.read()

with open("yaml/5.yaml") as f:
    table = yaml.load(f)

# A simple filter predicate
def is_init(node):
    if node.name == "__init__":
        return node


# Return an assign node for an init function
def init_assign(prop):
    return ast.Assign(
        targets=[ast.Attribute(value=ast.Name(id="self"), attr=prop)], value=ast.Name(id=prop)
    )


# Return an argument node
def init_arg(prop):
    return ast.arg(arg=prop, annotation=None)


# Load the original file into AST
tree = ast.parse(original)

# Dive into tree
for_each_module_body = lens.body & lens.Each()
for_each_class_body = lens.body & lens.Each()
function_body = lens.body
function_args = lens.args

# Filter for only init functions
is_init_function = lens.Filter(is_init)

# Compose previous optics to zoom in on the module's init function
init_function = for_each_module_body & for_each_class_body & is_init_function

# Construct node diff set
current_properties = (init_function & function_body & lens.Each().value.id).collect()(tree)
extra_properties = [k for k, v in table.items() if k not in current_properties]
extra_args = [init_arg(property_) for property_ in extra_properties]
extra_assign_nodes = [init_assign(property_) for property_ in extra_properties]

# Splice the new nodes into the tree
tree_ = ((init_function & function_body) + extra_assign_nodes)(tree)
new_tree = ((init_function & function_args & lens.args) + extra_args)(tree_)

print(astor.to_source(new_tree))
