# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Course Builder Hello World module.

This module provides examples of two handlers:

1. GlobalHandler, available at <your_url>:<your_port>/global. This is an example
   of a global handler that is not bound to a particular course.

2. NamespacedHandler, available at
   <your_url>:<your_port>/<course_slug>/local. This is an example of a
   namespaced handler that is bound to and aware of the current course. After
   creating any course ('my_course', say), visit
   <your_url>:<your_port>/my_course/local to invoke this handler. Note that
   unless your course is public you will not be able to visit this handler
   without authenticating.

Both handlers provide examples of signing the user in, and handling both
authenticated and unauthenticated users.
"""

__author__ = [
    'johncox@google.com (John Cox)',
]

import os

from common import jinja_utils
from controllers import utils
from models import custom_modules

from google.appengine.api import users


_BASE_PATH = os.path.dirname(__file__)
_TEMPLATES_PATH = os.path.join(_BASE_PATH, 'templates')


class GlobalHandler(utils.BaseHandler):
    """Handler for requests scoped to the Course Builder instance."""

    URL = '/global'

    def get(self):
        template = jinja_utils.get_template('index.html', [_TEMPLATES_PATH])
        self.response.write(template.render({
            'course': None,
            'login_url': users.create_login_url(self.request.path),
            'logout_url': users.create_logout_url(self.request.path),
            'user': users.get_current_user(),
        }))


class NamespacedHandler(utils.CourseHandler):
    """Handler that is aware of the current course."""

    URL = '/local'

    def get(self):
        template = jinja_utils.get_template('index.html', [_TEMPLATES_PATH])
        self.response.write(template.render({
            'course': self.get_course(),
            'login_url': users.create_login_url(self.request.path),
            'logout_url': users.create_logout_url(self.request.path),
            'user': users.get_current_user(),
        }))


custom_module = None


def register_module():
    # Allow global per CB module pattern.
    global custom_module  # pylint: disable=global-statement

    global_handlers = [
        (GlobalHandler.URL, GlobalHandler),
    ]
    namespaced_handlers = [
        (NamespacedHandler.URL, NamespacedHandler),
    ]
    custom_module = custom_modules.Module(
        'Hello World', 'Course Builder Hello World Module', global_handlers,
        namespaced_handlers)

    return custom_module
