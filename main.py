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
# If you need to log in:
# api.login('username', 'password')

# events = api.call('/events/search', q='music', l='San Diego')
# for event in events['events']['event']:
#     print "%s at %s" % (event['title'], event['venue_name'])
# ]

jinja_environment = jinja2.Environment(loader= jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        url = "api.eventful.com/json/events/search?app_key=dTJDKdL9vWFkMrwQ"
        end_url = url+"&location=buffalo"
        event_data_source = urllib2.urlopen(end_url).read()
        parsed_events = json.loads(event_data_source)
        self.response.write(parsed_events)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
