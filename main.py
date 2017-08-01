#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import webapp2
import logging
import os
import json
import urllib
import urllib2

jinja_environment = jinja2.Environment(loader= jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/results.html')
        base_url = "http://api.eventful.com/json/events/search?app_key=dTJDKdL9vWFkMrwQ"
        #remember to add code to make more than 10 events &page_size=100
        url = base_url + "&location=" + str(self.request.get("location")) + "&category=" +str(self.request.get("category"))
        event_data_source= urllib2.urlopen(url)
        print "-===-=-=-=-=--==--="
        print event_data_source
        print "-=-=-===--==-=-=-=-"
        event_json_content = event_data_source.read()
        parsed_event_dictionary = json.loads(event_json_content)
        listOfEvents = parsed_event_dictionary["events"]["event"]
        i = 0
        s = ""
        event_title_list = []
        global_event_dictionary = {}
        # event_info = {}
        for event in listOfEvents:
            event_title_list.append(listOfEvents[i]["title"])
            # # event_info("url") = urllib.quote(listOfEvents[i]["url"].encode("utf-8"))
            # # event_info("venue_url") = urllib.quote(listOfEvents[i]["venue_url"].encode("utf-8"))
            # if listOfEvents[i]["image"] is not None:
            #     event_info("url") = urllib.quote(listOfEvents[i]["image"]["small"]["url"].encode("utf-8"))
            #     event_info("url") = urllib.quote(listOfEvents[i]["image"]["medium"]["url"].encode("utf-8"))
            #     event_info("url") = urllib.quote(listOfEvents[i]["image"]["thumb"]["url"].encode("utf-8"))
            # if listOfEvents[i]["performers"] is not None:
            #     for perform in listOfEvents[i]["performers"]["performer"]:
            #         event_info("url") = urllib.quote(perform["url"].encode("utf-8"))
            # global_event_dictionary[listOfEvents[i]["title"]] = listOfEvents[i]
            i += 1

        event_dictionary = {"eventTitles": event_title_list, "global" : global_event_dictionary}
        # i = 0
        # s = ""
        # for event in listOfEvents:
        #
        #     s += "Title: "
        #
        #     if listOfEvents[i]["title"] is not None:
        #         s+= listOfEvents[i]["title"]
        #     else:
        #         s += "No title given"
        #
        #     s += "<br>"
        #     s += "Description: "
        #
        #     if listOfEvents[i]["description"] is not None:
        #         s += listOfEvents[i]["description"]
        #     else:
        #         s += "No description given"
        #
        #     s += "<br>"
        #     s += "Venue name:"
        #
        #     if listOfEvents[i]["venue_name"] is not None:
        #         s += listOfEvents[i]["venue_name"]
        #     else:
        #         s += "No venue given"
        #
        #     s += "<br>"
        #     s += "image"
        #
        #     if listOfEvents[i]["image"] is not None:
        #         s += "<img src = " + listOfEvents[i]["image"]["medium"]["url"] + ">"
        #     else:
        #         s += "<img src = /resources/No_image_available.png>"
        #
        #     s += "<br><br>"
        #     i+=1
        self.response.write(template.render(event_dictionary))

class EventInfo(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/event_specifics.html')
        s = self.request.get('global')
        print s
        self.response.write(s)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/event_specifics', EventInfo)
], debug=True)
