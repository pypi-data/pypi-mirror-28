#!/usr/bin/env python3
# vim: set fenc=utf8 ts=4 sw=4 et :
import sys
import argparse
import xml.sax
import imp
import inspect

from os import path
from pkg_resources import iter_entry_points, resource_filename
from shutil import copytree

from .logging import *
from .conf import Conf
from .plugin import *
from .pdmlhandler import PdmlHandler

def pdml2flow():
    parser = argparse.ArgumentParser(description='Aggregates wireshark pdml to flows')
    parser.add_argument('-f',
                        dest='FLOW_DEF_STR',
                        action='append',
                        help='Fields which define the flow, nesting with: \'{}\' [default: {}]'.format(Conf.FLOW_DEF_NESTCHAR, Conf.FLOW_DEF_STR)
                        )
    parser.add_argument('-t',
                        type=int,
                        dest='FLOW_BUFFER_TIME',
                        help='Lenght (in seconds) to buffer a flow before writing the packets [default: {}]'.format(Conf.FLOW_BUFFER_TIME)
                        )
    parser.add_argument('-l',
                        type=int,
                        dest='DATA_MAXLEN',
                        help='Maximum lenght of data in tshark pdml-field [default: {}]'.format(Conf.DATA_MAXLEN)
                        )
    parser.add_argument('-s',
                        dest='EXTRACT_SHOW',
                        action='store_true',
                        help='Extract show names, every data leaf will now look like {{ raw : [] , show: [] }} [default: {}]'.format(Conf.EXTRACT_SHOW)
                        )
    parser.add_argument('-x',
                        dest='XML_OUTPUT',
                        action='store_true',
                        help='Switch to xml output [default: {}]'.format(Conf.XML_OUTPUT)
                        )
    parser.add_argument('-c',
                        dest='COMPRESS_DATA',
                        action='store_true',
                        help='Removes duplicate data when merging objects, will not preserve order of leaves [default: {}]'.format(Conf.COMPRESS_DATA)
                        )
    parser.add_argument('-a',
                        dest='FRAMES_ARRAY',
                        action='store_true',
                        help='Instead of merging the frames will append them to an array [default: {}]'.format(Conf.FRAMES_ARRAY)
                        )
    parser.add_argument('-m',
                        dest='METADATA',
                        action='store_true',
                        help='Appends flow metadata [default: {}]'.format(Conf.METADATA)
                        )
    parser.add_argument('-d',
                        dest='DEBUG',
                        action='store_true',
                        help='Debug mode [default: {}]'.format(Conf.DEBUG)
                        )
    parser.add_argument('-p',
                        dest='PLUGIN_LOAD',
                        action='append',
                        help='Plguins to load, installed: {} [default: {}]'.format([str(ep).split(' =',1)[0] for ep in iter_entry_points(group=Conf.PLUGIN_GROUP)], Conf.PLUGIN_LOAD)
                        )
    parser.add_argument('-0',
                        dest='PRINT_0',
                        action='store_true',
                        help='Terminates lines with null character [default: {}]'.format(Conf.PRINT_0)
                        )
    conf = vars(parser.parse_args(args=Conf.ARGS))
    # split each flowdef to a path
    if conf['FLOW_DEF_STR'] is not None:
        conf['FLOW_DEF'] = Conf.get_real_paths(conf['FLOW_DEF_STR'], Conf.FLOW_DEF_NESTCHAR)

    # load plugins
    conf['PLUGINS'] = []
    if conf['PLUGIN_LOAD'] is not None:
        for plugin_name in conf['PLUGIN_LOAD']:
            for entry_point in iter_entry_points(group=Conf.PLUGIN_GROUP, name=plugin_name):
                plugin = entry_point.load()
                if inspect.isclass(plugin) and not plugin in Conf.SUPPORTED_PLUGIN_INTERFACES and any([
                    issubclass(plugin, supported_plugin_interface)
                        for supported_plugin_interface in Conf.SUPPORTED_PLUGIN_INTERFACES
                    ]):
                    conf['PLUGINS'].append(plugin())
    start_parser(conf)

def pdml2xml():
    Conf.XML_OUTPUT = True
    pdml2frame('xml')

def pdml2json():
    pdml2frame('json')

def pdml2frame(output_type):
    parser = argparse.ArgumentParser(description='Converts wireshark pdml to {}'.format(output_type))
    Conf.DATA_MAXLEN = sys.maxsize
    Conf.FLOW_BUFFER_TIME = 0
    Conf.FLOW_DEF_STR = [ 'frame.number' ]
    Conf.FLOW_DEF = Conf.get_real_paths(Conf.FLOW_DEF_STR, Conf.FLOW_DEF_NESTCHAR)
    parser.add_argument('-s',
                        dest='EXTRACT_SHOW',
                        action='store_true',
                        help='Extract show names, every data leaf will now look like {{ raw : [] , show: [] }} [default: {}]'.format(Conf.EXTRACT_SHOW)
                        )
    parser.add_argument('-d',
                        dest='DEBUG',
                        action='store_true',
                        help='Debug mode [default: {}]'.format(Conf.DEBUG)
                        )
    conf = vars(parser.parse_args(args=Conf.ARGS))
    start_parser(conf)

def start_parser(conf = {}):
    # apply configuration
    Conf.set(conf)
    # print config
    for name, value in Conf.get().items():
        debug('{} : {}'.format(name, value))
    try:
        xml.sax.parse(Conf.IN, PdmlHandler())
    except xml.sax._exceptions.SAXParseException as e:
        # this might happen when a pdml file is malformed
        warning('Parser returned exception: {}'.format(e))
        handler.endDocument()

def pdml2flow_new_plugin():
    print(resource_filename(__name__, '/plugin-skeleton'))

    parser = argparse.ArgumentParser(
        description='Initializes a new plugin'
    )
    parser.add_argument(
        'dst',
        type=str,
        nargs='+',
        help='Where to initialize the plugin, basename will become the plugin name'
    )
    conf = vars(parser.parse_args(args=Conf.ARGS))
    for dst in conf['dst']:
        plugin_name = path.basename(dst)
        copytree(
            resource_filename(__name__, '/plugin-skeleton'),
            dst
        )
