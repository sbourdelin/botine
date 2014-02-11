#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sebastien Bourdelin <sebastien.bourdelin@gmail.com>
#

PLUGINS_DIR     = "./plugins"

import imp
import os

class CPluginsManager:

    def __init__(self):
        self.pluginList     = {}    # dict of (plugin name, plugin class)

        self.init_plugins()


    def init_plugins(self):
        # retrieve the absolute plugins directory path
        directory = os.path.abspath(PLUGINS_DIR)

        # for each files in this directory
        for filename in os.listdir(directory):
            # split the file name and its extension
            file_basename, file_ext = os.path.splitext(filename)
            # verify that is a python file
            if file_ext.lower() == '.py':
                try:
                    # load the source file
                    plugin_file = imp.load_source(file_basename, str(directory + '/' + filename))
                    print("Loading plugin : " + file_basename)
                except Exception as e:
                    print(e)
                    return

                # we are checking for each class declare in our plugin
                for class_name in dir(plugin_file):
                    if class_name[:1] == '_' :
                        continue    # hidden classes begin with '_'

                    # retrieve the full class name
                    plugin = getattr(plugin_file, class_name)
                    
                    # verify this is really a class type
                    if isinstance(plugin, type) :
                        # add the load plugin to the plugin list
                        self.pluginList[file_basename] = plugin
