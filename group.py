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


    class Abelian(Group):

        def __init__(self, operation, members, identity) -> None:
            super().__init__(operation, members, identity)
