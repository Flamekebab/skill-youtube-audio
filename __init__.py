from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from  mycroft.util import wait_while_speaking

from bs4 import BeautifulSoup
import urllib.request
from os.path import join, isfile, abspath, dirname
from mycroft.skills.audioservice import AudioService
from rm import rm
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
        #define some variables, if I understand the syntax...
        self.search = ""
        self.url = ""

    def getResults(self, search, pos=0):
	#Let's use urllib to perform a query
        query = urllib.parse.quote(search)
        link = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(link)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        vids = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
        ytURL = 'https://www.youtube.com' + vids[pos]['href']
        return ytURL

    def initialize(self):
	#Here we give the intent builder a pattern to follow. First we're telling it to require a keyword, then it'll need a query
	#The query isn't pulled from a .voc file - instead we use Regex, because we hate ourselves.
	#As a result there's a folder, much like the vocab folder, which contains the regex pattern (in this case search_query.rx).
        play_video_audio_intent = IntentBuilder("PlayYoutubeAudioIntent").require("play_youtube_audio").require("search_query").build()
        # /\ This bit tells the skill which vocab file it needs so that users can make it work
        self.register_intent(play_video_audio_intent, self.play_video_audio_intent)
        #We'll be using the audio service to play the resulting audio so we need to initialise it here, or something
        self.audio_service = AudioService(self.bus)

    def play_video_audio_intent(self, message):
        #the full utterance can be accessed like this: message.data.get('utterance')
	#Remember that search_query.rx file from earlier? If we want the contents of the query we supplied we can get it using message.data.get("search_query")
        #self.speak_dialog(message.data.get("search_query"))

        ytURL = self.getResults(message.data.get("search_query"))

        #It takes a moment for the command to be processed so probably best to prompt them!
        self.speak_dialog("downloading")
        #Get Sultan running that command
        sultan = Sultan()
        #first we remove any existing output file:
        rm("/tmp/output.wav")
        #ytURL = "https://www.youtube.com/watch?v=IPXIgEAGe4U"
        #double underscores are needed for the syntax here - they're an equivalent of a hyphen
        sultan.youtube__dl("-x  --audio-format wav -o '/tmp/output.%(ext)s' " + ytURL).run()
        #Then we use the audio service to play our file:
        self.audio_service.play('file:///tmp/output.wav')

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
