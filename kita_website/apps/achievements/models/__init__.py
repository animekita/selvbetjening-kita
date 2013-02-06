from achievements import AchievementGroup, Achievement, Award
from privacy import Privacy

from kita_website.apps.achievements.generators.event_attendance import \
     GroupToAchievementGroup, EventAttendanceAchievement

from kita_website.apps.achievements.generators.positions import \
     Position, PositionHistory

from kita_website.apps.achievements.generators.tournaments import \
     Tournament, Winner

from kita_website.apps.achievements import processors

from kita_website.apps.achievements.generators import event_attendance, \
     positions, member_of_kita

refresh_achievements_handlers = [event_attendance.refresh,
                                 member_of_kita.refresh,
                                 positions.refresh]

from selvbetjening.sadmin.base.sadmin import site
from kita_website.apps.achievements.admin import PositionAdmin

