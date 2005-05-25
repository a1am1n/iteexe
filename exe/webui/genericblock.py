# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================
"""
GenericBlock can render and process GenericIdevices as XHTML
"""

import logging
import gettext
from exe.webui.block            import Block
from exe.engine.genericidevice  import GenericIdevice
from exe.webui.element          import createElement

log = logging.getLogger(__name__)
_   = gettext.gettext


# ===========================================================================
class GenericBlock(Block):
    """
    GenericBlock can render and process GenericIdevices as XHTML
    """
    def __init__(self, idevice):
        Block.__init__(self, idevice)
        self.elements = []
        for field in self.idevice:
            self.elements.append(createElement(field.fieldType, 
                                               field.name, 
                                               field.class_,
                                               self.id,
                                               field.instruction))


    def process(self, request):
        """
        Process the request arguments from the web server
        """
        Block.process(self, request)
        for element in self.elements:
            content = element.process(request)
            if content is not None:
                self.idevice[element.name] = content


    def renderEdit(self, style):
        """
        Returns an XHTML string with the form element for editing this block
        """
        html  = "<div ondblclick=submitLink('edit',9, 0);>\n"
        for element in self.elements:
            html += element.renderEdit(self.idevice[element.name])

        html += self.renderEditButtons()
        html += "</div>\n"
        return html


    def renderViewContent(self):
        """
        Common rendering function for both view and preview modes
        """
        html  = "<div class=\"iDevice_inner\">\n"
        for element in self.elements:
            html += element.renderView(self.idevice[element.name])
        html += "</div>\n"
        return html

# ===========================================================================
