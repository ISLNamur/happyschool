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


class DossierEleveAddTest(SeleniumTestBase):
    # headless = False

    fixtures = SeleniumTestBase.fixtures + [
        "dossier_eleve_infos.json",
        "dossier_eleve_sanctions.json",
        "test_dossier_eleve_settings.json",
    ]

    def test_adding_student(self):
        self.login()

        self.driver.get(f"{self.live_server_url}/dossier_eleve/")

        self.driver.find_element(By.LINK_TEXT, "Nouveau cas").click()
        self.driver.find_element(By.ID, "input-name").send_keys("tutu")
        time.sleep(1)
        self.driver.find_element(By.ID, "input-name").send_keys(Keys.ENTER)

        self.driver.find_element(By.ID, "input-demandeur").send_keys("tea")
        time.sleep(1)
        self.driver.find_element(By.ID, "input-demandeur").send_keys(Keys.ENTER)

        # Select info cas.
        self.driver.find_element(By.ID, "info-check").click()
        self.driver.find_element(By.ID, "input-info").click()
        self.driver.find_element(By.XPATH, "//option[@value=6]").click()
        time.sleep(1)

        # Add comment.
        self.driver.find_element(By.CSS_SELECTOR, "#comment .ck-content").send_keys("TEST COMMENT")
        # Give visibility to teachers.
        self.driver.find_element(By.XPATH, "//input[@text='Professeurs']").click()

        # Submit form.
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)

        # Check if new element was added.
        self.driver.find_elements(By.CLASS_NAME, "info")
