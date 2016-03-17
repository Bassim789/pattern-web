"""
<name>PatternWeb</name>
<description>Get corpus from pattern web</description>
<icon>path_to_icon.svg</icon>
<priority>11</priority> 
"""

# Standard imports...
import Orange
from OWWidget import *
import OWGUI

from pattern.web import Twitter

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter

class PatternWeb(OWWidget):
    """Orange widget to get corpus from pattern web"""
    


    # Widget settings declaration...
    settingsList = [
        'nb_tweet',
        'word_to_search',
        'operation'
    ]  
    
    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        #----------------------------------------------------------------------
        # Channel definitions...
        #self.inputs = [('Integer', str, 'debut')]     
        #self.outputs = [('Text data', Segmentation)]
        self.outputs = [('Text data', Segmentation)]

        

        #----------------------------------------------------------------------
        # Settings and other attribute initializations...
        self.nb_tweet = 3
        self.word_to_search = ''
        self.autoSend = True     
        self.loadSettings()
        
        self.inputData = None   # NB: not a setting.

        
        #----------------------------------------------------------------------
        # User interface...
        
        optionsBox = OWGUI.widgetBox(self.controlArea, 'Options')

        OWGUI.lineEdit(
                widget              = optionsBox,
                master              = self,
                value               = 'word_to_search',
                orientation         = 'horizontal',
                label               = u'Recherche:',
                labelWidth          = 131,
        )

        OWGUI.spin(
            widget=optionsBox,          
            master=self, 
            value='nb_tweet',
            label='Nombre de tweet:',
            tooltip='Select a number of tweet.',
            min= 1, 
            max= 100, 
            step=1,
        )


        OWGUI.button(
            widget=optionsBox,
            master=self,
            label='Get tweet',
            callback=self.sendData,
        )
        
        infoBox = OWGUI.widgetBox(self.controlArea, u'Info')
        self.infoLine = OWGUI.widgetLabel( # NB: using self here enables us to
                                           # access the label in other methods.
            widget=infoBox,              
            label='No input.',
        )

        self.resize(10, 10)
        


    def get_tweets(self, search, nb):
        
        twitter = Twitter()
        tweets = []
        for tweet in twitter.search(search, start=1, count=nb):
            tweet_input = Input(tweet.text)
            annotations = {
            	'source' : 'Twitter',
		        'author': tweet.author,
		        'date': tweet.date,
		        'url': tweet.url,
		        'search' : search,
		    }
            tweet_input.segments[0].annotations.update(annotations)
            tweets.append(tweet_input)
        return tweets
        

    def sendData(self):
        """Compute result of widget processing and send to output"""

        segments = []

        # add tweets
        segments += self.get_tweets(
        	self.word_to_search,
        	self.nb_tweet
        )

        self.infoLine.setText(
            '%i segments' % (len(segments))
        )

        segmenter = Segmenter()
        out_object = segmenter.concatenate(segments)

        self.send('Text data', out_object, self)

            

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = PatternWeb()
    myWidget.show()
    myApplication.exec_()
    
