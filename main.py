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
        template = jinja_environment.get_template('templates/index.html')
        base_url = "http://api.eventful.com/json/events/search?app_key=dTJDKdL9vWFkMrwQ&page_size=100"
        url = base_url + "&location=" + str(self.request.get("Location"))
        print "url = " + url
        event_data_source= urllib2.urlopen(url)
        event_json_content = event_data_source.read()
        parsed_event_dictionary = json.loads(event_json_content)
        thing = parsed_event_dictionary["events"]["event"]
        i = 0
        s = ""
        for event in thing:

            s += "title: "

            if thing[i]["title"] is not None:
                s+= thing[i]["title"]

            s += "<br>"
            s += "description: "

            if thing[i]["description"] is not None:
                s += thing[i]["description"]

            s += "<br>"
            s += "venue name:"

            if thing[i]["venue_name"] is not None:
                s += thing[i]["venue_name"]

            s += "<br><br>"
            i+=1

        self.response.write(s)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
