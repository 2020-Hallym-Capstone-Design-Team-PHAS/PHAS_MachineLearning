class Singleton(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super( Singleton, self).__new__(self)
            return self.instance

