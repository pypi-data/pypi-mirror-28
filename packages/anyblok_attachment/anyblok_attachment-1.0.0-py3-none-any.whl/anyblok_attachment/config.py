# This file is a part of the AnyBlok / Attachment api project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.config import Configuration


Configuration.add_configuration_groups('createdb', ['attachment-wkhtml2pdf'])
Configuration.add_configuration_groups('updatedb', ['attachment-wkhtml2pdf'])
Configuration.add_configuration_groups('nose', ['attachment-wkhtml2pdf'])
Configuration.add_configuration_groups('interpreter', ['attachment-wkhtml2pdf'])

try:
    # import the configuration to get application
    import anyblok_pyramid.config  # noqa
    Configuration.add_configuration_groups('pyramid', ['attachment-wkhtml2pdf'])
    Configuration.add_configuration_groups(
        'gunicorn', ['attachment-wkhtml2pdf'])
except ImportError:
    pass

try:
    # import the configuration to get application
    import anyblok_dramatiq.config  # noqa
    Configuration.add_configuration_groups(
        'dramatiq', ['attachment-wkhtml2pdf'])
except ImportError:
    pass


@Configuration.add('attachment-wkhtml2pdf', label="WkHtml2Pdf - options",
                   must_be_loaded_by_unittest=True)
def define_attachment_wkhtml2pdf(group):
    group.add_argument('--wkhtml2pdf-unquiet', action="store_false",
                       default=True, help="Be more verbose")
    group.add_argument('--wkhtml2pdf-debug-javascript', action="store_true",
                       help="Show javascript debugging output")
