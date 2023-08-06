''' A simple branching utility '''

def branch(condition):
    '''
    A simple curried predicate matcher.
    If the predicate is to be called with args,
    they must be extracted to a HOF by the caller.
    '''
    def inner(truthy_result, falsy_result):
        ''' The returned function '''
        predicate = condition

        if callable(condition):
            predicate = condition()

        if predicate:
            return truthy_result
        return falsy_result

    return inner
