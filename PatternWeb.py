"""
<name>PatterWeb</name>
<description>Get corpus from pattern web</description>
<icon>path_to_icon.svg</icon>
<priority>11</priority> 
"""

# Standard imports...
import Orange
from OWWidget import *
import OWGUI
#from pattern.web import Twitter


class PatternWeb(OWWidget):
    """Orange widget to get corpus from pattern web"""
    


    # Widget settings declaration...
    settingsList = [
        'integer',
        'operation'
    ]  
    
    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        #----------------------------------------------------------------------
        # Channel definitions...
        self.inputs = [('Integer', str, 'debut')]     
        self.outputs = [('Integer', int)]

        #----------------------------------------------------------------------
        # Settings and other attribute initializations...
        self.integer = 0
        self.autoSend = True     
        self.loadSettings()
        
        self.inputData = None   # NB: not a setting.

        
        #----------------------------------------------------------------------
        # User interface...
        
        optionsBox = OWGUI.widgetBox(self.controlArea, 'Options')
        OWGUI.spin(
            widget=optionsBox,          
            master=self, 
            value='integer',
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
            tweets.append(tweet.text.encode('utf-8'))
        return tweets
        

    def sendData(self):
        """Compute result of widget processing and send to output"""
        # Important: if input data is None, propagate this value to output...
        
        result = 'test tweet'


        for tweet in self.get_tweets('suisse', 3):
            result = tweet + '\n\n'

        self.infoLine.setText(
            '%s' % (result)
        )
        self.send('Integer', result)

            


if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = PatternWeb()
    myWidget.show()
    myApplication.exec_()
    