import sys
import re

def generate_list(tokens):
    if not tokens:
        return []

    token = tokens.pop(0)

    if token == '(':
        nested = []
        while tokens[0] != ')':
            nested.append(generate_list(tokens))
        
        tokens.pop(0)
        return nested
    else:
        return token

def tokenize(data):
    tokens = re.findall(r'[()]|l|\.|[a-zA-Z0-9]+', data)
    return generate_list(tokens)


def main():
    with open(sys.argv[1]) as f:
        data = f.read()

    print(data)

    tokens = tokenize(data)

    print(tokens)

if __name__ == "__main__":
    main()