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

from pattern.web import Twitter, Wikipedia, Bing, SEARCH

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter

from _textable.widgets.TextableUtils import *


class OWPatternWeb(OWWidget):
    """Orange widget to get corpus from pattern web"""
    
    # Widget settings declaration...
    settingsList = [
        'segment_label',
        'nb_tweet',
        'word_to_search',
        'autoSend',
        'operation',
        'displayAdvancedSettings',
        'licenseKey',
        'service',
        'wiki_section',
        'wiki_type_of_text'
        'nb_bing_entry'
        'language'
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
        self.segment_label = u'PatternWeb_data'
        self.nb_tweet = 50
        self.word_to_search = ''
        self.autoSend = False 
        self.displayAdvancedSettings = False
        self.licenseKey = ""
        self.service = u'Twitter'
        self.wiki_section = u'Yes'
        self.wiki_type_of_text = u'Plain text'
        self.nb_bing_entry = 50
        self.language = 'en'
        self.createdInputs = list()

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
            sendIfPreCallback= self.updateGUI,
            infoBoxAttribute='infoBox'
        )

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this 
        # class (here assigned to self.advancedSettings) contains two lists 
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.
        self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.toggle_AdvancedSettingg
        )
        #----------------------------------------------------------------------
        # User interface...
        
        # Advanced settings checkbox (basic/advanced interface will appear 
        # immediately after it...
        self.advancedSettings.draw()

        # key box (advanced settings only)
        advanceBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'',
            orientation='vertical',
        )

        keyInput = OWGUI.lineEdit(
            widget=advanceBox,
            master=self,
            value='licenseKey',
            orientation='horizontal',
            label=u'License key:',
            labelWidth=180,
        )

        segment_label_input = OWGUI.lineEdit(
            widget=advanceBox,
            master=self,
            value='segment_label',
            orientation='horizontal',
            label=u'Output segmentation label:',
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
        )
        
        OWGUI.comboBox(
            widget              = advanceBox,
            master              = self,
            value               = 'language',
            items               = ['en', 'fr'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Language:',
            labelWidth          = 130,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Select language."
            ),
        )


        # The following lines add keyBox (and a vertical separator) to the
        # advanced interface...
        self.advancedSettings.advancedWidgets.append(advanceBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()
        
        optionsBox = OWGUI.widgetBox(self.controlArea, 'Options')
        self.twitterBox = OWGUI.widgetBox(self.controlArea, 'Twitter')
        self.wikipediaBox = OWGUI.widgetBox(self.controlArea, 'Wikipedia')
        self.bingBox = OWGUI.widgetBox(self.controlArea, 'Bing')

        self.serviceBoxes = [self.twitterBox, self.wikipediaBox, self.bingBox]


        OWGUI.comboBox(
            widget              = optionsBox,
            master              = self,
            value               = 'service',
            items               = [u'Twitter', u'Wikipedia', u'Bing'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Service:',
            labelWidth          = 130,
            callback            = self.set_service_box_visibility,
            tooltip             = (
                    u"Select a service."
            ),
        )


        OWGUI.lineEdit(
            widget              = optionsBox,
            master              = self,
            value               = 'word_to_search',
            orientation         = 'horizontal',
            label               = u'Query:',
            callback            = self.sendButton.settingsChanged,
            labelWidth          = 131,
        )

        OWGUI.spin(
            widget=self.twitterBox,          
            master=self, 
            value='nb_tweet',
            label='Number of tweets:',
            tooltip='Select a number of tweet.',
            callback= self.sendButton.settingsChanged,
            min= 1, 
            max= 100, 
            step=1,
        )

        OWGUI.comboBox(
            widget              = self.wikipediaBox,
            master              = self,
            value               = 'wiki_section',
            items               = [u'Yes', u'No'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Separate in sections:',
            labelWidth          = 130,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Select wiki section separation."
            ),
        )

        OWGUI.comboBox(
            widget              = self.wikipediaBox,
            master              = self,
            value               = 'wiki_type_of_text',
            items               = [u'Plain text', u'HTML'],
            sendSelectedValue   = True,
            orientation         = 'horizontal',
            label               = u'Type of text:',
            labelWidth          = 130,
            callback            = self.sendButton.settingsChanged,
            tooltip             = (
                    u"Select type of text."
            ),
        )

        OWGUI.spin(
            widget=self.bingBox,          
            master=self, 
            value='nb_bing_entry',
            label='Number of entries:',
            tooltip='Select a number of entries.',
            callback= self.sendButton.settingsChanged,
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

        self.set_service_box_visibility()
        

        # Send data if autoSend.
        self.sendButton.sendIf()

        self.resize(10, 10)
        


    def get_tweets(self, search, nb):
        twitter = Twitter(language=self.language)
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
    
    def get_wiki_article(self, search, separate_in_section=u'Yes', type_of_text=u'Plain text'):
        segments = []
        article = Wikipedia(language=self.language).search(search, cached=False)
        if article:
            if separate_in_section == u'Yes':
                for section in article.sections:
                    if type_of_text == u'Plain text':
                        wiki_article = Input(section.string)
                    else:
                        wiki_article = Input(section.html)

                    annotations = {
                        'source' : 'Wikipedia',
                        'section title': section.title,
                        'section level': section.level,
                        'search' : search,
                    }
                    wiki_article.segments[0].annotations.update(annotations)
                    segments.append(wiki_article)
            else:
                if type_of_text == u'Plain text':
                    wiki_article = Input(article.string)
                else:
                    wiki_article = Input(article.html)
                annotations = {
                        'source' : 'Wikipedia',
                        'search' : search,
                    }
                wiki_article.segments[0].annotations.update(annotations)
                segments.append(wiki_article)
        return segments

    def get_bing_entries(self, search, nb):
        bing = Bing(language=self.language)
        entries = []
        for result in bing.search(search, start=1, count=nb, cached=False):
            entry_input = Input(result.text)
            annotations = {
                'source' : 'Bing',
                'title': result.title,
                'url': result.url,
                'search' : search,
            }
            entry_input.segments[0].annotations.update(annotations)
            entries.append(entry_input)
        return entries

    def sendData(self):
        """Compute result of widget processing and send to output"""

        if self.service == u'Twitter':
            segments = self.get_tweets(
                self.word_to_search,
                self.nb_tweet
            )

        elif self.service == u'Wikipedia':
            segments = self.get_wiki_article(
                self.word_to_search,
                self.wiki_section,
                self.wiki_type_of_text
            )

        elif self.service == u'Bing':
            segments = self.get_bing_entries(
                self.word_to_search,
                self.nb_bing_entry
            )

        # Clear created Inputs.
        self.clearCreatedInputs()

        # Initialize progress bar.
        progressBar = OWGUI.ProgressBar(
            self, 
            iterations=50
        )

        message = u'%i segment@p.' % len(segments)
        message = pluralize(message, len(segments))
        self.infoBox.dataSent(message)

        segmenter = Segmenter()
        out_object = segmenter.concatenate(segments, self.segment_label)
        a = 0
        while a < 50:
            progressBar.advance()   # 1 tick on the progress bar...
            a += 1

        # Clear progress bar.
        progressBar.finish()

        self.send('Text data', out_object, self)
        
        self.sendButton.resetSettingsChangedFlag()
        
    def updateGUI(self):  # si advanced settings est coche, alors cela l'affiche. 
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)

        self.infoBox.customMessage(u'Setting changed. Click send.')

        #if self.autoSend:
        #    self.sendData()

    def toggle_AdvancedSettingg(self):
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)


    def set_service_box_visibility(self):
        self.sendButton.settingsChanged()
        
        for serviceBox in self.serviceBoxes:
            serviceBox.setVisible(False)

        if self.service == u'Twitter':
            self.twitterBox.setVisible(True)

        elif self.service == u'Wikipedia':
            self.wikipediaBox.setVisible(True)

        elif self.service == u'Bing':
            self.bingBox.setVisible(True)

        self.updateGUI()

        #self.infoBox.dataSent('Debug: ' + self.service)
            

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

    def clearCreatedInputs(self):
        """Delete all Input objects that have been created."""
        # Delete strings...
        for i in self.createdInputs:
            i.clear()
        # Empty list of created inputs.
        del self.createdInputs[:]
        # Delete those created inputs that are at the end of the string store.
        for i in reversed(xrange(len(Segmentation.data))):
            if Segmentation.data[i] is None:
                Segmentation.data.pop(i)
            else:
                break

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWPatternWeb()
    myWidget.show()
    myApplication.exec_()
