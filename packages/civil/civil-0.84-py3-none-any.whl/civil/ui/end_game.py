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

import os

from pygame.locals import *

from civil import constants
from civil.constants import UNION, REBEL, UNKNOWN
from civil.ui.button import Button
from civil.ui.dialog import *
from civil.ui.fader import Fader
from civil.ui.normal_label import NormalLabel
from civil.ui.title_label import TitleLabel


class EndGame(Dialog):
    """
    This class is used as a dialog for showing the final results of the game to the player. This
    class will gather statistics about the game, such as casualities and captured
    objectives. Depending on how the game ended a different backdrop will be used, i.e. the winning
    player gets a different backdrop from the losing player.

    First only the backdrop is shown, no stats. Then after a while a part starts to fade towards
    black, and then the stats are shown on that one.
    """

    def __init__(self):
        """
        Creates the dialog.
        """

        # calculate statistics
        self.calculateStatistics()

        # init superclass
        Dialog.__init__(self, scenario.sdl)

        # set our background to a tiled image. this should take into account weather the player won
        # or lost and use a different background for a loss and victory
        self.setBackground(properties.endgame_background)

        # we're showing backdrop. this is a counter (seconds) that only the backdrop is shown
        self.showbackdroponly = 4

        # we want time events
        self.enableTimer(1000)

    def createWidgets(self):
        """
        Creates all widgets for the dialog.
        """

        # load the fade and the box
        self.fader = Fader(position=(212, 100), size=(600, 300))

        # register our fader
        self.wm.register(self.fader)

    def createLabels(self):
        """
        Creates all labels for the dialog.
        """
        # create the labels
        report = TitleLabel("Battle report", (400, 120), color=(255, 255, 0))
        result = NormalLabel(self.summary, (400, 160), color=(255, 255, 255))

        # create the side headers
        men = TitleLabel("Men", (250, 240), color=(255, 180, 100))
        guns = TitleLabel("Guns", (250, 270), color=(255, 180, 100))
        score = TitleLabel("Score", (250, 320), color=(255, 180, 100))

        # create the top headers                            
        union = TitleLabel("Union", (350, 200), color=(255, 255, 0))
        rebel = TitleLabel("Confederate", (500, 200), color=(255, 255, 0))

        # create result strings for men and guns
        unionmenstr = "%d of %d" % (self.men_destroyed[UNION], self.men_ok[UNION])
        rebelmenstr = "%d of %d" % (self.men_destroyed[REBEL], self.men_ok[REBEL])
        uniongunsstr = "%d of %d" % (self.guns_destroyed[UNION], self.guns_ok[UNION])
        rebelgunsstr = "%d of %d" % (self.guns_destroyed[REBEL], self.guns_ok[REBEL])
        scorestr = "%d vs %d" % (self.score[UNION], self.score[REBEL])

        # and labels too
        unionmen = NormalLabel(unionmenstr, (350, 250))
        unionguns = NormalLabel(uniongunsstr, (350, 280))
        rebelmen = NormalLabel(rebelmenstr, (500, 250))
        rebelguns = NormalLabel(rebelgunsstr, (500, 280))
        score2 = NormalLabel(scorestr, (425, 325))

        # register our labels
        self.wm.register(report)
        self.wm.register(result)
        self.wm.register(union)
        self.wm.register(rebel)
        self.wm.register(men)
        self.wm.register(guns)
        self.wm.register(score)
        self.wm.register(score2)
        self.wm.register(unionmen)
        self.wm.register(rebelmen)
        self.wm.register(unionguns)
        self.wm.register(rebelguns)

        # buttons
        self.wm.register(Button(os.path.join(properties.path_dialogs, "butt-ok-moff.png"),
                                os.path.join(properties.path_dialogs, "butt-ok-mover.png"),
                                (406, 650), {widget.MOUSEBUTTONUP: self.ok}), K_RETURN)

    def ok(self, trigger, event):
        """
        Callback triggered when the user clicks the 'Ok' button.
        """

        # no more timer events needed
        self.disableTimer()

        # we're accepting the dialog
        self.state = ACCEPTED

        return widget.DONE

    def timer(self):
        """
        Callback triggered when the dialog has enabled timers and a timer fires. Updates the fade
        image on the dialog with some more alpha.
        """

        # are we still showing the backdrop only?
        if self.showbackdroponly > 0:
            # yes, decrement and go away
            self.showbackdroponly -= 1

            # did we get to 0 now?
            if self.showbackdroponly == 0:
                # yes, so change the timer value to make it faster
                self.enableTimer(100)

            return

        # we've shown the backdrop for some seconds, now get on with the fading. first get old alpha 
        alpha = self.fader.getAlpha()

        # are we done fading?
        if alpha >= 50:
            # yep, no more fading needed
            self.disableTimer()

            # create labels
            self.createLabels()

        else:
            # fade more, add 5 to the alpha
            self.fader.setAlpha(alpha + 5)

    def calculateStatistics(self):
        """
        This method calculates statistics about how the battle went. The data that is gathered
        is:

        * total/lost men
        * total/lost guns
        * total/lost units
        * captured objectives
        * a victory score

        The stats are stored in members for later usage.
        """
        # calculate destroyed units
        self.calculateDestroyedUnits()

        # and men
        self.calculateDestroyedMenAndGuns()

        # calculate all objectives
        self.calculateObjectives()

        # now calculate a victory score
        self.calculateScore()

        # create a summary string
        self.createSummary()

    def calculateDestroyedUnits(self):
        """
        This method calculates the number of units for both players that have been destroyed and
        how many are still ok, i.e. not destroyed.
        """

        # nothing alive at all yet
        self.units_ok = {REBEL: 0, UNION: 0}
        self.units_destroyed = {REBEL: 0, UNION: 0}

        # loop over all ok units
        for unit in scenario.info.units.values():
            # add to the counts
            self.units_ok[unit.getOwner()] += 1

        # loop over all destroyed units
        for unit in list(scenario.info.destroyed_units.values()):
            # add to the counts
            self.units_destroyed[unit.getOwner()] += 1

    def calculateDestroyedMenAndGuns(self):
        """
        This method calculates the number of men and guns for both players that have been
        destroyed and how many are still ok, i.e. not destroyed.
        """

        # nothing alive at all yet
        self.men_ok = {REBEL: 0, UNION: 0}
        self.men_destroyed = {REBEL: 0, UNION: 0}
        self.guns_ok = {REBEL: 0, UNION: 0}
        self.guns_destroyed = {REBEL: 0, UNION: 0}

        # loop over all ok units
        for unit in scenario.info.units.values():
            # add to the counts
            self.men_ok[unit.getOwner()] += unit.getMen()
            self.men_destroyed[unit.getOwner()] += unit.getKilled()

            # does it have guns?
            if unit.getWeapon().isArtillery():
                # yep, add those too
                ok, destroyed = unit.getWeaponCounts()
                self.guns_ok[unit.getOwner()] += ok
                self.guns_destroyed[unit.getOwner()] += destroyed

        # loop over all destroyed units
        for unit in list(scenario.info.destroyed_units.values()):
            # add to the counts. these units have no ok guns nor men
            self.men_destroyed[unit.getOwner()] += unit.getKilled()

            # does it have guns?
            if unit.getWeapon().isArtillery():
                # yep, add those too
                self.guns_destroyed[unit.getOwner()] += unit.getWeaponCounts()[1]

    def calculateObjectives(self):
        """
        Calculates all data related to objectives. Each objective a player has captured
        increases the score.
        """

        # no points yet
        self.objectives = {REBEL: 0, UNION: 0}

        # loop over all objectives
        for objective in scenario.info.objectives:
            # is the objective neutral?
            if objective.getOwner() != UNKNOWN:
                # nope, so add the score for the objective to the proper player
                self.objectives[objective.getOwner()] += objective.getPoints()

    def calculateScore(self):
        """
        Calculates a final score based on all totals.
        """

        # no score yet
        self.score = {REBEL: 0, UNION: 0}

        # add for all ok and destroyed men
        for player in [REBEL, UNION]:
            # add 1 for each killed enemy
            self.score[player] += self.men_destroyed[[UNION, REBEL][player]] * 1

            print("EndGame.calculateScore: %d: killed: %d" % (player,
                                                              self.men_destroyed[[UNION, REBEL][player]]))

            # add 100 for each destroyed enemy gun
            self.score[player] += self.guns_destroyed[[UNION, REBEL][player]] * 100

            print("EndGame.calculateScore: %d: guns: %d" % (player,
                                                            self.guns_destroyed[[UNION, REBEL][player]]))

            # add the scores for the objectives too
            self.score[player] += self.objectives[player]

            print("EndGame.calculateScore: %d: objectives: %d" % (player, self.objectives[player]))

        print("EndGame.calculateScore: total: %d - %d" % (self.score[REBEL], self.score[UNION]))

        # get a nice sum of the scores
        sum = self.score[REBEL] + self.score[UNION]

        # get the percentages for the players
        if self.score[REBEL] == 0:
            # rebel player has no points, all points go to the opponent then
            self.score[UNION] = 100

        elif self.score[UNION] == 0:
            # union player has no points, all points go to the opponent then
            self.score[REBEL] = 100

        else:
            # both player have at least some points
            self.score[REBEL] = int((float(self.score[REBEL]) / float(sum)) * 100)
            self.score[UNION] = int((float(self.score[UNION]) / float(sum)) * 100)

        print("EndGame.calculateScore: percentage: %d - %d" % (self.score[REBEL], self.score[UNION]))

    def createSummary(self):
        """
        This method creates a summary string that depends on the way the game ended. In most
        cases the calculated score in calculateScore() is used.
        """

        self.summary = ""

        # how did we end?
        type = scenario.end_game_type

        # special ending texts
        special = {constants.UNION_SURRENDER: 'The Union army surrenders',
                   constants.REBEL_SURRENDER: 'The Confederate army surrenders',
                   constants.UNION_DESTROYED: 'The Union army is destroyed',
                   constants.REBEL_DESTROYED: 'The Confederate army is destroyed',
                   constants.TIMEOUT: 'Time ran out - ',
                   constants.CEASE_FIRE: 'Cease fire called - '}

        # is the ending one that has a special text?
        if type in special:
            # yep, use it as a default text
            self.summary = special[type]

        # now, should we leave it at that?
        if type in [constants.UNION_SURRENDER, constants.REBEL_SURRENDER,
                    constants.UNION_DESTROYED, constants.REBEL_DESTROYED]:
            # yes, these types need no more explanation
            return

        # see the victory level
        rebelscore = self.score[REBEL]
        if rebelscore in range(75, 100):
            # rebel major victory
            self.summary += "Confederate major victory"

        elif rebelscore in range(60, 74):
            # rebel major victory
            self.summary += "Confederate minor victory"

        elif rebelscore in range(41, 59):
            # rebel major victory
            self.summary += "Draw"

        elif rebelscore in range(26, 40):
            # union minor victory
            self.summary += "Union minor victory"

        else:
            # union major victory
            self.summary += "Union major victory"
