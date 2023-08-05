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

import pygame

from civil.ui import properties_audio


class AudioManager:
    """
    This class is the central handler for all audio in Civil. It takes care of:

    * initializing the audio subsystem
    * loading samples from disk
    * loading music from disk
    * playing samples and music
    * pausing the music

    * checking for an audio CD
    * playing, stopping and pausing audio CD playing
    * ejecting the CD tray

    If no audio is available all operations are dummy operations and samples are just never
    played. Thus the 'clients' of this interface need never worry about weather audio is avilable or
    not, they just play samples and music without worrying about that.
    """

    def __init__(self):
        """
        Initializes the audio manager. Checks weather audio can be used at all, and if it can
        determines and sets up parameters.
        """

        # try to init audio
        try:
            # if this succeeds we assume audio is present, otherwise not
            pygame.mixer.init()

            # get the number of channels
            self.channels = pygame.mixer.get_num_channels()

            # we do have audio but no music
            self.audio = 1
            self.music = 0
            self.playing = 0
            self.paused = 0
            self.paused_cd = 0

            # no samples loaded yet
            self.loadedsamples = {}

        except:
            # no channels and no audio
            self.channels = 0
            self.audio = 0
            self.music = 0
            self.playing = 0
            self.playing_cd = 0
            self.paused = 0
            self.paused_cd = 0

        # try to init CD audio
        try:
            # if this succeeds we assume a CD with audio is present in the cd drive, otherwise not
            pygame.cdrom.init()

            # check for an audio cd
            if not self.checkForAudioCD():
                # no audio cd
                raise RuntimeError("not an audio cd")

            self.audio_cd = 1
            self.playing_cd = 0
            self.paused_cd = 0
            self.track = 0

        except:
            # no cd or no cd with audio
            self.audio_cd = 0
            self.playing_cd = 0
            self.paused_cd = 0
            self.track = 0

        # print some info
        if self.audio:
            print("audio: %d sound channels available" % self.channels)
        else:
            print("audio: no audio detected")

        if self.audio_cd:
            print("audio: found audio CD with %d tracks" % self.cd.get_numtracks())
        else:
            print("audio: no audio CD found")

    def getNumChannels(self):
        """
        Returns the number of audio channels available. This is 0 if no audio is available at
        all.
        """
        return self.available

    def disableAudio(self):
        """
        Disables audio even if audio is available. This can be used for instance if a commandline
        option has been given.
        """
        self.audio = 0

    def hasAudio(self):
        """
        Returns 1 if audio is available and 0 if not.
        """
        return self.audio

    def playSample(self, sample):
        """
        Plays a sample. If no audio is available this method does nothing. If the sample is not
        already loaded then it will be loaded, stored and then played.
        """

        # do we have audio at all?
        if not self.audio:
            # no, go away
            return

        # do we already have the sample loaded
        if sample not in self.loadedsamples:
            # nope, get the file_name for that logical name
            try:
                name = properties_audio.samplenames[sample]
            except KeyError:
                # no such sample
                raise RuntimeError("AudioManager.playSample: no such sample: '%s'" % sample)

                # all ok so far, load the sample
            try:
                sampledata = pygame.mixer.Sound(name)
            except pygame.error:
                print("*** Couldn't play sound:", name)
                return

            # store it in our cache
            self.loadedsamples[sample] = sampledata

        else:
            # it's loaded, just get it
            sampledata = self.loadedsamples[sample]

        # play the sample
        sampledata.play()

    def loadMusic(self, music):
        """
        Loads 'music' as the background music. Does not yet start playing it. Only one music can
        be loaded at one time, so calling this method repeatedly overwrites the current
        music. Nothing is returned, as the music is stored internally. If audio is not enabled this
        method does nothing.
        """

        # do we have audio or musicat all?
        if not self.audio:
            # no, go away
            return

        # are we playing already?
        if self.playing:
            # yes, stop it
            print("AudioManager.loadMusic: stopping old music")
            self.stopMusic()

        # load it
        try:
            print("AudioManager.loadMusic: about to load music: " + music)
            pygame.mixer.music.load(music)

            # now we have music
            self.music = 1

        except:
            # failed?
            print("AudioManager.loadMusic: failed to load: " + music)

            # no music available
            self.music = 0

        print("AudioManager.loadMusic: loaded music: " + music)

    def playMusic(self):
        """
        Plays the current music. If audio is not enabled this method does nothing. If audio is
        enabled but music is not loaded using the method 'loadMusci()' then a warning is printed.
        """

        # do we have audio or musicat all?
        if not self.audio:
            # no, go away
            return

        # do we have music loaded?
        if not self.music:
            # no music?
            print("AudioManager.playMusic: no music loaded, can't play")
            return

        # play music
        pygame.mixer.music.play()

        # we're playing now
        self.playing = 1

    def stopMusic(self):
        """
        Stops playing music if it is playing. Does nothing if no mucis is playing or if there is
        no audio available.
        """

        # do we have audio or music at all?
        if not self.audio or not self.music:
            # no, go away
            return

        # stop music
        pygame.mixer.music.stop()

        # we're stopped now
        self.playing = 0

    def pauseMusic(self):
        """
        Pauses playing music if it is playing. Does nothing if no music is playing or if there is
        no audio available.
        """

        # do we have audio or music at all?
        if not self.audio or not self.music:
            # no, go away
            return

        # are we paused?
        if self.paused:
            # yep, go away
            return

        # pause music
        pygame.mixer.music.pause()

        # we're paused now
        self.paused = 1

    def unpauseMusic(self):
        """
        Resumes playing music if it is paused. Does nothing if no music is already playing or if
        there is no audio available.
        """

        # do we have audio or music at all?
        if not self.audio or not self.music:
            # no, go away
            return

        # are we not paused?
        if not self.paused:
            # nope, go away
            return

        # pause music
        pygame.mixer.music.unpause()

        # we're not paused anymore
        self.paused = 0

    def fadeoutMusic(self, milliseconds):
        """
        Fades out the music to silent over a period of 'milliseconds'. If no music is playing or
        no audio is used this method does nothing.
        """

        # do we have audio or music at all?
        if not self.audio or not self.music or not self.playing:
            # no, go away
            return

        # fade out the music
        pygame.mixer.music.fadeout(milliseconds)

    def isPlaying(self):
        """
        Returns 1 if we're currently playing music. It returns 1 even if we're currently
        paused. It mainly means that 'playMusic()' was called later than 'stopMusic()'. Returns 0 if
        music is not playing.
        """
        return self.playing

    def isPaused(self):
        """
        Returns 1 if we're currently playing music but paused.  Returns 0 if not paused.
        """
        return self.paused

    def checkForAudioCD(self):
        """
        Checks the drive for an audio CD. Returns 1 if found and None of not. Stores the CD
        object internally if ok.
        """

        # precautions
        if pygame.cdrom.get_count() == 0:
            # no cd
            return 0

        # init the cd by creating a CD class and initializing it
        self.cd = pygame.cdrom.CD(0)
        self.cd.init()

        # does it have any tracks at all?
        if self.cd.get_numtracks() == 0:
            # no tracks, can't play
            return 0

        # loop over all tracks
        for index in range(self.cd.get_numtracks()):
            # is this an audio track?
            if not self.cd.get_track_audio(index):
                # not an audio track, not an audio cd
                return 0

        # we got this far, so it has to be an audio cd, as all tracks are audio, and there is at
        # least one track
        return 1

    def hasAudioCD(self):
        """
        Returns 1 if an audio CD is available and 0 if not.
        """
        return self.audio_cd

    def isPlayingCD(self):
        """
        Returns 1 if we're currently playing music from an audio CD. It returns 1 even if we're
        currently paused. It mainly means that 'playMusicCD()' was called later than
        'stopMusicCD()'. Returns 0 if CD music is not playing.
        """
        return self.playing_cd

    def playCD(self):
        """
        Starts playing the CD from the current track. If no audio CD has been found or we are
        already playing a CD nothing will be done.
        """
        # do we have an audio cd available or are we already playing?
        if not self.audio_cd or self.playing_cd:
            # no, go away
            return

        # start playing the current track
        self.cd.play(self.track)

        # we're playing now
        self.playing_cd = 1

    def stopCD(self):
        """
        Stops playing an audio CD if one is available and we are currently playing one.
        """
        # do we have an audio cd available or are we already stopped?
        if not self.audio_cd or not self.playing_cd:
            # no, go away
            return

        # stop playing
        self.cd.stop()

        # we're not playing now
        self.playing_cd = 0

    def pauseCD(self):
        """
         """
        # do we have an audio cd available?
        if not self.audio_cd:
            # no, go away
            return

    def unpauseCD(self):
        """
         """
        # do we have an audio cd available?
        if not self.audio_cd:
            # no, go away
            return

    def nextTrackCD(self):
        """
        Starts playing the next track of the cd. Stops playing if we've come to the end of the
        cd.
        """
        # do we have an audio cd available?
        if not self.audio_cd:
            # no, go away
            return

        # next track
        self.track += 1

        # too far?
        if self.track == self.cd.get_numtracks():
            # yep, stop playing
            self.stopCD()

            # and let the last track be the max
            self.track -= 1

    def prevTrackCD(self):
        """
        Starts playing the previous track of the cd. Starts from track 0 if we've come to the
        beginning of the cd.
        """
        # do we have an audio cd available?
        if not self.audio_cd:
            # no, go away
            return

        # decrement the track
        self.track -= 1

        # too far?
        if self.track == -1:
            # yep, go to the first track
            self.track = 0

    def ejectCD(self):
        """
        Ejects the CD tray if possible. If we are currently playing CD music it is of course
        stopped first.
        """
        try:
            # are we playing and audio cd right now?
            if self.playing_cd:
                # yes, stop playing
                self.stopCD()

            # eject the cd
            self.cd.eject()

        except:
            # failed to eject the cd
            pass
