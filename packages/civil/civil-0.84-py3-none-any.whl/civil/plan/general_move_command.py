# coding=utf-8
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

"""

from civil.plan.plan import Plan


class GeneralMoveCommand(Plan):
    """
    Any command which displaces the unit somehow must subclass from this class. Target
    coordinates of the move command must be in self.target_x, self.target_y. This class is mostly used
    to have a common base class for movement related orders.
    """
    pass
