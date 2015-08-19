# vboxmanage guestcontrol "win7-2 Clone" exec --image "cmd.exe" --verbose --wait-stdout --wait-stderr --username User --password 5262gagarin -- /c "jython E:\repos\sikulix-scripts\test.sikuli\test.py"
import sys
import os
import subprocess
import urllib
import time

import org.sikuli.basics.SikulixForJython
from sikuli import *
load('sikulixapi.jar')
load("mongo-java-driver-3.0.0-rc1.jar")
ImagePath.add("C:\\sikulix\\test.sikuli\\.")
from com.mongodb import *
from com.mongodb.client.model import *
from org.bson import *

# Debug.setDebugLevel(3)
m = MongoClient("10.0.2.2")
db = m.getDatabase("test")
coll = db.getCollection("krug_accounts")

user= coll.find(Filters.eq("_id", types.ObjectId(os.environ['ID']))).first()
# user = coll.find(Filters.exists("ImageUrl")).first()
# email = user["EmailAddress"]
# print email
print user.toJson()


ImagePath.add("E:\\repos\\sikulix-scripts\\gmail_continue.sikuli\\.")
GUEST_IP = "10.0.2.2"
print user["ImageUrl"]
her = urllib.urlretrieve("http://" + GUEST_IP + ":3000/" + user["ImageUrl"], "E:\\profile_pic.jpg")
print "\ndone\n"
print time.time()
print her[0]