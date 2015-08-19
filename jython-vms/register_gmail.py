import os
import subprocess
import requests
import random
import time
import glob

from com.mongodb import *
from com.mongodb.client.model import *
from org.bson import *
from java.util import Date

def connect_to_db(db_name):
  m = MongoClient("localhost")
  db = m.getDatabase(db_name)
  return db
db = connect_to_db("test")


FFDIR = os.path.dirname(os.path.realpath(__file__)) + "/download.cdn.mozilla.net/pub/mozilla.org/firefox/releases/latest/win32/en-US/"

def download_ff():
  # wget -r -l1 --no-parent -A.exe http://download.cdn.mozilla.net/pub/mozilla.org/firefox/releases/latest/win32/en-US/
  subprocess.check_call(["wget", "-r", "-l1", "--no-parent", "-A.exe", "http://download.cdn.mozilla.net/pub/mozilla.org/firefox/releases/latest/win32/en-US/" ])
  for fl in glob.glob(FFDIR + "Firefox Setup St*"):
    os.remove(fl)
    os.rename(FFDIR + os.listdir(FFDIR)[0], FFDIR + "firefox_setup.exe")

def install_ff():
  scrPath="E:\\repos\sikulix-commands\download.cdn.mozilla.net\pub\mozilla.org\\firefox\\releases\latest\win32\en-US\\firefox_setup.exe -ms" 
  subprocess.check_call(["vboxmanage", 
                        "guestcontrol",
                        "win7-2 Clone",
                        "exec", "--image", "cmd.exe", 
                        "--environment", 
                        "--verbose",
                        "--wait-stdout",
                        "--wait-stderr",
                        "--username",
                        "User",
                        "--password",
                        "5262gagarin",
                        "--",
                        "/c",
                        scrPath])

def run_ff():
  scrPath="jython E:\\repos\sikulix-scripts\\run_ff.sikuli\\run_ff.py"
  subprocess.check_call(["vboxmanage", 
                        "guestcontrol",
                        "win7-2 Clone",
                        "exec", "--image", "cmd.exe", 
                        "--environment", 
                        "--verbose",
                        "--wait-stdout",
                        "--wait-stderr",
                        "--username",
                        "User",
                        "--password",
                        "5262gagarin",
                        "--",
                        "/c",
                        scrPath])

def take_snapshot(snapshot_count, email):
  coll = db.getCollection("krug_accounts")
  subprocess.check_call(["VBoxManage", "snapshot", "win7-2 Clone", "take", email + "-" + str(snapshot_count), "--live"])
  coll.updateOne(Filters.eq("GmailEmail", email), Document("$set", Document("snapshot_count", snapshot_count).append("snapshot", True)))


def check_email(email, append):
  email = email
  print "Checking " + email
  url = 'http://107.170.225.78:3000/' + email + append
  resp = requests.get(url=url)
  data = resp.json()
  status = data['codeBol']
  if status == False:
    newemail = email + str(random.randint(1,100)) 
    return check_email(newemail, append)
  return email



def assign_gmail():
  coll = db.getCollection("krug_accounts")
  cursor = coll.find().iterator()

  while cursor.hasNext():

    user = cursor.next()
    email = user["GivenName"] + user["Surname"]
    gmail = "@gmail.com"
    verified_email = check_email(email, gmail)
    verified_email += gmail
    print verified_email
    coll.updateOne(Filters.eq("_id", user["_id"]), Document("$set", Document("GmailEmail", verified_email)))

def get_ip():

  cmd = "adb shell netcfg | grep UP | tail -1 | cut -d ' ' -f8"
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  ip = ps.communicate()[0].rstrip()
  print "********************************"
  print ip
  print "********************************"

  return ip

def change_ip(old_ip):
  print "starting " + old_ip
  count = 0
  # current activity:
  # adb shell dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'
  #press home
  # cmd = "adb shell input keyevent 3"
  # ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  cmd = "adb shell am start -n com.android.settings/.wimax.WimaxSettings"
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  time.sleep(5)
  times = 1
  while times > 0:
    print "jumping " + str(times)
    cmd = "adb shell input keyevent 19"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT) 
    time.sleep(2)
    times -= 1
  cmd = "adb shell input keyevent 23"
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT) 
  time.sleep(30)
  print "slept 30 sec"
  #going back
  cmd = "adb shell input keyevent 3"
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  cmd = "adb shell am start -n com.koushikdutta.tether/.TetherActivity"
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  ip = get_ip()
  while ip == old_ip and count < 3:
    print "sleeping 1 sec"
    time.sleep(5)
    count += 1
    ip = get_ip()
  if ip == old_ip:
    print "changing ip again"
    change_ip(ip)
  return ip

def get_clean_ip(ip):
  checkingUser = coll.find(Filters.eq("ips", Document("$elemMatch", Document("ip", ip)))).first()
  if checkingUser:
    new_ip = change_ip(ip)
    get_clean_ip(new_ip)
  return ip

def create_gmail():
  ip = check_user_ip(get_ip())
  coll = db.getCollection("krug_accounts")

  # make sure there a user with snapshot
  user = coll.find(Filters.and(Filters.exists("ImageUrl"), Filters.exists("snapshot", False),
      Filters.or(Filters.exists("GmailExists", False), Filters.eq("GmailExists", False)))).first()
  if user:
    # coll.updateOne(Filters.eq("_id", user["_id"]), Document("$unset", Document("ips", Document("ip", ip).append("created", Date()))))
    coll.updateOne(Filters.eq("_id", user["_id"]), Document("$push", Document("ips", Document("ip", ip).append("created", Date() ))))
    print user.toJson()
  # vboxmanage guestcontrol "win7-2 Clone" exec --image "cmd.exe" --environment "EMAIL=BarbaraMJacobson@gustr.com" --verbose --wait-stdout --wait-stderr --username User --password 5262gagarin -- /c $scrPath  

    subprocess.check_call(["VBoxManage", "snapshot", "win7-2 Clone", "restore", "prod_prod"])
    subprocess.check_call(["VBoxManage", "startvm", "win7-2 Clone"])
    id = 'ID=' + str(user["_id"])
    id = "%(id)s" % locals()
    print id
    scrPath="jython E:\\repos\sikulix-scripts\gmail_reg.sikuli\gmail_reg.py"
    subprocess.check_call(["vboxmanage", 
                          "guestcontrol",
                          "win7-2 Clone",
                          "exec", "--image", "cmd.exe", 
                          "--environment", 
                          "%(id)s" % locals(),
                          "--verbose",
                          "--wait-stdout",
                          "--wait-stderr",
                          "--username",
                          "User",
                          "--password",
                          "Password01",
                          "--",
                          "/c",
                          scrPath])
    print "done creating"
    print "**********************************************************************"
    take_snapshot(1, user["GmailEmail"])

download_ff()
install_ff()
run_ff()

