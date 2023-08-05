class Action:
    def __init__(self, name, setup, teardown):
        self.name = name
        self.setup = setup
        self.teardown = teardown


all_actions = {}
history = []

def register(name, setup, teardown):
    """
    **Arguments**
    name        action identifier
    setup       function that conducts the action
    teardown    function that rolls back the action
    """
    action = Action(name, setup, teardown)
    if name not in all_actions:
        all_actions[name] = action
    else:
        raise "'{}' action already registered!".format(name)

def push(name, *args, **kwargs):
    history.append({
        'name': name,
        'args': args,
        'kwargs': kwargs,
    })
    all_actions[name].setup(*args, **kwargs)

def pop():
    if len(history) > 0:
        action = all_actions[history[-1]['name']]
        action.teardown()
    else:
        print('[WARN] Nothin to pop')
