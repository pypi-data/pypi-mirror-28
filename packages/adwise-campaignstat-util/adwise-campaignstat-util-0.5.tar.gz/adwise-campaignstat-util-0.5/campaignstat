#!/usr/bin/env python
'''
Created on Feb 7, 2016

@author: sonu
'''
import os
import sys
from datetime import datetime, timedelta
import json
import requests
import re

import time
from optparse import OptionParser

#ADWISE_MEDIA_URL = "http://127.0.0.1:8000"
ADWISE_ANALYTICS_URL = "http://ec2-18-221-71-42.us-east-2.compute.amazonaws.com:8001"
ADWISE_MEDIA_URL = "http://ec2-18-221-71-42.us-east-2.compute.amazonaws.com:8000"
AMQP_URL = "amqp://mrafhtxb:HuPwIQDIAxoC3HQTuyHluZPULpR6uReS@white-mynah-bird.rmq.cloudamqp.com/mrafhtxb"
NIKAZA_URL = "https://nikaza.io/"


def print_table(items, header=None, wrap=True, max_col_width=20, wrap_style="wrap", row_line=False, fix_col_width=False):
    ''' Prints a matrix of data as a human readable table. Matrix
    should be a list of lists containing any type of values that can
    be converted into text strings.

    Two different column adjustment methods are supported through
    the *wrap_style* argument:

       wrap: it will wrap values to fit max_col_width (by extending cell height)
       cut: it will strip values to max_col_width

    If the *wrap* argument is set to False, column widths are set to fit all
    values in each column.

    This code is free software. Updates can be found at
    https://gist.github.com/jhcepas/5884168

    '''

    if fix_col_width:
        c2maxw = dict([(i, max_col_width) for i in xrange(len(items[0]))])
        wrap = True
    elif not wrap:
        c2maxw = dict([(i, max([len(str(e[i])) for e in items])) for i in xrange(len(items[0]))])
    else:
        c2maxw = dict([(i, min(max_col_width, max([len(str(e[i])) for e in items])))
                        for i in xrange(len(items[0]))])
    if header:
        current_item = -1
        row = header
        if wrap and not fix_col_width:
            for col, maxw in c2maxw.iteritems():
                c2maxw[col] = max(maxw, len(header[col]))
                if wrap:
                    c2maxw[col] = min(c2maxw[col], max_col_width)
    else:
        current_item = 0
        row = items[current_item]
    while row:
        is_extra = False
        values = []
        extra_line = [""]*len(row)
        for col, val in enumerate(row):
            cwidth = c2maxw[col]
            wrap_width = cwidth
            val = str(val)
            try:
                newline_i = val.index("\n")
            except ValueError:
                pass
            else:
                wrap_width = min(newline_i+1, wrap_width)
                val = val.replace("\n", " ", 1)
            if wrap and len(val) > wrap_width:
                if wrap_style == "cut":
                    val = val[:wrap_width-1]+"+"
                elif wrap_style == "wrap":
                    extra_line[col] = val[wrap_width:]
                    val = val[:wrap_width]
            val = val.ljust(cwidth)
            values.append(val)
        print ' | '.join(values)
        if not set(extra_line) - set(['']):
            if header and current_item == -1:
                print ' | '.join(['='*c2maxw[col] for col in xrange(len(row)) ])
            current_item += 1
            try:
                row = items[current_item]
            except IndexError:
                row = None
        else:
            row = extra_line
            is_extra = True

        if row_line and not is_extra and not (header and current_item == 0):
            if row:
                print ' | '.join(['-'*c2maxw[col] for col in xrange(len(row)) ])
            else:
                print ' | '.join(['='*c2maxw[col] for col in xrange(len(extra_line)) ])


class AdwiseHttpConnection(object):

    def __init__(self, endpoint, user, passwd):
        self._endpoint = endpoint
        self.VENUE_URL = "/mediacontentapp/mediasource/venue/"
        self._user = user
        self._passwd = passwd

    @property
    def enpoint(self):
        return self._endpoint

    def _get_campaing_playing(self, campId):
        api_endpoint = self._endpoint + (
                                "/mediacontent/campaign/playing/%s" % (campId))
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.get(url=api_endpoint,
                                headers=headers)
        return response

    def _get_campaign_tracking(self, campId):
        api_endpoint = self._endpoint + (
                                "/mediacontent/campaign/%s/track/" % (campId))
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.get(url=api_endpoint,
                                headers=headers)
        return response

    def list_venues(self):
        api_endpoint = self._endpoint + "/mediacontent/mediasource/venue/"
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.get(url=api_endpoint,
                                headers=headers)
        if response.ok:
            resp = json.loads(response.text)
            return resp
        else:
            return None

    def list_campaign(self):
        api_endpoint = self._endpoint + "/mediacontent/campaign/"
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.get(url=api_endpoint,
                                headers=headers)
        if response.ok:
            campresp = json.loads(response.text)
            camptrack = {}
            campplay = {}
            for camp in campresp:
                # get track information
                trackresp = self._get_campaign_tracking(camp['id'])
                if trackresp.ok:
                    camptrack[camp['id']] = json.loads(trackresp.text)
                # get playing information
                playing = self._get_campaing_playing(camp['id'])
                if playing.ok:
                    campplay[camp['id']] = json.loads(playing.text)
            return (campresp, camptrack, campplay)
        else:
            return (None, None, None)
    
    def get_campaign_stat(self, objectid, begin, end):
        api_endpoint = self._endpoint + "/stats/campaign/?"
        api_query_params = "campaign_id=%s&start_time=%s&end_time=%s" % (objectid, begin, end)
        api = api_endpoint + api_query_params
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.get(url=api,
                                headers=headers)
        if response.ok:
            statresp = json.loads(response.text)
            return statresp
        # Bad response
        return None  

def get_stat(user, password, objectid, begin=None, end=None):
    connection = AdwiseHttpConnection(ADWISE_ANALYTICS_URL, user, password)
    return connection.get_campaign_stat(objectid, begin, end)    
    
def venue_summary(venuedata):
#     [
#      [3,2, {"whatever": 1, "bla": [1,2]}],
#      [5,"function",777],
#      [1,1,1]
#     ]
    venueRecords = []
    for venue in venuedata:
        sensors = venue['sensors']
        _rec = [venue['venue_name'], venue['id'],
                {"queue-url": AMQP_URL,
                 "queue-id": [venue['venue_name'], venue['venue_name']+"_control"],
                 "venue-meta": venue['venue_meta']},
                {"sensors": [(sensor["id"], sensor["mac_address"], sensor["display_name"], sensor["sensor_meta"]) for sensor in sensors]}]
        venueRecords.append(_rec)

    print_table(venueRecords,
                header=[ "Venue Name", "Venue Id", "Message Queue", "Sensor Ids"],
                wrap=True, max_col_width=50, wrap_style='wrap',
                row_line=True, fix_col_width=False,)

def campaign_stat_summary(campid, statresp):
    stat_table = []
    if statresp:
        _campaigndata = statresp[0]
        _data = []
        # prepare data rows
        _data.append(_campaigndata["campaign_id"])
        _data.append(_campaigndata["numClicks"])
        _data.append(_campaigndata["numAndroid"])
        _data.append(_campaigndata["numiPhone"])
        _data.append(_campaigndata["numWindows"])        
        stat_table.append(_data)
        
        print_table(stat_table,
                    header=[ "Campaign Id", "Total Clicks", "Android Users", "Apple Users", "Windows/Linux Users"],
                    wrap=True, max_col_width=33, wrap_style='wrap',
                    row_line=True, fix_col_width=False,)
    else:
        print "Empty response"
        

def campaign_summary(campaigndata, campaigntrack, campaignplaying):
#     [
#      [3,2, {"whatever": 1, "bla": [1,2]}],
#      [5,"function",777],
#      [1,1,1]
#     ]
    campaignRecords = []
    for campaign in campaigndata:
        campId = campaign['id']
        short_url = campaigntrack[campId]['short_url'] if campaigntrack and campId in campaigntrack.keys() else ""
        plays = campaignplaying[campId] if campaignplaying and campId in campaignplaying.keys() else ""
        sensors = [(play['primary_media_source']['display_name'])
                            for play in plays ]
        _rec = [campaign['name'], campaign['id'],
                {"Playing": sensors},{"url":short_url}]
        
        campaignRecords.append(_rec)

    print_table(campaignRecords,
                header=[ "Campaign Name", "Campaign Id", "Playing", "URL"],
                wrap=True, max_col_width=33, wrap_style='wrap',
                row_line=True, fix_col_width=False,)


def list_venue(user, passwd):
    connection = AdwiseHttpConnection(ADWISE_MEDIA_URL, user, passwd)
    resp = connection.list_venues()
    if resp:
        return venue_summary(resp)

def list_campaign(user, passwd):
    connection = AdwiseHttpConnection(ADWISE_MEDIA_URL, user, passwd)
    return connection.list_campaign()

def main(argv):
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-z", "--adwise-user", dest="adwiseuser")
    parser.add_option("-y", "--adwise-passwd", dest="adwisepasswd")    
    parser.add_option("-a", "--list-campaign", action="store_true", dest="listcamp")
    parser.add_option("-b", "--camp-id", dest="campid")
    parser.add_option("-c", "--venue-id", dest="venueid")    
    parser.add_option("-d", "--list-venue", action="store_true", dest="listvenue")
    parser.add_option("-e", "--start", dest="begin")
    parser.add_option("-f", "--end", dest="end")
    parser.add_option("-g", "--list-sensor", action="store_true", dest="listsensor")
    parser.add_option("-i", "--sensor-id", dest="sensorid")
    parser.add_option("-j", "--get-stat", action="store_true", dest="getstat")
    
    (options, args) = parser.parse_args()
    if not options.adwiseuser or not options.adwisepasswd:
        print "Usage error: Adwise access is required to do  operation."
        return -1
    
    if options.listcamp:
        # List campaign with tracking
        (camp, track, play) = list_campaign(options.adwiseuser,
                                            options.adwisepasswd)
        if camp:
            campaign_summary(camp, track, play)
        else:
            print "Error listing campaigns"
        return 0
    elif options.listvenue:
        list_venue(options.adwiseuser, options.adwisepasswd)
    elif options.getstat:
        if options.campid:
            statresp = get_stat(options.adwiseuser,
                                options.adwisepasswd,
                                options.campid,
                                options.begin,
                                options.end)
            campaign_stat_summary(options.campid, statresp)
        elif options.venueid:
            print "Not implemented"            
        else:
            print "Object ID is not passed."
    else:
        print "Usage Error : unknown options"


if __name__ == '__main__':
    main(sys.argv[1:])
