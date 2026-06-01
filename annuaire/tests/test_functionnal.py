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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class SeleniumTestBase(StaticLiveServerTestCase):
    fixtures = ["test_functional.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def login(self):
        """
        Login as an administrator
        """
        self.selenium.get(f"{self.live_server_url}/auth/")
        username_input = self.selenium.find_element(By.ID, "username")
        username_input.send_keys("admin")
        password_input = self.selenium.find_element(By.ID, "password")
        password_input.send_keys("password")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()


class SearchTest(SeleniumTestBase):
    def test_login(self):
        """
        Test login through auth page with local user.
        """
        self.login()
        self.selenium.find_elements(By.XPATH, "//*[@id='menu']")

    def test_basic_search(self):
        """
        Test a basic search: student, responsible and classe.
        """
        self.login()
        self.selenium.get("%s%s" % (self.live_server_url, "/annuaire/"))

        # Search for a student.
        search_input = self.selenium.find_element(By.CLASS_NAME, "multiselect__input")
        search_input.send_keys("tutu")
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        # self.selenium.find_element(By.ID, "info-person")
        self.selenium.find_elements(By.XPATH, "//*[@id='info-person']")
        self.selenium.find_elements(By.XPATH, "//*[contains(text(), 'Toto')]")
        self.selenium.find_elements(By.XPATH, "//*[contains(text(), '1234')]")

        # Search for a responsible.
        search_input = self.selenium.find_element(By.CLASS_NAME, "multiselect__input")
        search_input.send_keys("tea")
        search_input.send_keys(Keys.ENTER)
        # self.selenium.find_element(By.ID, "info-person")
        self.selenium.find_elements(By.XPATH, "//*[@id='info-person']")
        self.selenium.find_elements(By.XPATH, "//*[contains(text(), 'Tea')]")
        self.selenium.find_elements(By.XPATH, "//*[contains(text(), 'Titulariat')]")

        # Search for a class.
        search_input = self.selenium.find_element(By.CLASS_NAME, "multiselect__input")
        search_input.send_keys("1")
        search_input.send_keys(Keys.ENTER)
        # self.selenium.find_element(By.ID, "class-student-list")
        self.selenium.find_elements(By.XPATH, "//*[@id='class-student-list']")
        self.selenium.find_elements(By.XPATH, "//*[contains(text(), 'Tutu Toto 1A')]")


class TabsNavigation(SeleniumTestBase):
    """
    Test tabs navigation after person search
    """

    def test_tabs_navigation(self):
        self.login()
        self.selenium.get("%s%s" % (self.live_server_url, "/annuaire/"))

        self.selenium.find_element(By.CSS_SELECTOR, ".multiselect__input").send_keys("tut")
        time.sleep(1)
        self.selenium.find_element(By.CSS_SELECTOR, ".multiselect__input").send_keys(Keys.ENTER)
        self.selenium.find_element(By.LINK_TEXT, "Infos personnelles").click()
        self.selenium.find_element(By.LINK_TEXT, "Horaire").click()
        element = self.selenium.find_element(By.LINK_TEXT, "Horaire")
        actions = ActionChains(self.selenium)
        actions.move_to_element(element).perform()
        element = self.selenium.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.selenium)
        actions.move_to_element(element).perform()
        self.selenium.find_element(By.LINK_TEXT, "Moyens de contacts").click()
        self.selenium.find_element(By.LINK_TEXT, "Infos médicales").click()
        element = self.selenium.find_element(By.LINK_TEXT, "Infos médicales")
        actions = ActionChains(self.selenium)
        actions.move_to_element(element).perform()
        element = self.selenium.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.selenium)
        actions.move_to_element(element).perform()
        self.selenium.find_element(By.LINK_TEXT, "Infos générales 0").click()
        element = self.selenium.find_element(By.LINK_TEXT, "Infos générales 0")
        actions = ActionChains(self.selenium)
        actions.move_to_element(element).perform()
        element = self.selenium.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.selenium)
        actions.move_to_element(element).perform()
