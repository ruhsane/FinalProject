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
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader= jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user:
            greeting = ('(<a href="%s">Sign Out</a>)' % (users.create_logout_url('/signin')))
        else:
            greeting = ('<a href="%s">Sign In</a>' % users.create_login_url('/signin'))

        signin = ('<html><body><section id="WholeTopPart"><div class="top" id="SignIn">%s</div></section></body></html>' % greeting)

        login = {"Signin" : signin}


        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render(login))

    def post(self):
        template = jinja_environment.get_template('templates/results.html')
        base_url = "http://api.eventful.com/json/events/search?app_key=dTJDKdL9vWFkMrwQ&page_size=70"
        #remember to add code to make more than 10 events &page_size=100
        print "--------------"
        print self.request.get("category")
        print "--------------"
        url = base_url + "&location=" + str(self.request.get("location")) + "&category=" +str(self.request.get("category"))
        event_data_source= urllib2.urlopen(url)
        event_json_content = event_data_source.read()
        parsed_event_dictionary = json.loads(event_json_content)
        if parsed_event_dictionary['events'] is not None:
            listOfEvents = parsed_event_dictionary["events"]["event"]
        else:
            listOfEvents = []
            event_dictionary = {
            "error" : "Sorry! No results found."
            }
            self.response.write(template.render(event_dictionary))
        i = 0
        event_title_list = []
        event_id_list = []
        event_title_id = {}
        event_title_venue= {}
        event_category = {}
        for event in listOfEvents:
            event_title_list.append(listOfEvents[i]["title"])#puts all the titles in a list
            event_id_list.append(listOfEvents[i]["id"])#puts all the ids in a list
            event_title_id[listOfEvents[i]["title"]] = listOfEvents[i]["id"]#conencts the title with its id
            event_title_venue[listOfEvents[i]["title"]] = listOfEvents[i]["venue_name"]
            event_category[listOfEvents[i]["title"]] = str(self.request.get("category"))
            i += 1
        event_dictionary = {
            "eventTitleVenue": event_title_venue,
            "eventTitles": event_title_list,
            "eventIds": event_id_list,
            "eventTitleId" : event_title_id
            }
        self.response.write(template.render(event_dictionary))


class EventInfo(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/event_specifics.html')
        base_url = "http://api.eventful.com/json/events/get?app_key=dTJDKdL9vWFkMrwQ&id="
        url = base_url + self.request.get("id") + '&category=' + self.request.get("category")
        specific_event_data_source= urllib2.urlopen(url)
        specific_event_json_content = specific_event_data_source.read()
        parsed_specific_event_dictionary = json.loads(specific_event_json_content)

        event_title = parsed_specific_event_dictionary["title"]
        event_category = parsed_specific_event_dictionary["categories"]["category"][0]["id"]

        event_venue_name = parsed_specific_event_dictionary["venue_name"]

        if "venue_address" in parsed_specific_event_dictionary:
            event_venue_address = parsed_specific_event_dictionary["venue_address"]
        else: event_venue_address = "location not found"

        event_description = parsed_specific_event_dictionary["description"]
        if event_description is None:
            event_description = "No description found"

        if parsed_specific_event_dictionary['start_time'] is None:
            event_start_time= "No start time found"
        else:
            event_start_time = parsed_specific_event_dictionary["start_time"]

        if parsed_specific_event_dictionary['stop_time'] is None:
            event_stop_time= "No stop time found"
        else:
            event_stop_time = parsed_specific_event_dictionary["stop_time"]

        if parsed_specific_event_dictionary["images"] is None:
            event_image_url_medium = "/resources/No_image_available.png"
        else:
            if not parsed_specific_event_dictionary["images"]["image"]["medium"]:
                event_image_url_medium = parsed_specific_event_dictionary["images"]["image"][0]["medium"]["url"]
            else:
                event_image_url_medium = parsed_specific_event_dictionary["images"]["image"]["medium"]["url"]

        event_dict = {
            "title" : event_title,
            "venueName" : event_venue_name,
            "description" : event_description,
            "venueAddress" : event_venue_address,
            "mediumPicURL" : event_image_url_medium,
            "startTime" : event_start_time,
            "stopTime" : event_stop_time
        }
        self.response.write(template.render(event_dict))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/event_specifics', EventInfo)
], debug=True)
