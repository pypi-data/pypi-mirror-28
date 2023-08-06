'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from scif.logger import bot
import sys
import os

    

def main(args,parser,subparser):

    from scif.main import ScifRecipe
    client = ScifRecipe(writable=False, quiet=True)
    
    result = []
    for app in client.apps():
        config = client.get_appenv(app)
        result.append([app.rjust(10), config['SCIF_APPROOT']]) 

    if len(result) > 0:
        header = "[app]              [root]"
        bot.custom(prefix="SCIF", message=header, color="CYAN")
        bot.table(result)
