class Entity(object):
    def __init__(self, value):
        self.successors = set()
        self._value = value

    def __repr__(self):
        return f'E({self._value})'

    def dependents(self):
        breadcrumb = object()
        for constraint in self.successors:
            constraint.check_cycles(breadcrumb)

        def h(constraint):
            constraint._hits -= 1
            if constraint._hits > 0: return
            yield constraint
            for succ in constraint.target.successors:
                yield from h(succ)

        for constraint in self.successors:
            yield from h(constraint)

    def update(self, value):
        self._value = value
        for constraint in self.dependents():
            constraint.fire()


class CycleException(Exception):
    pass


class Constraint(object):

    def __init__(self, preds: list[Entity], target: Entity):
        self.predecessors = preds
        self.target = target
        for pred in self.predecessors:
            pred.successors.add(self)
        self._breadcrumb = None
        self._entered = False
        self._hits = 0

    def __str__(self):
        return f'{self.predecessors} -> {self.target}'

    def check_cycles(self, breadcrumb):
        if self._breadcrumb is not breadcrumb:
            self._hits = 0
            self._entered = False
            self._breadcrumb = breadcrumb
        if self._entered:
            raise CycleException()
        self._hits += 1
        if self._hits == 1:
            self._entered = True
            for c in self.target.successors:
                c.check_cycles(breadcrumb)
            self._entered = False

    def fire(self):
        self.target._value = sum(pred._value for pred in self.predecessors)


def detach_constraint(constraint: Constraint):
    for entity in constraint.predecessors:
        entity.successors.remove(constraint)


if __name__ == '__main__':
    entities = [Entity(name) for name in range(10)]
    a1 = Entity('A1')
    b1 = Entity('B1')
    a2 = Entity('A2')
    b2 = Entity('B2')
    a3 = Entity('A3')
    b3 = Entity('B3')
    a4 = Entity('A4')
    b4 = Entity('B4')
    constraints = [
        Constraint([b1], a2),
        Constraint([a2, b2], b3),
        Constraint([b3], a4),
        Constraint([a3, b3], b4),
        Constraint([a1, b1], b2),
        Constraint([b2], a3),
        # Constraint([b4], a1)
    ]
    a1.update('1')
    b1.update('0')
    for constraint in b1.dependents():
        print(constraint)
