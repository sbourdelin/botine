#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

import irc.client
import CServerList
import CPluginsManager

pluginList = []

class CBot () :

    def __init__ (self) :

        global pluginList
        pluginList      = CPluginsManager.CPluginsManager().pluginList  # plugins list
        self.serverList = CServerList.CServerList()                     # servers list

        # Create the IRC object
        self.irc = irc.client.IRC()
        self.irc.add_global_handler("all_events", self.dispatch_event, -10)

        self.start()


    def start(self):
        """ start all connection """

        for server_ in self.serverList.servers:

            # we only work with enabled server
            if server_.enable == 0:
                continue

            print("connecting to " + str(server_.name) + " ...")
            server_.connection = self.irc.server()
            server_.run()
            
        # Run an infinite loop
        self.irc.process_forever()


    def dispatch_event(self, server, event):
        """ dispatch all event """

        for server_ in self.serverList.servers:

            # we only work with enabled server
            if server_.enable == 0:
                continue
            
            # dispatch the event to the server concerned
            if str.find(server.get_server_name(), server_.name) != -1:
                server_.dispatch_event(server, event)
