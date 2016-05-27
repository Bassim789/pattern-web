from _textable.widgets.LTTL.Segmenter import Segmenter
from operator import itemgetter

def main():
        
    unsignifiant_fr = [
        'de', 'des', 'du', 'un', 'une', 'le', 'la', 'les',
        '-', 'et', '', 'en', 'au', 'sur', 'pour', u'\xe0',
        '!', '.', '?', ','
    ]
    
    unsignifiant = unsignifiant_fr
 
    word_dict = {}
    for segment in in_object:
        segment_content = segment.get_content()
        searched = segment.annotations['search'].lower()
        for word in segment_content.split(' '):
            if word.lower() not in unsignifiant and not word.lower() == searched:
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1

    count = 0
    for word in sorted(word_dict, key=word_dict.get, reverse=True):
        count += 1
        print word + ': ' + str(word_dict[word])
        if count == 10:
            break


if __name__ == "__builtin__":
    if in_object:
        main()
