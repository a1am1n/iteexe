# -- coding: utf-8 --
# ===========================================================================
# eXe
# Copyright 2012, Pedro Peña Pérez, Open Phoenix IT
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
'''
@author: Pedro Peña Pérez
'''

from exe.engine.persistxml import encodeObjectToXML
from exe.engine.path import Path
from exe.engine.package import Package
from exe.export.scormexport import ScormExport
from exe.export.imsexport import IMSExport
from exe.export.websiteexport import WebsiteExport
from exe.export.singlepageexport import SinglePageExport


class CmdlineExporter(object):
    extensions = {'xml': '.xml',
                  'scorm': '.zip',
                  'ims': '.zip',
                  'website': '',
                  'webzip': '.zip',
                  'singlepage': ''
                  }

    def __init__(self, config):
        self.config = config
        self.web_dir = Path(self.config.webDir)

    def do_export(self, ftype, inputf, outputf, overwrite=False):
        if hasattr(self, 'export_' + ftype):
            if not outputf:
                if ftype in ('website','singlepage'):
                    outputf = inputf.rsplit(".elp")[0]
                else:
                    outputf = inputf + self.extensions[ftype]
            outputfp = Path(outputf)
            if outputfp.exists() and not overwrite:
                error = _(u'"%s" already exists.\nPlease try again \
with a different filename') % outputf
                raise Exception(error.encode('utf-8'))
            else:
                if outputfp.exists() and overwrite:
                    if outputfp.isdir():
                        for f in outputfp.walkfiles():
                            f.remove()
                        outputfp.rmdir()
                    else:
                        outputfp.remove()
                pkg = Package.load(inputf)
                if not pkg:
                    error = _(u"Invalid input package")
                    raise Exception(error.encode('utf-8'))
                self.styles_dir = self.web_dir.joinpath('style', pkg.style)
                getattr(self, 'export_' + ftype)(pkg, outputf)
                return outputf
        else:
            raise Exception(_(u"Export format not implemented")\
.encode('utf-8'))

    def export_xml(self, pkg, outputf):
        open(outputf, "w").write(encodeObjectToXML(pkg))

    def export_scorm(self, pkg, outputf):
        scormExport = ScormExport(self.config, self.styles_dir, outputf,
'scorm1.2')
        scormExport.export(pkg)

    def export_ims(self, pkg, outputf):
        imsExport = IMSExport(self.config, self.styles_dir, outputf)
        imsExport.export(pkg)

    def export_website(self, pkg, outputf):
        outputfp = Path(outputf)
        outputfp.makedirs()
        websiteExport = WebsiteExport(self.config, self.styles_dir, outputf)
        websiteExport.export(pkg)

    def export_webzip(self, pkg, outputf):
        websiteExport = WebsiteExport(self.config, self.styles_dir, outputf)
        websiteExport.exportZip(pkg)

    def export_singlepage(self, pkg, outputf, print_flag=0):
        images_dir = self.web_dir.joinpath('images')
        scripts_dir = self.web_dir.joinpath('scripts')
        templates_dir = self.web_dir.joinpath('templates')
        singlePageExport = SinglePageExport(self.styles_dir, outputf, \
                             images_dir, scripts_dir, templates_dir)
        singlePageExport.export(pkg, print_flag)