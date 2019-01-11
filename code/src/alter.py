import ast
import astor
import yaml

with open("src/models/original.py") as f:
    original = f.read()

with open("yaml/5.yaml") as f:
    table = yaml.load(f)

tree = ast.parse(original)

current_properties = []
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        if node.name == "__init__":
            for body_node in node.body:
                if isinstance(body_node, ast.Assign):
                    for assign_node in ast.walk(body_node):
                        if isinstance(assign_node, ast.Name):
                            if assign_node.id != "self":
                                current_properties.append(assign_node.id)

# Don't use a generator
extra_properties = [k for k, v in table.items() if k not in current_properties]


def init_arg(prop):
    return ast.arg(arg=prop, annotation=None)


def init_assign(prop):
    return ast.Assign(
        targets=[ast.Attribute(value=ast.Name(id="self"), attr=prop)], value=ast.Name(id=prop)
    )


for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        if node.name == "__init__":
            node.args.args.extend(init_arg(property_) for property_ in extra_properties)
            node.body.extend(init_assign(property_) for property_ in extra_properties)


print(astor.to_source(tree))
