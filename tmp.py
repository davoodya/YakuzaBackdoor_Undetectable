import subprocess
import os
import win32api
TMP = os.environ['APPDATA']

vbOkOnly = "0"
vbInformation = "64"
vbSystemModal = "4096"

def MessageBox(message):
    objVBS = open(TMP + "/m.vbs", "w")

    objVBS.write(f'MsgBox "{message}", {vbOkOnly} + {vbInformation} + {vbSystemModal}, "Message"')   # noqa
    objVBS.close()

    subprocess.Popen(['cscript', TMP + "/m.vbs"], shell=False)

MessageBox('hello')
