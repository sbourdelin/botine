#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

class CEventManager:

    def __init__(self):
        self.eventList = {}     # dict of handler list for event


    def register_handler(self, event, handler, priority = 0):
        """ add an handler to an event """

        # if this type of event is not already used
        if not event in self.eventList:
            # we create a new list to register its handlers
            self.eventList[event] = []
        
        # add the new handler to this type of event
        self.eventList[event].append(handler)
