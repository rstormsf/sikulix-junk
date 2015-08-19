import sys
import os
import subprocess
import time

import org.sikuli.basics.SikulixForJython
from sikuli import *
Debug.setDebugLevel(3)
type("r", Key.WIN)
time.sleep(2)
type("firefox.exe")
time.sleep(2)
type(Key.ENTER)
time.sleep(5)
type(Key.ENTER)
type(Key.F4, KeyModifier.ALT)