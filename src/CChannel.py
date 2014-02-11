#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

PLUGINS_DIR     = "./plugins"
CMD_HANDLER     = 0
CMD_MESSAGE     = 1

import imp
import os
import CBot
import CEventManager

class CChannel:

    def __init__(self, name, plugins = None):
        self.EventManager   = CEventManager.CEventManager()
        self.name           = name
        self.plugins        = plugins
        self.cmd            = { '!help'     : [self.cmd_help, "display this help message"],
                                '!version'  : [self.cmd_version, "show the bot version number"],
                                '!plugin'   : [self.cmd_plugin, "list the plugins used in this channel"]
                            }

        # this handler is used for all the control bot message send on a channel
        self.EventManager.register_handler('pubmsg', self.on_pubmsg)

        # activate the channel plugins
        self.load_plugins()

        
    def dispatch_event(self, server, event):
        """ the event dispatcher have to loop over the
            event type that had been register in the EventManager
            and call their respectives callbacks.
        """

        if event.type in self.EventManager.eventList:
            handlerList = self.EventManager.eventList[event.type]

            for handler_ in handlerList:
                handler_(server, event)


    def load_plugins(self):
        """ loop over the global plugin list and
            activate all the plugins selected for this channel.
        """
        
        if self.plugins :
            # for each plugins that must be activated for this channel
            for plugin_ in self.plugins:
                # if the plugin name exist in the global plugin list
                if plugin_ in CBot.pluginList:
                    # we execute the plugin and send him our event manager 
                    # to register its callback to this channel
                    CBot.pluginList[plugin_](self.EventManager)


    def on_pubmsg(self, server, event):
        """ we are covering the channel message used
            to control the bot here.
        """

        msg_data    = event.arguments[0]
        msg_author  = event.source.nick

        if self.is_cmd(msg_data):
            self.cmd_parser(server, msg_data, msg_author)


    def is_cmd(self, data):
        """ we are considering that if message is beginning
            by the character '!', its a command message.
        """

        return data.startswith('!')

    
    def cmd_parser(self, server, cmd, author):
        """ here we know we are on a command
            so we have to call the command handler.
        """
        
        if cmd in self.cmd:
            self.cmd[cmd][CMD_HANDLER](server, author)


    def cmd_help(self, server, author):
        """ send the help message in private message
            to the nickname that was asking for.
        """

        for cmd in self.cmd:
            server.privmsg(author, cmd + ':\t\t' + self.cmd[cmd][CMD_MESSAGE])


    def cmd_plugin(self, server, author):
        """ send the number of plugins load for this channel
            and list them.
        """
        
        server.privmsg(author, "This channel used " + str(len(self.plugins)) + " plugins")

        if len(self.plugins) > 0:
            for plugin_ in self.plugins:
                server.privmsg(author, plugin_)


    def cmd_version(self, server, author):
        """ send the bot version number.
        """

        server.privmsg(author, "botine v2.0")
