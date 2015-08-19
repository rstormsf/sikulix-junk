import os
import subprocess

from com.mongodb import *
from com.mongodb.client.model import *
from org.bson import *

m = MongoClient("localhost")
db = m.getDatabase("test")
coll = db.getCollection("krug_accounts")

user = coll.find(Filters.and(Filters.exists("ImageUrl"), Filters.exists("snapshot", False))).first()
email = user["EmailAddress"]
print email
print user.toJson()

subprocess.check_call(["VBoxManage", "snapshot", "win7-2 Clone", "restore", "prod"])
subprocess.check_call(["VBoxManage", "snapshot", "win7-2 Clone", "take", email, "--live"])

coll.updateOne(Filters.eq("EmailAddress", email), Document("$set", Document("snapshot", True)))
