#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

import json
import CServer

class CServerList:
    def __init__(self):
        self.servers    = []

        #self.parse_servers()
        self.parse_json()

    def parse_json(self):
        try:
            with open('servers.json') as f:
                json_data = json.load(f)
        except Exception as e:
            print(e)

        # parse servers informations
        if 'server' in json_data:
            for server_ in json_data['server']:

                if not 'name' in server_ or not 'url' in server_ or not 'nickname' in server_:
                    print("error: server name, url, and nickname are mandatory items in server config file")
                    continue

                # server channels
                channels = {}
                if 'channel' in server_:
                    for channel_ in server_['channel']:
                        channels[channel_['name']] = []
                        if 'plugin' in channel_:
                            for plugin_ in channel_['plugin']:
                                channels[channel_['name']].append(plugin_)

                self.servers.append(
                        CServer.CServer(server_.get('name'),
                                    server_.get('url'),
                                    server_.get('port'),
                                    server_.get('nickname'),
                                    server_.get('realname'),
                                    server_.get('password'),
                                    channels,
                                    server_.get('enable'))
                )
