# BOTLIB - Framework to program bots !!
#
# bot/udp.py
#
# Copyright 2017,2018 B.H.J Thate
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice don't have to be included.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# 9-1-2018 As the creator of this file, I disclaim all rights on  this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" relay txt through a udp port listener. """

from bot import fleet
from bot.obj import Config, Object
from bot.thr import Launcher

import logging
import socket
import time

udp_tpl = Object()
udp_tpl.cfg = "udp"
udp_tpl.host = "localhost"
udp_tpl.port = 5500
udp_tpl.password = "boh"
udp_tpl.seed = "blablablablablaz" # needs to be 16 chars wide
udp_tpl.server = udp_tpl.host
udp_tpl.owner = ""

class UDP(Object):

    """ UDP class to echo txt through the bot, use the mad-udp program to send. """

    def __init__(self):
        super().__init__(self)
        self._stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()

    def start(self, *args, **kwargs):
        """ start the UDP server. """
        lhr = Launcher()
        self.cfg = Config(udp_tpl).fromdisk("udp")
        lhr.launch(self.server)

    def server(self, host="", port="", *args, **kwargs):
        """ main server loop. """
        self._sock.bind((host or self.cfg.host, port or self.cfg.port))
        logging.warn("# udp listening at %s:%s" % (host or self.cfg.host, port or self.cfg.port))
        self.ready()
        while not self._stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self._stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)
        logging.info("! stop udp %s:%s" % (self.cfg.host, self.cfg.port))

    def exit(self):
        """ shutdown the UDP server. """
        self._stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("bla", "utf-8"), (self.cfg.host, self.cfg.port))

    def output(self, txt, addr=None):
        """ output to all bot on fleet. """
        try:
            (passwd, text) = txt.split(" ", 1)
        except:
            return
        text = text.replace("\00", "")
        if passwd == self.cfg.password:
            for bot in fleet:
                bot.announce(text)
