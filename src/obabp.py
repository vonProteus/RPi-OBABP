'''
Created on Nov 21, 2012

@author: proteus
'''
from vonProteus.RPi.OBABP import OBABP
import RPi.GPIO as GPIO

def main():
    obabp = OBABP();
    obabp.setLed(12);
    obabp.setButton(13);
    obabp.setDriveName("1GB");
    obabp.setMountPoint("/mnt/usb/");
    obabp.setMusicDir("/var/lib/mpd/music/");
    obabp.setMpdTagCasche("/var/lib/mpd/tag_cache");
    obabp.satupGPIO(GPIO.BOARD);
    obabp.go();

if __name__ == '__main__':
    main()