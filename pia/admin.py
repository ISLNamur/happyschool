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

from django.contrib import admin

from . import models

admin.site.register(models.PIASettingsModel)
admin.site.register(models.PIAModel)
admin.site.register(models.DisorderModel)
admin.site.register(models.DisorderResponseModel)
admin.site.register(models.ScheduleAdjustmentModel)
admin.site.register(models.CrossGoalModel)
admin.site.register(models.AssessmentModel)
admin.site.register(models.BranchModel)
admin.site.register(models.BranchGoalModel)
admin.site.register(models.CrossGoalItemModel)
admin.site.register(models.BranchGoalItemModel)
admin.site.register(models.ClassCouncilPIAModel)
admin.site.register(models.OtherStatementModel)
admin.site.register(models.ResourceDifficultyModel)
admin.site.register(models.StudentStateModel)
