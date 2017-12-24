

class Di(Object):

    def __init__(self):
        Di.Redis = null

    def getRedis(self):
        return Di.Redis 

    def getMongoDb(self)
        if Di.MongoDb:
            return Di.MongoDb
        else:
            Di.MongoDb = MongoDb()
        return Di.MongoDb