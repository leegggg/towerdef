from batt import adb, getScreen, activityPart, checkSsim
import time
import os
from PIL import Image

threshold = 0.8


class Runner():
    def __init__(self):
        self.conf = {}

    def adbShell(self, cmd, sleep=1):
        fullCmd = "{} shell {}".format(adb, cmd)
        res = os.system(fullCmd)
        time.sleep(sleep)
        print("{} {}".format(res, fullCmd))
        return res

    def unlock(self):
        res = 0
        res = res + self.adbShell("input keyevent 26")
        res = res + self.adbShell("input touchscreen swipe 380 2061 380 1000")
        res = res + self.adbShell('input text "{}"'.format(self.conf.get("passwd", "aaa")))
        res = res + self.adbShell("input tap 910 1740")
        return res

    def card(self):
        cap = getScreen().crop(activityPart)
        tplPath = "./data/tpl/lockedTmp.png"
        tpl = Image.open(tplPath)
        part = (0, 0, 1, 1)
        likeness = checkSsim(cap, tpl, part)
        res = 0
        if likeness > threshold:
            print("Locked {}".format(likeness))
            res += self.unlock()
        print("Unlocked")
        res += self.adbShell("monkey -p com.alibaba.android.rimet -c android.intent.category.LAUNCHER 1")
        time.sleep(self.conf.get("keep_running", 10))
        res += self.adbShell("am force-stop com.alibaba.android.rimet")
        return res

    def run(self):
        import json
        with open('./data/conf.json') as f:
            self.conf = json.load(f)
        
        retry = self.conf.get("retry", 5) + 1
        for i in range(1, retry):
            print("try {} / {}".format(i, retry-1))
            res = self.card()
            if res == 0:
                break
            sleep = self.conf.get("sleep", 300)
            print("Failed wait {}s".format(sleep))
            time.sleep(sleep)
        else:
            exit(res)


if __name__ == "__main__":
    runner = Runner()
    runner.run()
