from deathbycaptcha import *

client = SocketClient("LOGIN", "PASSWORD")
client.is_verbose = True
DEFAULT_TIMEOUT = 60
print 'Your balance is %s US cents' % client.get_balance()

try:
    # Put your CAPTCHA image file name or file-like object, and optional
    # solving timeout (in seconds) here:
    captcha = client.decode("sdfk.png", DEFAULT_TIMEOUT)
except Exception, e:
    sys.stderr.write('Failed uploading CAPTCHA: %s\n' % (e, ))
    captcha = None

if captcha:
    print 'CAPTCHA %d solved: %s' % \
          (captcha['captcha'], captcha['text'])

#dir = getBundlePath()
#reg = Region(746,676,299,60)
#screen =reg.getScreen().capture(746,676,299,60).getFile(dir, "sdfk")

#screen.capture().getFile(dir, "sdf2")
#img = Image.create(screen.capture())

