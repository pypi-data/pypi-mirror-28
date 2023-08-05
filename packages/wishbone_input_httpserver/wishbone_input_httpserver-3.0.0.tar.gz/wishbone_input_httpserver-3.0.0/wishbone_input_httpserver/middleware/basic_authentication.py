#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  basic_authentication.py
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
from base64 import b64decode
from passlib.hash import apr_md5_crypt


class BasicAuthentication(object):
    '''
    A Falcon middleware which handles Apache compatible Basic HTTP authentication.
    '''

    def __init__(self, gethash_callback):

        self.getHash = gethash_callback

    def process_request(self, req, resp):

        auth = req.get_header('Authorization')
        if auth is not None:
            payload = self.extractPrefixPayload(auth)
            if payload is None:
                return
            else:
                username, password = self.extractUsernamePasswordHash(payload)
                if not self.validatePassword(password, self.getHash(username)):
                    raise HTTPUnauthorized(
                        title="401 Unauthorized",
                        description="Password incorrect."
                    )
                else:
                    req.auth_type = "basic"
                    req.auth_user = username

    def extractPrefixPayload(self, data):
        '''
        Extracts the HTTP auth string prefix and returns decoded payload

        Args:
            data (str): The authentication string to process

        Returns:
            str: The base64 decoded value of the user/password


        Raises:
            HTTPUnauthorized: For every error occurring
        '''

        result = data.split()

        if len(result) != 2:
            raise HTTPUnauthorized(
                title="401 Unauthorized",
                description="Authorize header value does not have the right format."
            )

        if result[0].lower() == "basic":
            try:
                payload = b64decode(result[1]).decode('utf-8')
            except Exception:
                raise HTTPUnauthorized(
                    title="401 Unauthorized",
                    description="Could not properly decode authentication value."
                )
            else:
                return payload
        else:
            return None

    def extractUsernamePasswordHash(self, data):

        try:
            username, password = data.split(':')
            return username, password
        except Exception as err:
            raise HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization: Username password payload does not have expected format.',
            )

    def validatePassword(self, password, hash_value):
        '''
        Validates whether ``hash_value`` matches ``password``

        Args:
            password (str): The password to validate
            hash_value (str): The has to validate against

        Returns:
            bool: True when ``password`` and ``hash_value`` match

        Raise:
            HTTPUnauthorized: For every error occurring
        '''

        try:
            authenticated = apr_md5_crypt.verify(password, hash_value)
        except Exception as err:
            raise HTTPUnauthorized(
                title="401 Unauthorized",
                description="Password incorrect."
            )

        if not authenticated:
                raise HTTPUnauthorized(
                    title="401 Unauthorized",
                    description="Password incorrect."
                )
        else:
            return True
