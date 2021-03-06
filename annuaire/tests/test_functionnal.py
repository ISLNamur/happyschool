# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


class SeleniumTests(StaticLiveServerTestCase):
    fixtures = ['test_functional.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/auth/'))
        username_input = self.selenium.find_element_by_id("inputUser")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_id("inputPassword")
        password_input.send_keys('password')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/annuaire/'))

        search_input = self.selenium.find_element_by_class_name("multiselect__input")
        search_input.send_keys("tutu")
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        self.selenium.find_element_by_id("info-student")
        self.selenium.find_elements_by_xpath("//*[contains(text(), 'Toto')]")
        self.selenium.find_elements_by_xpath("//*[contains(text(), '1234')]")
