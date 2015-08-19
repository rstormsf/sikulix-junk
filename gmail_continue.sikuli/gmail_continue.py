import os
import subprocess
import sys
import org.sikuli.basics.SikulixForJython
from sikuli import *
from datetime import datetime
from com.mongodb import *
from com.mongodb.client.model import *
from org.bson import *

load('sikulixapi.jar')
load("mongo-java-driver-3.0.0-rc1.jar")
ImagePath.add("E:\\repos\\sikulix-scripts\\gmail_continue.sikuli\\.")

Debug.setDebugLevel(3)
m = MongoClient("10.0.2.2")
db = m.getDatabase("test")
coll = db.getCollection("krug_accounts")


#click("add_a_photo.png")
#click("select_a_photo_from_you_computer.png")

#type("E:\\repos\\sikulix-scripts\\gmail_reg.sikuli\\01.jpg")
#type(Key.ENTER)
#click("set_as_profile_photo.png")
#click("create_your_profile.png")
#click("continue_to_gmail.png")
#5#click("Next.png")
#click("Go_to_gmail.png")
#click("Gmail_Team.png")
#click("Inbox.png")
#click("icon_smartphone.png")
#click("icon_education.png")
#click("icon_addFriend.png")
#click("icon_picture.png")
#click("icon_notification.png")
#2click("icon_close_notification.png")
#click("icon_notification2.png")
#click("Social_subitem.png")
#click("Google_team_inbox.png")
#click("Inbox.png")

def take_snapshot():
  m = MongoClient("localhost")
  db = m.getDatabase("test")
  coll = db.getCollection("krug_accounts")
# get id vs that nasty check
  user = coll.find(Filters.and(Filters.exists("ImageUrl"), Filters.exists("snapshot", True), Filters.eq("GmailExists", True) )).first()
  email = user["EmailAddress"]
  current_snapshot = user["snapshot_count"]
  new_snapshot = email + "-" + str(current_snapshot + 1)
  # print user.toJson()

  coll.updateOne(Filters.eq("EmailAddress", email), Document("$set", Document("snapshot_count", current_snapshot + 1)))
  # subprocess.check_call(["VBoxManage", "snapshot", "win7-2 Clone", "restore", email])
  subprocess.check_call(["VBoxManage", "snapshot", "win7-2 Clone", "take", new_snapshot, "--live"])















