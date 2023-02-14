from group import Binary

type = "u64"

def mul(first, second):
    return int("{0:64b}".format(first * second), 2)

def add(first, second):
    return int("{0:64b}".format(first + second), 2)

members = []

# the maximum 64 bit unsigned integer
for member in range(18446744073709551615):
    members.append(member)

multiplicative_group = Binary(
    mul, 
    members,
    1, 
    data_type="u64", 
    symbol="*"
)

additive_group = Binary(
    add, 
    members,
    1, 
    data_type="u64", 
    symbol="*"
)

multiplicative_group.generate_table()
additive_group.generate_table()

multiplicative_group.synthesize_logic(verbose=True, simplify=True)
additive_group.synthesize_logic(verbose=True, simplify=True)