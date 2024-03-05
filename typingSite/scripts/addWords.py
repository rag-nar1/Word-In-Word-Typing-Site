from app.models import words , characters




def get_alphabetical_order(char):
    return ord(char) - ord('a') + 1


# process word and make an entry in database
def processWord(word):
    word = word.lower()
    freq = {}
    for char in word:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    # sort the dictionary by value
    freq = sorted(freq.items() , key=lambda x: x[1] , reverse=True)
    most_freq1 = freq[0][0]
    if(len(freq) == 1):
        most_freq2 = most_freq1
        most_freq3 = most_freq1
    elif(len(freq) == 2):
        most_freq2 = freq[1][0]
        most_freq3 = most_freq1
    else:
        most_freq2 = freq[1][0]
        most_freq3 = freq[2][0]
    id1 = get_alphabetical_order(most_freq1)
    id2 = get_alphabetical_order(most_freq2)
    id3 = get_alphabetical_order(most_freq3)
    word = words(   word=word,
                    most_freq_char=characters.objects.get(id=id1),
                    most_freq_char2=characters.objects.get(id=id2),
                    most_freq_char3=characters.objects.get(id=id3),
                    used_cnt=0
                 )
    word.save()


# add words to database
def addWords(wordslist):
    for word in wordslist:
        processWord(word)


def addChars():
    for i in range(1,27):
        char = characters( char=chr(i+96) , id=i )
        char.save()

# read words from files
def run():
    f1 = open("words/long.txt" , "r")
    f2 = open("words/medium.txt" , "r")
    f3 = open("words/short.txt" , "r")
    longWords = f1.read().strip().split("\n")
    mediumWords = f2.read().strip().split("\n")
    shortWords = f3.read().strip().split("\n")
    addChars()
    addWords(shortWords)
    addWords(mediumWords)
    addWords(longWords)
    f1.close()
    f2.close()
    f3.close()


