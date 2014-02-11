#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

class CParrot:

    def __init__(self, EventManager):
        self.plugin_name    = "parrot"
        self.plugin_version = "0.1"

        EventManager.register_handler("pubmsg", self.on_pubmsg)


    def get_info(self):
        return str(self.plugin_name + " " + self.plugin_version) 


    def on_pubmsg(self, server, event):
        msg_data = event.arguments[0]
        msg_chan = event.target

        server.privmsg(msg_chan, msg_data)
