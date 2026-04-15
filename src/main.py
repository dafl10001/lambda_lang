import sys
import re


counter = 0
def get_fresh():
    global counter
    counter += 1
    return f"v{counter}"


def get_free_vars(expr):
    if isinstance(expr, str):
        return {expr}
    if expr[0] == "LAMBDA":
        return get_free_vars(expr[2]) - {expr[1]}
    res = set()
    for item in expr:
        res.update(get_free_vars(item))
    return res


def substitute(substr, string, expr, free_in_string):
    if isinstance(expr, str):
        return string if expr == substr else expr

    if expr[0] == "LAMBDA":
        var, body = expr[1], expr[2]
        if var == substr: return expr # Shadowed
        
        if var in free_in_string:
            fresh = get_fresh()
            body = substitute(var, fresh, body, [fresh])
            var = fresh
            
        return ["LAMBDA", var, substitute(substr, string, body, free_in_string)]

    return [substitute(substr, string, item, free_in_string) for item in expr]


def reduce(expr):
    while True:
        if isinstance(expr, str):
            return expr

        if isinstance(expr, list) and len(expr) == 2:
            func = reduce(expr[0])
            arg = expr[1]

            if isinstance(func, list) and func[0] == "LAMBDA":
                expr = substitute(func[1], arg, func[2], get_free_vars(arg))
                continue 
            
            return [func, reduce(arg)]

        if expr[0] == "LAMBDA":
            new_body = reduce(expr[2])
            return ["LAMBDA", expr[1], new_body]

        return expr


def parse(tokens):
    for i, tok in enumerate(tokens):
        print(reduce(tok))


def generate_list(tokens):
    token = tokens.pop(0)

    if token == '(':
        exprs = []
        while tokens[0] != ')':
            exprs.append(generate_list(tokens))
        tokens.pop(0)
        
        res = exprs[0]
        for i in range(1, len(exprs)):
            res = [res, exprs[i]]
        return res
    
    elif token == 'l':
        var = tokens.pop(0)
        tokens.pop(0)
        body = generate_list(tokens)
        return ["LAMBDA", var, body]
    
    return token


def tokenize(data):
    tokens = re.findall(r'[()]|l|\.|[a-zA-Z0-9]+', data)
    return generate_list(tokens)


def tree_to_expr(tree):
    if isinstance(tree, str):
        return tree

    if tree[0] == "LAMBDA":
        var = tree[1]
        body = tree_to_expr(tree[2])
        return f"(ʎ{var}.{body})"

    if isinstance(tree, list) and len(tree) == 2:
        left = tree_to_expr(tree[0])
        right = tree_to_expr(tree[1])
        return f"({left} {right})"

    return str(tree)


def main():
    if len(sys.argv) < 2: return
    with open(sys.argv[1]) as f:
        data = f.read().strip()

    tokens = tokenize(data)
    
    exprs = []
    while tokens:
        exprs.append(generate_list(tokens))
    
    if not exprs: return
    tree = exprs[0]
    for i in range(1, len(exprs)):
        tree = [tree, exprs[i]]
    
    print(tree_to_expr(tree) + "\n->\n" + tree_to_expr(reduce(tree)))

if __name__ == "__main__":
    main()