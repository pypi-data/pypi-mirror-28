__all__ = ['fituple']


class fituple(tuple):
    """
    Tuple with fast O(1) index and __contains__ methods (at the expense of
    memory footprint)

    """
    def __init__(self, iterable):
        self._mapping = {v: i for i, v in enumerate(self)}

    def index(self, value):
        try:
            return self._mapping[value]
        except KeyError:
            raise ValueError('tuple.index(x): x not in tuple')
        
    def __contains__(self, value):
        return value in self._mapping
