#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  token_authentication.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from falcon import HTTPUnauthorized


class TokenAuthentication(object):
    '''
    A Falcon middleware which extracts the token value from the Authorization header.
    '''

    def process_request(self, req, resp):

        auth = req.get_header('Authorization')

        if auth is not None:
            auth_type, token = self.extractTokenAndType(auth)
            if auth_type == "token":
                req.auth_type = "token"
                req.auth_token = token

    def extractTokenAndType(self, data):
        '''
        Extracts the token from the Authorize header

        Args:
            data (str): The authentication string to process

        Returns:
            str: The token value

        Raises:
            HTTPUnauthorized: For every error occurring
        '''

        result = data.split()

        if len(result) != 2:
            raise HTTPUnauthorized(
                title="401 Unauthorized",
                description="Auth value does not have the right format."
            )

        return result[0].lower(), result[1]
