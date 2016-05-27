from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Input import Input

def main():
    global out_object
    
    unsignifiant = []
    
    unsignifiant_fr = [
        'de', 'des', 'du', 'un', 'une', 'le', 'la', 'les', 'd', 'l', 'a', 'ou', 'dans', 'par', 'ce', 'cette',
        '-', 'et', '', 'en', 'au', 'sur', 'pour', u'\xe0',
        'est', 'se', 'qui', 'plus', 'avec', 's', 'entre', 'son', 'elle', 'il', 'que', 'ne', 'sont', 'sa', 'ses',
        '!', '.', '?', ','
    ]
    
    unsignifiant_wiki_fr = ['code', 'modifier']
    
    unsignifiant.extend(unsignifiant_fr)
    unsignifiant.extend(unsignifiant_wiki_fr)
    
    filtredInputs = []
 
    for segment in in_object:
        word = segment.get_content()
        if word.lower() not in unsignifiant:
            filtredInputs.append(Input(word, label=False))
        
    segmenter = Segmenter() 
    out_object = segmenter.concatenate(filtredInputs)
    print out_object.to_string()
            
if __name__ == "__builtin__":
    if in_object:
        main()
