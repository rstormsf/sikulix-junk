#1366x1006
# Install Firefox from ninite.com
# save picture locally
# 
import os
import deathbycaptcha
import subprocess
import sys
import org.sikuli.basics.SikulixForJython
from sikuli import *
from datetime import datetime
from com.mongodb import *
from com.mongodb.client.model import *
from org.bson import *


def solve_captcha(filename):

  client = deathbycaptcha.HttpClient("LOGIN", "PASSWORD")
  # client.is_verbose = True
  DEFAULT_TIMEOUT = 90
  print 'Your balance is %s US cents' % client.get_balance()

  try:
      # Put your CAPTCHA image file name or file-like object, and optional
      # solving timeout (in seconds) here:
      captcha = client.decode(filename + ".png", DEFAULT_TIMEOUT)
  except Exception, e:
      sys.stderr.write('Failed uploading CAPTCHA: %s\n' % (e, ))
      captcha = None

  if captcha:
      print 'CAPTCHA %d solved: %s' % \
            (captcha['captcha'], captcha['text'])
      return captcha['text']

load('sikulixapi.jar')
load("mongo-java-driver-3.0.0-rc1.jar")
ImagePath.add("E:\\repos\\sikulix-scripts\\gmail_reg.sikuli\\.")

GUEST_IP = "10.0.2.2"\

Debug.setDebugLevel(3)
m = MongoClient(GUEST_IP)
db = m.getDatabase("test")
coll = db.getCollection("krug_accounts")

# user = coll.find(Filters.and(Filters.exists("ImageUrl"), Filters.exists("snapshot", False))).first()
user= coll.find(Filters.eq("_id", types.ObjectId(os.environ['ID']))).first()
email = user["EmailAddress"]
print email
print user.toJson()


# click("1429849365038.png")
click("1429849365038.png")
sleep(15)
type("l", Key.CTRL)
type("gmail.com")
type(Key.ENTER)
sleep(15)
click("1429851115779.png")
sleep(15)
click("1429851320547.png")


type(user["GivenName"])
type(Key.TAB)
type(user["Surname"])
type(Key.TAB)
type(user["GmailEmail"])
type(Key.TAB)
type(user["Password"])
type(Key.TAB)
type(user["Password"])
type(Key.TAB)
monthArr = [0, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
birthday = user["Birthday"]
dob = datetime.strptime(birthday, '%m/%d/%Y').date()
type(monthArr[dob.month])
type(Key.TAB)
type(str(dob.day))
type(Key.TAB)
type(str(dob.year))
type(Key.TAB)
type("F")
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type(user["EmailAddress"])
type(Key.TAB)
type(Key.TAB)
reg = Region(818,838,302,62)
dir = "E:\\repos\\sikulix-scripts\\gmail_reg.sikuli\\"
filename = "captcha"
screen =reg.getScreen().capture(818,838,302,62).getFile(dir, filename)
captcha = solve_captcha(dir + filename)
type(captcha)
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type(Key.SPACE)
type(Key.ENTER)
sleep(25)
coll.updateOne(Filters.eq("_id", types.ObjectId(os.environ['ID'])), Document("$set", Document("GmailExists", True)))

#debug
# click("1429849365038.png")
#debug

ImagePath.add("E:\\repos\\sikulix-scripts\\gmail_continue.sikuli\\.")

print user["ImageUrl"]
dowloading_pic = urllib.urlretrieve("http://" + GUEST_IP + ":3000/" + user["ImageUrl"], "E:\\profile_pic.jpg")
print "\n\n downloading is done\n\n"
print dowloading_pic[0]

click("add_a_photo.png")
sleep(25)
click("select_a_photo_from_you_computer.png")
sleep(25)
type("E:\\profile_pic.jpg")
type(Key.ENTER)
sleep(60)
click("set_as_profile_photo.png")
sleep(15)
click("create_your_profile.png")
sleep(20)
click("continue_to_gmail.png")

click("Next.png")
click("Next.png")
click("Next.png")
click("Next.png")
click("Next.png")

sleep(20)

click("Go_to_gmail.png")
sleep(15)
click("Gmail_Team.png")
sleep(15)
click("Inbox.png")
sleep(15)
click("icon_smartphone.png")
sleep(15)
click("icon_education.png")
sleep(15)
click("icon_addFriend.png")
sleep(15)
click("icon_picture.png")
sleep(15)
click("icon_notification.png")
sleep(15)

click("icon_close_notification.png")
click("icon_close_notification.png")
sleep(10)
click("icon_notification2.png")
sleep(10)
click("Social_subitem.png")
sleep(10)
click("Google_team_inbox.png")
sleep(10)
click("Inbox.png")

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

take_snapshot()
