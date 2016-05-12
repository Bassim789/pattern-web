##################################
WebSearch
##################################



1 Signals
**************
Inputs : None

Outputs : WebSearch_data

2 Description
**************
The WebSearch widget is designed for the Orange Canvas environment to generate textual data retrieved from Twitter, Wikipedia or Bing. 
Depending on the service, the output segmentation has the following annotations with keys :

* Twitter : date, source, search, url and author.
* Wikipedia : source and search.
* Bing : url, source, search and title.

The interface of WebSearch adapts itself to the selected service. If the **Advanced settings** checkbox is selected, more options are revealed.

2.1 Basic Interface
**************
As stated before, the basic interface is dependant of the selected service. In case Twitter is chosen, the interface looks like this :

.. image:: img/twitter.png
Figure 1 : WebSearch widget with Twitter selected (basic interface)

The **Service** field allows the user to select a search engine (Twitter, Wikipedia or Bing).

The **Query** field contains the word(s) that is (are) going to be searched on the chosen web engine, in this example Twitter. 

By default, the **Output segmentation label** is named `WebSearch_data`. Users can however change it if needed. 

Clicking on the **Send** button executes the request. The **Info** box above indicates the number of segments sent if any matches the request.

2.1.1 Twitter
~~~~~~~~~~~~~~~~~~

2.2 Advanced Interface
**************
Once the **Advanced settings** checkbox is selected, a new box reveals itself on top of the window. It enables the user to enter a License key and choose the Language of the retrieved data. 
img

3. Message
**************
*Setting changed. Click send.*
This message informs the user that th settings have been changed and are ready to be sent. 

*Data correctly sent to output: <n> segments.*
The data, comprises of <n> number of segments has been sent to the output correctly.

*No data sent to output.*
The search didn't retrieve any data. When confronted to this message, the user should try to simplify the query.




