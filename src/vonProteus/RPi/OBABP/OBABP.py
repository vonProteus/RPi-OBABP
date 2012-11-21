'''
Created on Nov 21, 2012

@author: proteus
'''
import RPi.GPIO as GPIO
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
from time import sleep
import os
import pyudev


class OBABP(object):
    '''
    classdocs
    '''


    def __init__(self,):
        '''
        Constructor
        '''
        self.setPort('6600');
        self.setHost('localhost');
        self.client = MPDClient();
       
        
    
    def setLed(self, _led):
        self.led = _led;
    
    def setButton(self, _button):
        self.button = _button;
    
    def setPort(self, _port):
        self.port = _port;
    
    def setHost(self, _host):
        self.host = _host;
        
    def setDriveName(self, _driveName):
        self.driveName = _driveName;
        
    def setMountPoint(self, _mountPoint):
        self.mountPoint = _mountPoint;
        
    def setMusicDir(self, _musicDir):
        self.musicDir = _musicDir;
    
    def setMpdTagCasche(self, _mpdTagCasche):
        self.mpdTagCasche = _mpdTagCasche;
    
    def connectMPD(self):
        try:
            con_id = {'host':self.host, 'port':self.port}
            self.client.connect(**con_id)
        except SocketError:
            return False
        return True
    
    def satupGPIO(self, mode):
        GPIO.cleanup();
        GPIO.setmode(mode);
        GPIO.setup(self.led, GPIO.OUT);
        GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        
    
    def flashLED(self, speed, time):
        for x in range(0, time):
            GPIO.output(self.led, GPIO.LOW)
            sleep(speed)
            GPIO.output(self.led, GPIO.HIGH)
            sleep(speed)
    
    def loadMusic(self, device):
        os.system("mount "+device+" "+self.mountPoint);
        os.system("/etc/init.d/mpd stop");
        os.system("rm "+self.musicDir+"*");
        os.system("cp "+self.mountPoint+"* "+self.musicDir);
        os.system("umount "+self.mountPoint);
        os.system("rm "+self.mpdTagCasche);
        os.system("/etc/init.d/mpd start")
        os.system("mpc clear")
        os.system("mpc ls | mpc add")
        os.system("/etc/init.d/mpd restart")
    
    def updateLED(self):
        # adjust LED to actual state
        if self.client.status()["state"] == "play":
            GPIO.output(self.led, GPIO.LOW)
        else:
            GPIO.output(self.led, GPIO.HIGH)


    def checkForUSBDevice(self):
        res = ""
        context = pyudev.Context()
        for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
                if device.get('ID_FS_LABEL') == self.driveName:
                        res = device.device_node
        return res
    
    def buttonDown(self):
        if GPIO.input(self.button) == True:
            return True;
        else:
            return False;
    def playPause(self):
        if self.client.status()["state"] == "stop":
            self.client.play();
        else:
            self.client.pause();
    
    
    def go(self):
        if self.connectMPD():
            print "connection: ok";
        else:
            print "connection: error";
        
        print self.client.status();

        timebuttonisstillpressed = 0
        
        self.flashLED(0.1, 10);
        self.updateLED();
        
        while True:
            pendrive = self.checkForUSBDevice();
            if pendrive != "":
                self.flashLED(0.1, 5);
                self.client.disconnect();
                self.loadMusic(pendrive);
                self.connectMPD();
                print self.client.status();
                self.flashLED(0.05, 10)
                while self.checkForUSBDevice() == pendrive:
                    sleep(0.1);
                self.flashLED(0.1, 5);
            if self.buttonDown():
                if timebuttonisstillpressed == 0:
                    self.playPause();
                    self.updateLED();
                if timebuttonisstillpressed > 4:
                    self.client.previous();
                    self.flashLED(0.1, 5);
                    timebuttonisstillpressed = 0;
                timebuttonisstillpressed = timebuttonisstillpressed + 0.1;
            else:
                timebuttonisstillpressed = 0;
            sleep(0.1)

        
        return 1;
    