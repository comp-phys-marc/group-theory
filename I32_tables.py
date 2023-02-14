from group import Binary

type = "I32"

def mul(first, second):
    res = first * second
    magnitude = "{0:31b}".format(res)
    if res < 0:
        return - int(magnitude, 2)
    else:
        return int(magnitude, 2)

def add(first, second):
    res = first + second
    magnitude = "{0:31b}".format(res)
    if res < 0:
        return - int(magnitude, 2)
    else:
        return int(magnitude, 2)

members = []

for member in range(-2147483647, 2147483647):
    members.append(member)

multiplicative_group = Binary(
    mul, 
    members,
    1, 
    data_type="I32", 
    symbol="*"
)

additive_group = Binary(
    add, 
    members,
    1, 
    data_type="I32", 
    symbol="*"
)

multiplicative_group.generate_table()
additive_group.generate_table()

multiplicative_group.synthesize_logic(verbose=True, simplify=True)
additive_group.synthesize_logic(verbose=True, simplify=True)