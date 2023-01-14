class v128:
    def __init__(self, v):
        self._val = [x for x in v]
    def __str__(self):
        return '('+" ".join([str(x) for x in self._val])+')'

