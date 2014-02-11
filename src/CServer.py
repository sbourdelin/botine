#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

import CChannel

class CServer():

    def __init__(self, name, url, port = 6667, nickname = 'botine', realname = 'botine', password = None, channels = None, enable = False):
        self.name       = name
        self.enable     = enable
        self.url        = url
        self.port       = port
        self.nickname   = nickname
        self.realname   = realname
        self.password   = password
        self.channels   = []
        
        self.create_channels(channels)


    def run(self):
        """ start the server connection """

        self.connection.connect(self.url, self.port, self.nickname, self.realname)


    def create_channels(self, channels):
        """ Create channel list """

        for name_ in channels:
            pluginList_ = []

            # Create the plugin list related to this channel
            for plugin_ in channels[name_]:
                pluginList_.append(plugin_.get('name'))

            # Create the new channel
            self.channels.append(
                    CChannel.CChannel(name_, pluginList_)
            )


    def dispatch_event(self, connection, event):
        """ dispatch event used by the server class """

        try :
            {
                'welcome'   : self.on_welcome,
                'pubmsg'    : self.on_pubmsg,
            }[event.type](connection, event)
        # we don't care of the other messages.
        except KeyError:
            return


    def on_welcome(self, connection, event):
        """ welcome message means we are connect to the server
            it's the good time to register our nickname and
            join channel.
        """

        for channel_ in self.channels:
            print("INFO\t-> joining " + channel_.name)
            connection.join(channel_.name)


    def on_pubmsg(self, connection, event):
        """ pubmsg message means a message has been send to a
            channel, we must find the targeting channel and dispatch
            the message to it.
        """

        for chan in self.channels:
            if str.find(event.target, chan.name) != -1:
                chan.dispatch_event(connection, event)
        
    #TODO: def on_privnotice
    # verify nickserv
