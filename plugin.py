# -*- coding: utf-8 -*-
###
# Copyright (c) 2012, spline
# All rights reserved.
#
#
###

import urllib2
import re
from BeautifulSoup import BeautifulSoup
import collections
import string

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
#from supybot.i18n import PluginInternationalization, internationalizeDocstring

#_ = PluginInternationalization('Soccer')

#@internationalizeDocstring
class Soccer(callbacks.Plugin):
    """Add the help for "@plugin help Soccer" here
    This should describe *how* to use this plugin."""
    threaded = True

    def _b64decode(self, string):
        """Returns base64 decoded string."""
        import base64
        return base64.b64decode(string)

    def _validleagues(self, league=None):
        """Return string containing league string if valid, 0 if error. If no league given, return leagues as keys of tuple."""
        leagues = { 'MLS':'usa.1', 'EPL':'eng.1', 'LaLiga':'esp.1',
                    'SerieA':'ita.1', 'Bundesliga':'ger.1', 'Ligue1':'fra.1',
                    'Eredivise':'ned.1', 'LigaMX':'mex.1'
                  }
        
        if league is None:
            return leagues.keys() # return the keys here for an list to display.
        else:
            if league not in leagues:
                return "0" # to parse an error.
            else:
                return leagues[league]
            
    ####################
    # Public Functions #
    ####################
            
    
    def soccer(self, irc, msg, args, optleague):
        """[league]
        Display live/completed scores for various leagues.
        """
        
        leagueString = self._validleagues(league=optleague)
        
        if leagueString == "0":
            irc.reply("Must specify league. Leagues is one of: %s" % (self._validleagues(league=None)))
            return

        url = self._b64decode('aHR0cDovL20uZXNwbi5nby5jb20vc29jY2VyL3Njb3JlYm9hcmQ/') + 'leagueTag=%s&lang=EN&wjb=' % (leagueString)
    
        try:
            req = urllib2.Request(url)
            html = (urllib2.urlopen(req)).read()
        except:
            irc.reply("Failed to open %s" % url)
            return
        
        soup = BeautifulSoup(html)
        divs = soup.findAll('div', attrs={'class':'ind'})

        append_list = []

        for div in divs:
            if div.find('div', attrs={'style':'white-space: nowrap;'}):
                match = div.find('div', attrs={'style':'white-space: nowrap;'})
                if match:
                    match = match.getText().encode('utf-8') # do string formatting/color below. Ugly but it works.
                    match = match.replace('Final -',ircutils.mircColor('FT', 'red') + ' -')
                    match = match.replace('Postponed -',ircutils.mircColor('PP', 'yellow') + ' -')
                    match = match.replace('(ESPN, UK)','').replace('(ESPN3)','').replace(' ET','').replace(' CT','').replace(' PT','')
                    # 17' - Osasuna 1-0 Barcelona | 2:00 PM - Getafe vs Real Madrid
                    append_list.append(str(match).strip())
            
        if len(append_list) > 0:
            descstring = string.join([item for item in append_list], " | ")
            irc.reply(descstring)
        else:
            irc.reply("I did not find any matches going on for: %s" % leagueString)          
    soccer = wrap(soccer, [('somethingWithoutSpaces')])
    
    
    #def soccerstats(self, irc, msg, args)

Class = Soccer

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=250:
