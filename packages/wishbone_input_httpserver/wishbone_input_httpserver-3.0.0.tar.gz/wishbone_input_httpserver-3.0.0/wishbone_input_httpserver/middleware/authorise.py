#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  authorise.py
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


class Authorize(object):
    '''
    A Falcon middleware which handles user and token authorisation against endpoints.
    '''

    def __init__(self, authorize_user_callback, authorize_token_callback, requires_authentication):

        self.authorize_token = authorize_token_callback
        self.authorize_user = authorize_user_callback
        self.requires_authentication = requires_authentication

    def process_request(self, req, resp):

        if self.requires_authentication(req.queue):
            if hasattr(req, "auth_type"):
                if req.auth_type == "basic":
                    if not self.authorize_user(req.auth_user, req.queue):
                        raise HTTPUnauthorized(
                            title="401 Unauthorized",
                            description="User not authorized for resource."
                        )
                elif req.auth_type == "token":
                    if not self.authorize_token(req.auth_token, req.queue):
                        raise HTTPUnauthorized(
                            title="401 Unauthorized",
                            description="Token incorrect."
                        )
            else:
                raise HTTPUnauthorized(
                    title="401 Unauthorized",
                    description="Failed to authenticate."
                )
