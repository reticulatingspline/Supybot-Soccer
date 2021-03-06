###
# Copyright (c) 2013, spline
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry
#from supybot.i18n import PluginInternationalization, internationalizeDocstring

#_ = PluginInternationalization('Soccer')

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Soccer', True)


Soccer = conf.registerPlugin('Soccer')
conf.registerGlobalValue(Soccer, 'logURLs', registry.Boolean(True, """Should we log all URL calls?"""))
conf.registerChannelValue(Soccer, 'disableANSI', registry.Boolean(False, """Do not display any ANSI (color/bold) for channel."""))
conf.registerChannelValue(Soccer, 'adjustTZ', registry.Boolean(True, """Adjust timezone per match depending on the league/tournament."""))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=250:
