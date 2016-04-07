"""
<name>PatternWeb</name>
<description>Get corpus from pattern web</description>
<icon>icons/icon_p.png</icon>
<priority>11</priority> 
"""

__version__ = '0.0.1'

# Standard imports...
import Orange
from OWWidget import *
import OWGUI

from pattern.web import Twitter

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter

from _textable.widgets.TextableUtils import *


class OWPatternWeb(OWWidget):
    """Orange widget to get corpus from pattern web"""
    


    # Widget settings declaration...
    settingsList = [
        'nb_tweet',
        'word_to_search',
        'operation',
        'displayAdvancedSettings',
        'licenseKey'
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
        self.displayAdvancedSettings = False
        self.licenseKey = ""

        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        
        self.inputData = None   # NB: not a setting.

        # Next two instructions are helpers from TextableUtils. Corresponding
        # interface elements are declared here and actually drawn below (at
        # their position in the UI)...
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox',
            sendIfPreCallback=self.updateGUI,
        )

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this 
        # class (here assigned to self.advancedSettings) contains two lists 
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.
        self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.sendButton.settingsChanged,
        )
        #----------------------------------------------------------------------
        # User interface...
        
        # Advanced settings checkbox (basic/advanced interface will appear 
        # immediately after it...
        self.advancedSettings.draw()

        # key box (advanced settings only)
        keyBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Web service license key',
            orientation='vertical',
        )

        keyBoxCombo = OWGUI.lineEdit(
            widget=keyBox,
            master=self,
            value='licenseKey',
            orientation='horizontal',
            label=u'License key:',
            labelWidth=180,
        )
        


        # The following lines add keyBox (and a vertical separator) to the
        # advanced interface...
        self.advancedSettings.advancedWidgets.append(keyBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        
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


        # OWGUI.button(
        #     widget=optionsBox,
        #     master=self,
        #     label='Get tweet',
        #     callback=self.sendData,
        # )
        
        # Now Info box and Send button must be drawn...
        self.infoBox.draw()
        self.sendButton.draw()
        

        # Send data if autoSend.
        self.sendButton.sendIf()

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

        message = u'%i segment@p.' % len(segments)
        message = pluralize(message, len(segments))
        self.infoBox.dataSent(message)

        segmenter = Segmenter()
        out_object = segmenter.concatenate(segments)

        self.send('Text data', out_object, self)
        
    def updateGUI(self):  # si advanced settings est coche, alors cela l'affiche. 
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            

    def getSettings(self, *args, **kwargs):
        """Read settings, taking into account version number (overriden)"""
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings["settingsDataVersion"] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        """Write settings, taking into account version number (overriden)"""
        if settings.get("settingsDataVersion", None) \
                == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings["settingsDataVersion"]
            OWWidget.setSettings(self, settings)

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = PatternWeb()
    myWidget.show()
    myApplication.exec_()
    
