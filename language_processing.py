import speech_recognition as sr
import spacy
import time

def get_original_word(synonym):
    if synonym in synonyms_dict.keys():
        return synonym
    for original_word, synonyms in synonyms_dict.items():
        if synonym in synonyms:
            return original_word
    return None

def add_synonyms_to_commands():
    command_copy = list_commands[:]
    for list_syn in synonyms_dict.values():
        command_copy += list_syn
    return set(command_copy)

def transform_to_number(value):
    if value.isdigit():
        return int(value)
    else:
        match value.lower():
            case 'un':
                return 1
            case 'deux':
                return 2
            case 'trois':
                return 3
            case 'quatre':
                return 4
            case 'cinq':
                return 5
            case 'six':
                return 6
                

def handle_object_number():
    pos_words = [token.pos_ for token in tokens]
    if ('NUM' in pos_words) and (pos_words.index('NUM')>[token.text for token in tokens].index('objet')):
        number = tokens[pos_words.index('NUM')]
        print(f'The number of the object is: {transform_to_number(number.text)}')


def get_audio(trigger = False):
    with sr.Microphone() as source:
        print(f'Listening {"for trigger word" if trigger  else ""}')
        audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            print("Could not understand audio")
            recognized_text = ''

    return recognized_text


##==========================PARAMETERS=====================================

# elements to detect
list_commands = ["avancer","stopper","gauche","droite","faire","transporter"]
list_actions = ['prendre','déposer','objet']
list_products = ['bâton','planche']
trigger_words = "ok google"

synonyms_dict = {
    "avancer":['devant'],
    'stopper': ["arrêter","arrêt"],
    'faire': ['effectuer','fabriquer'],
    'transporter': ['déplacer'],
    'gauche': ['bâbord'],
    'droite': ['tribord']
}

follow_up_command = {'faire': list_actions, 'transporter':list_products}

##==========================================================================

# Initial loading
list_all_commands = add_synonyms_to_commands()
nlp = spacy.load('fr_core_news_md')
recognizer = sr.Recognizer()

i=0
while i==0:
    i+=1
    time.sleep(1)
    # recognized_text = get_audio(trigger=True)
    recognized_text = "ok google fait l'objet 3"
    print(recognized_text)
    if(trigger_words in recognized_text.lower()):

        # Speech to text
        # recognized_text = get_audio()

        #tokenise
        tokens = nlp(recognized_text) 
        print(tokens)

        # transform to radicals
        radical = set([token.lemma_ for token in tokens]) 

        print(radical)

        detected_commands = radical.intersection(list_all_commands) #get intersection 

        if len(detected_commands)>0: # if there is a matching command
            detected_command = detected_commands.pop()

            detected_command = get_original_word(detected_command)
            print(f'Command detected: {detected_command}')


            if detected_command in follow_up_command: # check if this command have a follow up command
                detected_follow_ups = radical.intersection(follow_up_command[detected_command])
                if len(detected_follow_ups)>0:
                    detected_follow_up = detected_follow_ups.pop()
                    print(f'Follow up command is: {detected_follow_up}')
                    if detected_follow_up=='objet':
                        handle_object_number()