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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.tests import SeleniumTestBase


class InfirmerieAddTest(SeleniumTestBase):
    fixtures = SeleniumTestBase.fixtures + ["test_infirmerie.json"]

    def test_adding_deleting_student(self):
        self.login()

        self.driver.find_element(By.LINK_TEXT, "Ajouter un malade").click()
        self.driver.find_element(By.CSS_SELECTOR, ".multiselect__input").send_keys("tutu")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".multiselect__input").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "input-admission").click()
        self.driver.find_element(By.ID, "input-admission").send_keys("ENTRÉE")
        self.driver.find_element(By.ID, "submit-passage").click()
        self.driver.find_element(By.LINK_TEXT, "Encoder départ").click()
        self.driver.find_element(By.ID, "input-remarque").click()
        self.driver.find_element(By.ID, "input-remarque").send_keys("SORTIE")
        self.driver.find_element(By.ID, "submit-passage").click()


class InfirmerieDeleteTest(SeleniumTestBase):
    def test_adding_deleting_student(self):
        self.login()

        self.driver.find_element(By.CSS_SELECTOR, ".form-check-input").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-light:nth-child(2) > svg").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary:nth-child(2)").click()
