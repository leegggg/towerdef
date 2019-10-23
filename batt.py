import os
import time
from PIL import Image
from PIL.Image import Image as PILImg
from skimage.io._plugins import pil_plugin
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
import random

adb = "C:\\Users\\yizho\\platform-tools\\adb.exe"
tempFileDevice = "/sdcard/screencaptmp.png"
tempFileHost = "./data/screencaptmp.png"
tempResizedFileHost = "./data/screencapresized.png"

# landscape 
deviceSize = (2340, 1080)
activityPart = (76, 244, 1127, 835)
threshold = 0.8

# portrait 
deviceSize = (1080, 2340)
activityPart = (0, 297, 1080, 905)
threshold = 0.6

# portrait q
deviceSize = (1080, 2340)
activityPart = (67, 75, 1013, 607)
threshold = 0.6

# activitySize = (1051, 591)

def getScreen():
    os.system("{} shell screencap -d 0 -p {}".format(adb, tempFileDevice))
    os.system("{} pull {} {} > ./data/nul".
              format(adb, tempFileDevice, tempFileHost))
    im = Image.open(tempFileHost)
    im = im.resize(deviceSize)
    im.save(tempFileHost)
    debugSave(im)
    return im


def checkSsim(cap: PILImg, tpl: PILImg, loc):
    box = (
        int(loc[0]*tpl.size[0]),
        int(loc[1]*tpl.size[1]),
        int(loc[2]*tpl.size[0]),
        int(loc[3]*tpl.size[1])
    )
    cap = cap.resize(tpl.size).crop(box).convert("L")
    tpl = tpl.crop(box).convert("L")
    #cap.show()
    #tpl.show()
    likeness = ssim(pil_plugin.pil_to_ndarray(cap),
                    pil_plugin.pil_to_ndarray(tpl))
    return likeness


def click(loc):
    x = int(
        (loc[0]+loc[2])/2*(activityPart[2]-activityPart[0])
        + activityPart[0]
    )
    y = int(
        (loc[1]+loc[3])/2*(activityPart[3]-activityPart[1])
        + activityPart[1]
    )
    cmd = "{} shell input tap {}  {}".format(adb, x, y)
    # print(datetime.now())
    print(cmd)
    os.system(cmd)
    pass


def debugSave(im):
    im.save("./data/debug/debug-full-{}.png".
            format(int(datetime.now().timestamp()))
            )
    im.crop(activityPart).save(
        "./data/debug/debug-act-{}.png".
        format(int(datetime.now().timestamp()))
    )


def paly(replay=False,bossIndex=-1):
    cap = getScreen().crop(activityPart)
    # start
    tplPath = "./data/tpl/menuTmp.png"
    replayPart = (787/1051, 524/591, 856/1051, 568/591)
    battlePart = (932/1051, 525/591, 1008/1051, 561/591)
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, replayPart)
    if likeness > threshold:
        print("Menue {} DEFEATED: {}".format(likeness, replay))
        if bossIndex >= 0:
            # Boss Black
            dist = 95
            click((514/1051, 189/591, 514/1051, 189/591))
            click((947/1051, 130/591+bossIndex*dist/591, 947/1051, 130/591+bossIndex*dist/591))
            click((947/1051, 130/591+bossIndex*dist/591, 947/1051, 130/591+bossIndex*dist/591))
            return

        if replay:
            click(replayPart)

        click(battlePart)
        return

    # Drop Down Boss
    part = (325/1051, 413/591, 730/1051, 485/591)
    tplPath = "./data/tpl/dropTpl.png"
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, part)
    if likeness > threshold:
        print("Drop down {}".format(likeness))
        # GET
        click((627/1051, 451/591, 627/1051, 451/591))
        return

    # replayChoosePart
    replayChoosePart = (651/1051, 516/591, 837/1051, 569/591)
    tplPath = "./data/tpl/replayChooseTpl.png"
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, replayChoosePart)
    if likeness > threshold:
        print("ReplayChoose {}".format(likeness))
        click(replayChoosePart)
        return

    # DEFEATED
    part = (445/1051, 81/591, 740/1051, 266/591)
    tplPath = "./data/tpl/dftTpl.png"
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, part)
    if likeness > threshold:
        print("DEFEATED {}".format(likeness))
        return True

    # play
    # part = (960/1051, 512/591, 1024/1051, 573/591)
    part = (25/1051, 521/591, 76/1051, 574/591)
    tplPath = "./data/tpl/playTpl.png"
    hero = (241/1051, 74/591)
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, part)
    if likeness > threshold:
        print("Playing {}".format(likeness))
        part = (817/1051, 9/591, 830/1051, 21/591)
        likeness = checkSsim(cap, tpl, part)
        if likeness > threshold:
            print("Has mema {}".format(likeness))
            for _ in range(3):
                x = hero[0]+random.randint(0, 2)*65/1051
                y = hero[1]+random.randint(0, 3)*77/591
                click((x, y, x, y))
        click((775/1051, 400/591, 775/1051, 400/591))
        return

    # closeMenu
    part = (992/1051, 42/591, 1024/1051, 80/591)
    tplPath = "./data/tpl/closeMenuTpl.png"
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, part)
    if likeness > threshold:
        print("closeMenu {}".format(likeness))
        click(part)
        return

    # closeMenu2
    part = (783/1051, 123/591, 815/1051, 153/591)
    tplPath = "./data/tpl/closeMenu2Tpl.png"
    tpl = Image.open(tplPath)
    likeness = checkSsim(cap, tpl, part)
    if likeness > threshold:
        print("closeMenu2 {}".format(likeness))
        click(part)
        return


    return


def main():
    dft = True
    while True:
        if paly(replay=dft,bossIndex=-1):
            dft = True
        time.sleep(1)


if __name__ == "__main__":
    main()
