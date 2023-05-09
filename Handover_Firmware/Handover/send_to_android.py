import time
import nfc
import ndef
from threading import Thread
from nfc.clf import RemoteTarget

with nfc.ContactlessFrontend('tty:S0') as clf:
        tag = clf.connect(rdwr={'on-connect': lambda tag: False })
        print(tag)
        for record in tag.ndef.record:
                print(record)
        clf.close()