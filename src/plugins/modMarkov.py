#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

MARKOV_DB   = 'markov.db'
NULLWORD    = '\n'
MAXGEN      = 50
SAVECOUNT   = 1

import os
import pickle
import random

class CMarkov:

    def __init__(self, EventManager):
        self.plugin_name    = 'markov'
        self.plugin_version = '0.1'

        # TODO: channel independant db
        self.database       = MARKOV_DB
        self.dico           = self._open_db()
        self.savecounter    = 0

        EventManager.register_handler("pubmsg", self._on_pubmsg)


    def get_info(self):
        return str(self.plugin_name + " " + self.plugin_version) 


    def _on_pubmsg(self, server, event):
        msg_data    = event.arguments[0]
        msg_chan    = event.target
        msg_author  = event.source.nick

        # is someone talking to me ?
        if server.get_nickname() in msg_data:
             # strip my nickname from msg
            msg = str.replace (msg_data, server.get_nickname(), '')
            msg = str.replace (msg, ':', '')
            msg = str.split (msg)
            try:
                msg_answer = str.strip(self._msg_gen(msg[0], msg[1]))
            except:
                msg_answer = str.strip(self._msg_gen())

            # send the answer
            server.privmsg(msg_chan, msg_author + " " + msg_answer)

        else:
            self._msg_add(msg_data)


    def _open_db(self):
        print("--> Loading Database : " + self.database)

        if not os.path.exists(self.database):
            f = open(self.database, 'wb')
            f.close()

        f = open(self.database, 'rb')

        is_eof = f.readline()
        if len(is_eof) == 0:
            dico = {}
        else:
            f.seek(0)
            dico = pickle.load(f)

        f.close()

        return dico


    def _msg_add (self, msg):
        word1, word2 = NULLWORD, NULLWORD
        wordList = msg.split()

        for word3 in wordList:
            # key not present, init with empty
            if not ((word1,word2)) in self.dico:
                self.dico[(word1,word2)] = []
            # Add suffix for word pair
            self.dico[(word1,word2)].append(word3)
            # Shift the windows on next word
            word1,word2 = word2,word3

        # Mark end
        self.dico[(word1,word2)] = [NULLWORD]
        # Store in file when we have SAVECOUNT new entry
        self.savecounter += 1
        if self.savecounter >= SAVECOUNT:
            pickle.dump(self.dico, open(self.database, 'wb'))


    def _msg_gen (self, word1=NULLWORD, word2=NULLWORD):
        # first two word start our message
        message = word1 + " " + word2

        # find association with this word
        # and go to the association with word2 & newword
        # repeat until MAXGEN or no association find
        for i in range(MAXGEN):
            sucessorList = self.dico[(word1,word2)]
            word3 = random.choice(sucessorList)
            if word3 == NULLWORD:
                break
            message = message + " " + word3
            word1,word2 = word2, word3

        return message
 

    def _nb_entry (self):
        return len(self.dico)

