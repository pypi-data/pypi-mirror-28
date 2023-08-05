# -*- coding: utf-8 -*-
#                ____             ____             ____
#  ----     /\   |     *  |    *  |     | /   _*   |
#  |___|   / \   |     |  |    |  |     |/     |   |
#  |___   /  \   |__|  |  |    |  |___  |\     |   |___
#  |   | /---\      |  |  |    |     |  | \    |      |
#  ---- /    \   ___|  |  |__  |  ___|  |  \ __|   ___|
"""
python webkit
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2017 by lich666dead.
:license: GNU GENERAL PUBLIC LICENSE, see LICENSE for more details.
"""

from os import popen
from json import loads
from abc import ABCMeta, abstractmethod


class Basilisk(object):
    '''
    This_abstract_class_with_the_basic_methods_for_generating_the_qc_file.
    :method get: method_for_the_get_query
    :method post: method_for_the_post_query
    '''

    core = True

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, url):
        pass

    @abstractmethod
    def post(self, url, data):
        pass


class PhantomJS(Basilisk):

    def __init__(self, **kwargs):
        '''
        :param kwargs: query_parameters
        :param __js: full_js
        :param __include: js_lib
        :param __slots__: all_parameters_are_in___slots__
        '''

        self.__js = ''

        self.__include = ''

        self.__slots__ = {
            'url': '',
            'image_size': {
                'width': 1920,
                'height': 1080
            },
            'add_cookie': {},
            'screenshot': False,
            'image_name': 'BasiliskJS.png',
            'content': False,
            'get_cookies': False,
            'user_agent': False,
            'load_images': False,
            'command': 'phantomjs ',
            'conversion': 1,
            'post_data': {},
            'method': 'GET',
            'load_finished_fun': '',
            'load_started_fun': '',
            'open_fun': '',
            'resource_error': False,
        }

        self.__slots__.update(kwargs)

    @staticmethod
    def __create_node(data):
        '''
        :param data: Main_settings
        :param necessary: create_page_object
        :param request: request_generation
        :param image_size: image_generation_size
        :param add_cookie: custom_cookie
        :param load_images: loading_image_on_page
        :param param: simple_options
        :param load_finished: end_of_page_load_event
        :param load_started: start_of_page_load_event
        :param resource_error: resource_load_failover_event
        :param url_changed: shift_event_url
        :param node: finished_file
        :return: node
        '''

        necessary = "const webPage" \
                    "=require('webpage');" \
                    "const page=" \
                    "webPage.create();" \
                    "var data = {};" \
                    "var k = 0;" \
                    "var url = [];"

        if data['screenshot']:
            screenshot = "page.render" \
                         "('%s');" % data['image_name']
        else:
            screenshot = ""

        if data['content']:
            content = "data['content'] =page.content;"
        else:
            content = ""

        if data["method"].upper() == "GET":
            request = "page.open( '%s'," \
                      "function(status){" \
                      "data['status']=" \
                      "status;" \
                      "%s" \
                      "%s});" % (
                          data["url"], content,
                          data["open_fun"]
                      )

        elif data["method"].upper() == "POST":
            request = "var postBody = %s;" \
                      "page.open('%s'," \
                      "'POST', postBody," \
                      "function(status){" \
                      "data['status'] = status;" \
                      "%s" \
                      "%s});" % (
                          data["post_data"],
                          data["url"],
                          content,
                          data["open_fun"]
                      )
        else:
            raise AttributeError

        image_size = "page." \
                     "viewportSize=" \
                     "%s;" % str(data["image_size"])

        if data["add_cookie"]:
            add_cookie = "phantom." \
                         "addCookie" \
                         "(%s);" % str(data["add_cookie"])
        else:
            add_cookie = ""

        if data["load_images"]:
            data["load_images"] = "true"
        else:
            data["load_images"] = "false"

        if data['get_cookies']:
            cookies = "data['cookies'] = page.cookies;"
        else:
            cookies = ""

        if data['user_agent']:
            user_agent = "page.settings." \
                         "userAgent=" \
                         "'%s';" % data['user_agent']
        else:
            user_agent = ""

        load_images = "page." \
                      "settings." \
                      "loadImages=" \
                      "%s;" \
                      "%s;" % (
            data["load_images"],
            user_agent
        )

        param = "{0}{1}{2}".format(image_size, add_cookie, load_images)

        load_finished = "page.onLoadFinished=" \
                        "function(){" \
                        "if (k==%i) {" \
                        "data['urls'] = url;" \
                        "%s" \
                        "console.log(JSON.stringify(data));" \
                        "%s" \
                        "phantom.exit();" \
                        "}%s};" % (
                            data["conversion"],
                            cookies,
                            screenshot,
                            data["load_finished_fun"]
                        )

        load_started = "page.onLoadStarted=" \
                       "function() {" \
                       "%s};" % data["load_started_fun"]

        if data["resource_error"]:
            resource_error = "page.onResourceError=" \
                             "function(resourceError) {" \
                             "data['error']=" \
                             "resourceError;" \
                             "};"
        else:
            resource_error = ""

        url_changed = "page.onUrlChanged=" \
                      "function(targetUrl) {" \
                      "k += 1;" \
                      "url.push(targetUrl);" \
                      "};"

        node = "{0}{1}{2}{3}{4}{5}{6}".format(
            necessary, param, request,
            load_finished, load_started,
            resource_error, url_changed
        )

        with open('run.js', 'w') as n:
            n.write(node)

    @staticmethod
    def run(command):
        '''
        this_method_launches_the_phantomjs_browser
        :param command: this_parameter_is_
        responsible_for_the_presence_of_the_phantomjs_browser
        :return: dict
        '''
        with popen(command + ' run.js') as j:
            for i in j.read().split('\n'):
                try:
                    return loads(i)
                except Exception:
                    continue

    def evaluate(self, js):
        '''
        :param js:full_js_script
        :return: function_js_script
        '''
        self.__js = "data['js']=page.evaluate(" \
                    "function() {" \
                    "%s" \
                    "});" % js

    def include_js(self, js):
        '''
        :param js: java_script_library
        :return: function_js
        '''
        self.__include += "page.includeJs" \
                          "('%s');" % js

    def get(self, url):
        """
        :param url: url_for_request
        :return: result_dict
        """
        self.__slots__['url'] = url

        self.__slots__['method'] = 'GET'

        self.__slots__['open_fun'] = "{0}{1}".format(
            self.__js, self.__include
        )

        if self.core:
            self.__create_node(self.__slots__)
            self.core = False
        return self.run(self.__slots__['command'])

    def post(self, url, data):
        '''
        collects_a_post_query
        :param url: url_for_request
        :return: result_dict
        '''
        self.__slots__['url'] = url

        self.__slots__['method'] = 'POST'

        self.__slots__['post_data'] = data

        self.__slots__['open_fun'] = "{0}{1}".format(
            self.__js, self.__include
        )

        if self.core:
            self.__create_node(self.__slots__)
            self.core = False
        return self.run(self.__slots__['command'])
