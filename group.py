import itertools

class Group:

    def __init__(self, operation, members, identity) -> None:
        if operation is not None:
            self.operation = operation
        else:
            raise ValueError("A composition operation must be provided with a Group.")
        if identity is not None:
            self.identity = identity
        else:
            raise ValueError("An identity element must be provided with a Group.")
        if isinstance(members, list):
            self.members = []
            for pair in members:
                if not (isinstance(pair, list) and len(pair) == 2) \
                    or self.operation(*pair) != self.identity \
                        or self.operation(*pair.reverse()) != self.identity:
                    raise ValueError("Group members must be provided in pairs of inverses.")
                if self.operation(pair[0], self.identity) != pair[0] \
                    or self.operation(pair[1], self.identity) == pair[1]:
                    raise ValueError("Group members composed with the identity must not change.")
                self.members += pair

        self.commutative = None
        self.table = {}

    def generate_table(self):
        self.table = {}

        if self.commutative:
            for [first, second] in itertools.combinations(self.members, 2):
                res = self.operation(first, second)
                self.table[res] = [first, second]
        else:
            for [first, second] in itertools.permutations(self.members, 2):
                res = self.operation(first, second)
                self.table[res] = [first, second]


class PseudoGroup:
    """
    Relaxes the constraints of a Group. Useful for solving mod n inverses so that a proper Group can be constructed next.
    """

    def __init__(self, operation, members, identity) -> None:
        if operation is not None:
            self.operation = operation
        else:
            raise ValueError("A composition operation must be provided with a Group.")
        if identity is not None:
            self.identity = identity
        else:
            raise ValueError("An identity element must be provided with a Group.")
        if isinstance(members, list):
            self.members = members

        self.commutative = None
        self.table = {}

    def generate_table(self):
        self.table = {}

        if self.commutative:
            for [first, second] in itertools.combinations(self.members, 2):
                res = self.operation(first, second)
                self.table[res] = [first, second]
        else:
            for [first, second] in itertools.permutations(self.members, 2):
                res = self.operation(first, second)
                self.table[res] = [first, second]


class Abelian(Group):

    def __init__(self, operation, members, identity) -> None:
        super().__init__(operation, members, identity)
        self.commutative = True


class Binary(PseudoGroup):

    def __init__(self, operation, members, identity, data_type=None, symbol="o") -> None:
        super().__init__(self, operation, members, identity)

        self.data_type = data_type
        self.symbol = symbol
        self.expressions = []
        self.minterms = []

    def generate_table(self):
        self.table = {}

        def save_with_type(res, first, second):
            if self.data_type == "I8":
                self.table["{0:08b}".format(res)] = ["{0:64b}".format(first), "{0:64b}".format(second)]
            elif self.data_type == "I32":
                self.table["{0:32b}".format(res)] = ["{0:64b}".format(first), "{0:64b}".format(second)]
            elif self.data_type == "I64":
                self.table["{0:64b}".format(res)] = ["{0:64b}".format(first), "{0:64b}".format(second)]

            # TODO: support more data types

        if self.commutative:
            for [first, second] in itertools.combinations(self.members, 2):
                res = self.operation(first, second)
                if not self.data_type:
                    self.table[res] = [first, second]
                else:
                    save_with_type(res, first, second)
        else:
            for [first, second] in itertools.permutations(self.members, 2):
                res = self.operation(first, second)
                if not self.data_type:
                    self.table[res] = [first, second]
                else:
                    save_with_type(res, first, second)

    def synthesize_logic(self, simplify=False, verbose=False):
        if self.data_type == "I32":
            expressions = [[] for p in range(32)]
            minterms = [[] for p in range(32)]
        elif self.data_type == "I64":
            expressions = [[] for p in range(64)]
            minterms = [[] for p in range(64)]
        elif self.data_type == "I8":
            expressions = [[] for p in range(8)]
            minterms = [[] for p in range(8)]

        # TODO: support more data types

        for (res, operands) in self.table.items():
            for p in range(len(res)):
                if res[p] == "1":
                    boolean_exp = ""
                    j = -1
                    for o in range(2):
                        label = "b"
                        if o == 0:
                           label = "a"
                        for b in operands[o]:
                            j += 1
                            o_bit = f" {label}{j}"
                            if b == "1":
                                if boolean_exp != "":
                                    boolean_exp += f" * {o_bit}"
                                else:
                                    boolean_exp += o_bit
                    if not boolean_exp in expressions[p]:
                        expressions[p].append(boolean_exp)
                        minterms[p].append("".join(operands))

        if verbose:
            for i in range(len(expressions)):
                perm_bit = "c{i} ="
                perm_bit_exps = expressions[i]
                perm_bit_total_exp = perm_bit + " + ".join(perm_bit_exps)
                print(perm_bit_total_exp)

        if simplify:
            expressions, minterms = self._simplify_logic(expressions, minterms, verbose)
        
        self.expressions = expressions
        self.minterms = minterms


    def _simplify_logic(self, expressions, minterms, verbose):
        has_deps = True
        
        while has_deps == True:
            
            has_deps = False
            if self.data_type == "I32":
                dup_dependencies = [[] for p in range(32)]
            elif self.data_type == "I64":
                dup_dependencies = [[] for p in range(64)]
            elif self.data_type == "I8":
                dup_dependencies = [[] for p in range(8)]
            
            for l in range(len(minterms)):
                for term in range(len(minterms[l])):
                    one_term_bits = []
                    for term_bit in range(len(minterms[l][term])):
                        if minterms[l][term][term_bit] == '1':
                            one_term_bits.append(term_bit)
                    for other_minterm in minterms[l][0:term] + minterms[l][term + 1:]:
                        dup = True
                        for bit_index in one_term_bits:
                            if(bit_index > len(other_minterm) or other_minterm[bit_index] == '0'):
                                dup = False
                        if dup == True:
                            if not term in dup_dependencies[l].keys():
                                dup_dependencies[l][term] = [minterms[l].index(other_minterm)]
                            else:
                                dup_dependencies[l][term].append(minterms[l].index(other_minterm))
            
            removal_candidates = [[] for index in range(len(minterms))]
            
            for p in range(len(dup_dependencies)):
                for opt_term_index in dup_dependencies[p].keys():
                    for rm_term in dup_dependencies[p][opt_term_index]:
                        if not rm_term in dup_dependencies[p].keys():
                            if not opt_term_index in removal_candidates[p]:
                                removal_candidates[p].append(rm_term)
            
            # filter optimal expressions
            optimal_expressions = [[] for index in range(len(expressions))]
            optimal_minterms = [[] for index in range(len(minterms))]
            
            removed = 0
            
            for k in range(len(expressions)):
                for q in range(len(expressions[k])):
                    if q in removal_candidates[k]:
                        print('Redundant term {0} removed from c{1} expression'.format(expressions[k][q], k))
                        removed += 1
                        continue
                    optimal_expressions[k].append(expressions[k][q])
                    optimal_minterms[k].append(minterms[k][q])
                    
            expressions = optimal_expressions
            minterms = optimal_minterms
            
            if removed != 0:
                has_deps = True

            if verbose:
                print('pass removed {0} terms'.format(removed))
        
        if verbose: 
            # print optimal expressions
            for e in range(len(expressions)):
                perm_bit = 'c{0} ='.format(e)
                perm_bit_exps = expressions[e]
                perm_bit_total_exp = perm_bit + ' + '.join(perm_bit_exps)
                
                print(perm_bit_total_exp)

        return expressions, minterms