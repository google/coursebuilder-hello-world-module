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

"""Functional tests for the Course Builder Hello World module.

These tests provide examples of how to test global and namespaced handlers, as
well as authenticated and unauthenticated users.
"""


from modules.hello import hello
from tests.functional import actions


class _TestBase(actions.TestBase):

    def setUp(self):
        super(_TestBase, self).setUp()
        self.user_email = 'test@example.com'

    def assert_course_title_in(self, course_title, response):
        self.assertIn('Welcome to ' + course_title, response.body)

    def assert_authenticated_response_looks_correct(
            self, response, course_title=None):
        self.assertEqual(200, response.status_code)
        self.assertIn(self.user_email, response.body)
        self.assertIn('Sign out', response.body)

        if course_title:
            self.assert_course_title_in(course_title, response)

    def assert_unauthenticated_response_looks_correct(
            self, response, course_title=None):
        self.assertEqual(200, response.status_code)
        self.assertIn('Please sign in', response.body)

        if course_title:
            self.assert_course_title_in(course_title, response)


class GlobalHandlerTest(_TestBase):

    def test_authenticated_response_looks_correct(self):
        actions.login(self.user_email)

        self.assert_authenticated_response_looks_correct(
            self.testapp.get(hello.GlobalHandler.URL))

    def test_unauthenticated_response_looks_correct(self):
        self.assert_unauthenticated_response_looks_correct(
            self.testapp.get(hello.GlobalHandler.URL))


class NamespacedHandlerTest(_TestBase):

    def setUp(self):
        super(NamespacedHandlerTest, self).setUp()
        self.admin_email = 'admin@example.com'
        self.course_name = 'test_course'
        self.course_title = 'Test Course'
        self.namespaced_url = '/%s%s' % (
            self.course_name, hello.NamespacedHandler.URL)
        actions.simple_add_course(
            self.course_name, self.admin_email, self.course_title)

    def test_authenticated_response_looks_correct(self):
        actions.login(self.user_email)

        self.assert_authenticated_response_looks_correct(
            self.testapp.get(self.namespaced_url),
            course_title=self.course_title)

    def test_unauthenticated_response_looks_correct(self):
        self.assert_unauthenticated_response_looks_correct(
            self.testapp.get(self.namespaced_url),
            course_title=self.course_title)
