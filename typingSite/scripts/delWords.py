from app.models import words

def run():
    # put the bad words in here
    bad_words =['sex' , 'gay' , 'fuck']
    for bad_word in bad_words:
        word = words.objects.filter(word__contains = bad_word)
        for w in word:
            print(w.word)
            w.delete()
