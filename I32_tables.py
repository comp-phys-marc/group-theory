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

# the maximum 32 bit signed integer
for member in range(2147483647):
    pair = [member]
    # TODO: calculate the mod n inverse using the extended euclidian algorithm or other for each number
    # pair.append(inverse)

    # TODO: account for negatively signed numbers
    members.append(pair)

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