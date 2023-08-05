from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from ..exceptions import Http400Exception, Http404Exception, Http409Exception

# TODO host, port, ssl, login, password from config file
client = MongoClient(connect=False)


class MongoDB:
    def __init__(self):
        # TODO from config file
        self.db = client["wiri"]

    def getMany(self, collection, offset=0, limit=0, sort=None, match=None, projects=None):
        if projects is None:
            projects = []
        if match is None:
            match = {}

        if projects:
            pipeline = [{"$match": match}]
            if offset:
                pipeline.append({"$skip": offset})
            if limit:
                pipeline.append({"$limit": limit})
            # pipeline.append({"$lookup": {"from": rightField, "localField": rightField, "foreignField": "_id", "as": rightField}})
            for project in projects:
                pipeline.append({"$project": project})
            if sort:
                pipeline.append({"$sort": dict(sort)})

            return list(self.db[collection].aggregate(pipeline))
        else:
            data = list(self.db[collection].find(match, skip=offset, limit=limit, sort=sort))

            for row in data:
                if "_id" in row:
                    row["uuid"] = row.pop("_id")

            return data

    def get(self, collection, identifier, key="_id", match=None):
        if match is None:
            match = {}

        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        match[key] = identifier
        data = self.db[collection].find_one(match)

        if data:
            if "_id" in data:
                data["uuid"] = data.pop("_id")
            return data
        else:
            raise Http404Exception()

    def getleftJoin(self, collection, identifier, rightField, key="_id", projects=None):
        if projects is None:
            projects = []

        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        data = self._leftJoin(collection, {key: identifier}, rightField, projects)

        if data:
            data = data.pop()
            if "_id" in data:
                data["uuid"] = data.pop("_id")
            return data
        else:
            raise Http404Exception()

    def getManyleftJoin(self, collection, match, rightField, offset=0, limit=0, sort=None, projects=None):
        if projects is None:
            projects = []

        data = self._leftJoin(collection, match, rightField, projects, offset, limit, sort)

        for row in data:
            if "_id" in row:
                row["uuid"] = row.pop("_id")

        return data

    def getleftJoinMany(self, collection, identifier, rightField, key="_id", projects=None):
        if projects is None:
            projects = []
        pass

    def getManyleftJoinMany(self, collection, offset=0, limit=0, sort=None, projects=None):
        if projects is None:
            projects = []

        pass

    def _leftJoin(self, collection, match, rightField, projects=None, offset=0, limit=0, sort=None):
        if projects is None:
            projects = []

        pipeline = [{"$match": match}]
        if offset:
            pipeline.append({"$skip": offset})
        if limit:
            pipeline.append({"$limit": limit})
        pipeline.append({"$lookup": {"from": rightField, "localField": rightField, "foreignField": "_id", "as": rightField}})
        for project in projects:
            pipeline.append({"$project": project})
        if sort:
            pipeline.append({"$sort": dict(sort)})

        return list(self.db[collection].aggregate(pipeline))

    def post(self, data, collection):
        try:
            return self.db[collection].insert_one(data).inserted_id
        except errors.DuplicateKeyError:
            raise Http409Exception("Already registered")

    def patch(self, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        self.db[collection].update_one({key: identifier}, {'$set': data})

    def patchMany(self, data, collection, mongofilter):
        self.db[collection].update_many(mongofilter, {'$set': data})

    def put(self, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        self.db[collection].replace_one({key: identifier}, data, True)

    def delete(self, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        self.db[collection].delete_one({key: identifier})


Db = MongoDB()
