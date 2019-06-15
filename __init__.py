from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from  mycroft.util import wait_while_speaking
from mycroft.util import play_wav, play_mp3
from os.path import join, isfile, abspath, dirname

from sultan.api import Sultan

__author__ = 'Flamekebab'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class YoutubeAudioSkill(MycroftSkill):

    # The constructor of the skill, which calls Mycroft Skill's constructor
    def __init__(self):
        super(YoutubeAudioSkill, self).__init__(name="YoutubeAudioSkill")

    def initialize(self):
	#This bit tells the skill which vocab file it needs so that users can make it work
        play_video_audio_intent = IntentBuilder("PlayYoutubeAudioIntent"). \ 
                require("play_youtube_audio").build()
        self.register_intent(play_video_audio_intent, self.play_video_audio_intent)

    def play_video_audio_intent(self, message):
        #It takes a moment for the command to be processed so probably best to prompt them!
        self.speak_dialog("downloading")
        #Get Sultan running that command
        sultan = Sultan()
        ytURL = "https://www.youtube.com/watch?v=IPXIgEAGe4U"
        sultan.youtube-dl("-x  -o \"output.opus\" " + ytURL).run()
        sultan.vlc("output.opus").run()

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return YoutubeAudioSkill()

