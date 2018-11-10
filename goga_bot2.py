#!/usr/bin/env python3

import time
import pygame
import pygame.camera
from telegram import ChatAction, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
import configparser
import minimalmodbus
import serial.tools.list_ports


mb = None
minimalmodbus.BAUDRATE = 115200
minimalmodbus.TIMEOUT = 3
minimalmodbus.PARITY = 'N'
slave_address = 1

blue = True
white = True
red = True
green = True
yellow = True

def FindDevice():
    global mb

    for p in list(serial.tools.list_ports.comports()):
        if (p.vid == 0x0403) and (p.pid == 0x6015):
        #if (p.vid == 0x1b5c) and (p.pid == 0x0104):
            mb = minimalmodbus.Instrument(str(p.device), slave_address, mode='rtu')
            if not mb.serial.is_open:
                mb.serial.open()
            print('Device Found!')
            return True
    
    return False


class Photographer():

    def __init__(self, device, resolution, pic):
        self.device = device
        self.resolution = resolution
        self.pic = pic
        self.photo_count = 0
        self.lastday = ""

    def recalculate_photo_count(self):

        current_time = time.localtime()
        today = current_time.tm_mday

        if self.lastday:

            if today > self.lastday:
                print("%s: now is a new day, \
                       resetting the count..." % time.asctime())
                self.lastday = today
                self.photo_count = 0

            else:
                print("%s: now is not a new day" % time.asctime())
                self.photo_count += 1

        else:
            print("%s: script started, so lastday is today" % time.asctime())
            self.lastday = today
            self.photo_count += 1

        print(self.photo_count)

    def start(self, bot, update):

        custom_keyboard = [["/blue"],["/white"],["/red"],["/green"],["/yellow"]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        msg = "Это мигалка светодиодами."
        bot.send_message(chat_id=update.message.chat_id,
                         text=msg, reply_markup=reply_markup)

    def send_photo_blue(self, bot, update):

        global blue

        mb.write_bit(8,blue, functioncode=0x05)


        blue = not blue

        def make_shot():
            pygame.camera.init()
            cam = pygame.camera.Camera(self.device,
                                       tuple(map(int,
                                                 self.resolution.split('x'))))
            cam.start()
            #time.sleep(1)  # need to play with it
            img = cam.get_image()
            pygame.image.save(img, self.pic)
            cam.stop()

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.UPLOAD_PHOTO)

        make_shot()
        photo = open(self.pic, 'rb')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
        self.recalculate_photo_count()

    def send_photo_white(self, bot, update):

        global white

        mb.write_bit(9,white, functioncode=0x05)


        white = not white

        
        def make_shot():
            pygame.camera.init()
            cam = pygame.camera.Camera(self.device,
                                       tuple(map(int,
                                                 self.resolution.split('x'))))
            cam.start()
            #time.sleep(3)  # need to play with it
            img = cam.get_image()
            pygame.image.save(img, self.pic)
            cam.stop()

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.UPLOAD_PHOTO)

        make_shot()
        photo = open(self.pic, 'rb')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
        self.recalculate_photo_count()

    def send_photo_red(self, bot, update):

        global red

        mb.write_bit(10,red, functioncode=0x05)


        red = not red
        def make_shot():
            pygame.camera.init()
            cam = pygame.camera.Camera(self.device,
                                       tuple(map(int,
                                                 self.resolution.split('x'))))
            cam.start()
            #time.sleep(3)  # need to play with it
            img = cam.get_image()
            pygame.image.save(img, self.pic)
            cam.stop()

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.UPLOAD_PHOTO)

        make_shot()
        photo = open(self.pic, 'rb')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
        self.recalculate_photo_count()

    def send_photo_green(self, bot, update):

        global green

        mb.write_bit(11,green, functioncode=0x05)


        green = not green
        def make_shot():
            pygame.camera.init()
            cam = pygame.camera.Camera(self.device,
                                       tuple(map(int,
                                                 self.resolution.split('x'))))
            cam.start()
            #time.sleep(3)  # need to play with it
            img = cam.get_image()
            pygame.image.save(img, self.pic)
            cam.stop()

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.UPLOAD_PHOTO)

        make_shot()
        photo = open(self.pic, 'rb')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
        self.recalculate_photo_count()

    def send_photo_yellow(self, bot, update):

        global yellow

        mb.write_bit(12,yellow, functioncode=0x05)


        yellow = not yellow
        def make_shot():
            pygame.camera.init()
            cam = pygame.camera.Camera(self.device,
                                       tuple(map(int,
                                                 self.resolution.split('x'))))
            cam.start()
            #time.sleep(3)  # need to play with it
            img = cam.get_image()
            pygame.image.save(img, self.pic)
            cam.stop()

        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.UPLOAD_PHOTO)

        make_shot()
        photo = open(self.pic, 'rb')
        bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
        self.recalculate_photo_count()

    def send_statistic(self, bot, update):

        message = "За сегодняшний день Игоря хотели увидеть " \
                  "столько раз: %d" % self.photo_count
        bot.send_message(chat_id=update.message.chat_id, text="За сегодняшний день Игоря хотели увидеть " \
                                                              "столько раз: %d" % self.photo_count)


def read_config(config_file):

    config = configparser.ConfigParser()
    config.read(config_file)

    return {'token':       config['bot']['token'],
            'device':      config['camera']['device'],
            'resolution':  config['camera']['resolution']}


def main():

    config = read_config('bullfinch_igor_bot.cfg')

    FindDevice()

    mb.write_bit(0,1, functioncode=0x05)
    mb.write_bit(1,1, functioncode=0x05)
    mb.write_bit(2,1, functioncode=0x05)
    mb.write_bit(3,1, functioncode=0x05)
    mb.write_bit(4,1, functioncode=0x05)
    mb.write_bit(5,1, functioncode=0x05)
    mb.write_bit(6,1, functioncode=0x05)
    mb.write_bit(7,1, functioncode=0x05)

    token = config['token']
    device = config['device']
    resolution = config['resolution']

    pic = '/tmp/igor/igor.jpg'

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    photographer = Photographer(device, resolution, pic)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", photographer.start))
    dp.add_handler(CommandHandler("blue", photographer.send_photo_blue))
    dp.add_handler(CommandHandler("white", photographer.send_photo_white))
    dp.add_handler(CommandHandler("red", photographer.send_photo_red))
    dp.add_handler(CommandHandler("green", photographer.send_photo_green))
    dp.add_handler(CommandHandler("yellow", photographer.send_photo_yellow))

    #dp.add_handler(CommandHandler("stat", photographer.send_statistic))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()