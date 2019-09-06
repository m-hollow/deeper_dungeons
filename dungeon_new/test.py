class Foo:
    def __init__(self):
        print("I have made a foo.")
        self.foo = { "foo": "this is a newly initialized foo" }

    def mutate(self):
        self.foo = { "bar": "this is a mutated foo with a bar instead of a foo.foo.foo" }

def checkFoo(state):
    print("Foo is: '{0}' with foo attribute {1}".format(state['foo'], state['foo'].foo))

def changeFoo(state):
    state['foo'] = Foo()

state = {}

state['foo'] = Foo()
checkFoo(state)

state['foo'].mutate()
checkFoo(state)

changeFoo(state)
checkFoo(state)

