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
        template = jinja_environment.get_template('templates/index.html')
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            greeting = ('Hello, ' + nickname + "!" + '<a href="%s">Sign Out</a>' % (users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign In</a>' % users.create_login_url('/'))
        signin = ('<html><body><section id="WholeTopPart"><div class="top" id="SignIn">%s</div></section></body></html>' % greeting)
        login = {
                "Signin" : signin
                }

        self.response.write(template.render(login))

    def post(self):
        template = jinja_environment.get_template('templates/results.html')
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            greeting = ('Hello, ' + nickname + "!" + '<a href="%s">Sign Out</a>' % (users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign In</a>' % users.create_login_url('/'))
        signin = ('<html><body><section id="WholeTopPart"><div class="top" id="SignIn">%s</div></section></body></html>' % greeting)


        #self.response.write(template.render(login))

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
        event_image_url_medium = {}
        for event in listOfEvents:
            if listOfEvents[i]["title"] not in event_title_list:
                event_title_list.append(listOfEvents[i]["title"])#puts all the titles in a list
            event_id_list.append(listOfEvents[i]["id"])#puts all the ids in a list
            event_title_id[listOfEvents[i]["title"]] = listOfEvents[i]["id"]#conencts the title with its id
            if listOfEvents[i]["image"]is None:
                if self.request.get('category') == 'outdoors_recreation':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/outdoors_image.jpg"
                elif self.request.get('category') == 'music':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/concerts_image.gif"
                elif self.request.get('category') == 'art':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/art_image.png"
                elif self.request.get('category') == 'animals':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/pets_image.jpg"
                elif self.request.get('category') == 'sports':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/sports_image.png"
                elif self.request.get('category') == 'comedy':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/comedy_image.jpg"
                elif self.request.get('category') == 'family_fun_kids':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/family_image.jpg"
                elif self.request.get('category') == 'singles_social':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/nightlife_image.jpg"
                elif self.request.get('category') == 'performing_arts':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/performing_arts_image.jpg"
                elif self.request.get('category') == 'learning_education':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/educational_image.jpg"
                elif self.request.get('category') == 'movies_film':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/movies_image.jpg"
                elif self.request.get('category') == 'food':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/food_image.jpg"
                elif self.request.get('category') == 'support':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/health_image.jpg"
                elif self.request.get('category') == 'attractions':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/museums_image.jpg"
                elif self.request.get('category') == 'politics_activism':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/politics_image.jpg"
                elif self.request.get('category') == 'science':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/science_image.jpg"
                elif self.request.get('category') == 'technology':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/technology_image.jpg"
                elif self.request.get('category') == 'conference':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/conferences_image.jpg"
                elif self.request.get('category') == 'fundraisers':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/fundraiser_image.jpg"
                elif self.request.get('category') == 'holiday':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/holiday_image.jpg"
                elif self.request.get('category') == 'community':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/community_image.jpg"
                elif self.request.get('category') == 'books':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/books_image.jpg"
                elif self.request.get('category') == 'business':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/business_image.jpg"
                elif self.request.get('category') == 'schools_alumni':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/school_events.jpg"
                elif self.request.get('category') == 'clubs_association':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/organizations_image.jpg"
                elif self.request.get('category') == 'sales':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/sales_image.jpg"
                elif self.request.get('category') == 'religion_spirituality':
                    event_image_url_medium[listOfEvents[i]["title"]] = "/resources/religion_image.jpg"
            else:
                if type(listOfEvents[i]["image"]) is list:
                    event_image_url_medium[listOfEvents[i]["title"]] = listOfEvents[i]["image"][0]["medium"]["url"]
                else:
                    event_image_url_medium[listOfEvents[i]["title"]] = listOfEvents[i]["image"]["medium"]["url"]
            event_title_venue[listOfEvents[i]["title"]] = listOfEvents[i]["venue_name"]
            event_category[listOfEvents[i]["title"]] = str(self.request.get("category"))
            i += 1
        event_dictionary = {
            "eventTitlePhotoUrl": event_image_url_medium,
            "eventTitleVenue": event_title_venue,
            "eventTitles": event_title_list,
            "eventIds": event_id_list,
            "eventTitleId" : event_title_id,
            "eventCategory" : event_category,
            "Signin" : signin
            }
        self.response.write(template.render(event_dictionary))



class EventInfo(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/event_specifics.html')
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            greeting = ('Hello, ' + nickname + "!" + '<a href="%s">Sign Out</a>' % (users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign In</a>' % users.create_login_url('/'))
        signin = ('<html><body><section id="WholeTopPart"><div class="top" id="SignIn">%s</div></section></body></html>' % greeting)


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
            if self.request.get('category') == 'outdoors_recreation':
                event_image_url_medium = "/resources/outdoors_image.jpg"
            elif self.request.get('category') == 'music':
                event_image_url_medium = "/resources/concerts_image.gif"
            elif self.request.get('category') == 'art':
                event_image_url_medium = "/resources/art_image.png"
            elif self.request.get('category') == 'animals':
                event_image_url_medium = "/resources/pets_image.jpg"
            elif self.request.get('category') == 'sports':
                event_image_url_medium = "/resources/sports_image.png"
            elif self.request.get('category') == 'comedy':
                event_image_url_medium = "/resources/comedy_image.jpg"
            elif self.request.get('category') == 'family_fun_kids':
                event_image_url_medium = "/resources/family_image.jpg"
            elif self.request.get('category') == 'singles_social':
                event_image_url_medium = "/resources/nightlife_image.jpg"
            elif self.request.get('category') == 'performing_arts':
                event_image_url_medium = "/resources/performing_arts_image.jpg"
            elif self.request.get('category') == 'learning_education':
                event_image_url_medium = "/resources/eduacational_image.jpg"
            elif self.request.get('category') == 'movies_film':
                event_image_url_medium = "/resources/movies_image.jpg"
            elif self.request.get('category') == 'food':
                event_image_url_medium = "/resources/food_image.jpg"
            elif self.request.get('category') == 'support':
                event_image_url_medium = "/resources/health_image.jpg"
            elif self.request.get('category') == 'attractions':
                event_image_url_medium = "/resources/museums_image.jpg"
            elif self.request.get('category') == 'politics_activism':
                event_image_url_medium = "/resources/politics_image.jpg"
            elif self.request.get('category') == 'science':
                event_image_url_medium = "/resources/science_image.jpg"
            elif self.request.get('category') == 'technology':
                event_image_url_medium = "/resources/technology_image.jpg"
            elif self.request.get('category') == 'conference':
                event_image_url_medium = "/resources/conferences_image.jpg"
            elif self.request.get('category') == 'fundraisers':
                event_image_url_medium = "/resources/fundraiser_image.jpg"
            elif self.request.get('category') == 'holiday':
                event_image_url_medium = "/resources/holiday_image.jpg"
            elif self.request.get('category') == 'community':
                event_image_url_medium = "/resources/community_image.jpg"
            elif self.request.get('category') == 'books':
                event_image_url_medium = "/resources/books_image.jpg"
            elif self.request.get('category') == 'business':
                event_image_url_medium = "/resources/business_image.jpg"
            elif self.request.get('category') == 'schools_alumni':
                event_image_url_medium = "/resources/school_events.jpg"
            elif self.request.get('category') == 'clubs_association':
                event_image_url_medium = "/resources/organizations_image.jpg"
            elif self.request.get('category') == 'sales':
                event_image_url_medium = "/resources/sales_image.jpg"
            elif self.request.get('category') == 'religion_spirituality':
                event_image_url_medium = "/resources/religion_image.jpg"
        else:
            if type(parsed_specific_event_dictionary["images"]["image"]) is list:
                event_image_url_medium = parsed_specific_event_dictionary["images"]["image"][0]["medium"]["url"]
            else:
                event_image_url_medium = parsed_specific_event_dictionary["images"]["image"]["medium"]["url"]


        if event_start_time is not "No start time found":
            start_time_list = event_start_time.split(" ")
            start_time_date = start_time_list[0].split("-")
            start_time_time = start_time_list[1].split(":")

            year = start_time_date[0]
            month = start_time_date[1]
            day = start_time_date[2]
            finalDate = day + "/" + month + "/" + year + " "

            AMorPM = ""
            minute = start_time_time[1]
            if start_time_time[0] >= 12:
                AMorPM = "PM"
            else:
                AMorPM = "AM"
            hour = int(start_time_time[0]) % 12
            if hour == 0:
                hour = 12
            finalTime = str(hour) + ":" + str(minute) + " " + AMorPM

            event_start_time = finalDate + finalTime

        if event_stop_time is not "No stop time found":
            stop_time_list = event_stop_time.split(" ")
            stop_time_date = stop_time_list[0].split("-")
            stop_time_time = stop_time_list[1].split(":")

            year = stop_time_date[0]
            month = stop_time_date[1]
            day = stop_time_date[2]
            finalDate = day + "/" + month + "/" + year + " "

            AMorPM = ""
            minute = stop_time_time[1]
            if stop_time_time[0] >= 12:
                AMorPM = "PM"
            else:
                AMorPM = "AM"
            hour = int(stop_time_time[0]) % 12
            if hour == 0:
                hour = 12
            finalTime = str(hour) + ":" + str(minute) + " " + AMorPM

            event_stop_time = finalDate + finalTime

        event_dict = {
            "title" : event_title,
            "venueName" : event_venue_name,
            "description" : event_description,
            "venueAddress" : event_venue_address,
            "mediumPicURL" : event_image_url_medium,
            "startTime" : event_start_time,
            "stopTime" : event_stop_time,
            "Signin" : signin

        }

        self.response.write(template.render(event_dict))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/event_specifics', EventInfo)
], debug=True)
