import speech_recognition as sr
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening")
    audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")

list_commands = set(["forward","stop","left","right","do","transport"])
list_actions = ['take','drop']
list_products = ['stick','planck']

next_command = {'do': list_actions, 'tranport':list_products}

# recognized_text = 'go forth'

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

tokens = nltk.tokenize.word_tokenize(recognized_text)
print(tokens)

radicals = [stemmer.stem(token) for token in tokens]
print(radicals)

radic = [lemmatizer.lemmatize(token, wordnet.VERB) for token in radicals]

print(radic)
radic = set(radic)

detected_commands = radic.intersection(list_commands)
if len(detected_commands)>0:
    detected_command = detected_commands.pop()
    print(f'Command detected: {detected_command}')

    if detected_command in next_command:
        detected_follow_ups = radic.intersection(next_command[detected_command])
        if len(detected_follow_ups)>0:
            detected_follow_up = detected_follow_ups.pop()
            print(f'Follow up command is: {detected_follow_up}')