class MDatabase:
    db = {}
    state = False
    def __init__(self, host,port, db, user, password ):
        self.db['host'] = host
        self.db['db']= db
        self.db['user'] = user
        self.db['password'] = password

    def isConnected(self):
        return self.state
    
    def setConnected(self, connected):
        self.state = connected

    



