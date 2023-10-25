import speech_recognition as sr
import spacy

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
                

# handle sentences such as "Fait trois objets de type 2"
def handle_object_number():
    # if no number and no object are specified, create the object 0 once
    default_object_id = 0
    default_object_number = 1

    # get the type of each word
    pos_words = [token.pos_ for token in tokens]
    number_numbers = pos_words.count('NUM')
    object_index = radical.index('objet')

    if number_numbers >0:
        num1_index = pos_words.index('NUM')
        # if there only is one number in the sentence
        if number_numbers == 1:
            number = tokens[num1_index]

            # if the number is after the object, its the id, otherwise it is the number
            if object_index<num1_index:
                default_object_id = transform_to_number(number.text)
            else:
                default_object_number = transform_to_number(number.text)

        # if there is 2 numbers in the sentence
        elif (number_numbers == 2):
            num2_index = pos_words[num1_index+1:].index('NUM')+ num1_index + 1

            # if one number is before and the other is after, set the corresponding values
            if (num1_index < object_index < num2_index):
                default_object_id = transform_to_number(tokens[num2_index].text)
                default_object_number = transform_to_number(tokens[num1_index].text)
        print(f'Creating {default_object_number} objet{"s" if default_object_number>1 else ""} with id {default_object_id}')

def get_distance(detected_command):
    if detected_command in ["avancer","reculer"]:
        distance = 0.1 # go forward by 10 centimeters by default
    else:
        distance = 90 # turn 90° by default

    # if there is a number in the sentence, extract it
    pos_words = [token.pos_ for token in tokens]
    number_numbers = pos_words.count('NUM')
    if(number_numbers == 1):
        number = str(tokens[pos_words.index('NUM')]).replace(",",".")
        distance = float(number)

    return distance

# listen to the mic and transform any loud sound it to a text
def get_input_text(trigger = False):
    with sr.Microphone() as source:
        print(f'Listening {"for trigger word" if trigger  else ""}')
        audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            print("Could not understand audio")
            recognized_text = ''

    return recognized_text

def calibrate_noise():
    print("Calibrating, don't make any noise")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels


##==========================PARAMETERS=====================================

# elements to detect
list_commands = ["reculer","avancer","stopper","gauche","droite","faire","transporter"]
list_actions = ['prendre','déposer','objet']
list_products = ['bâton','planche']
trigger_words = "ok google"

# synonym dictionary
synonyms_dict = {
    "avancer":['devant','avant'],
    'stopper': ["arrêter","arrêt"],
    'faire': ['effectuer','fabriquer'],
    'transporter': ['déplacer'],
    'gauche': ['bâbord'],
    'droite': ['tribord'],
    "reculer": ["arrière"]
}

follow_up_command = {'faire': list_actions, 'transporter':list_products}

##==========================================================================

# Initial loading
list_all_commands = add_synonyms_to_commands()
nlp = spacy.load('fr_core_news_md') # load french library
recognizer = sr.Recognizer()
calibrate_noise() # adapt the sound threshold to the ambient noise

while True:
    recognized_text = get_input_text(trigger=True)

    # if the tiger world is in the list of words
    if(trigger_words in recognized_text.lower()):

        # Get actual command
        recognized_text = get_input_text()
        print(f'Google understood: {recognized_text}')

        # tokenise it
        tokens = nlp(recognized_text) 

        # transform to radicals
        radical = [token.lemma_ for token in tokens]

        #get intersection of the list of commands and the radicals
        detected_commands = set(radical).intersection(list_all_commands) 
        
        # if there is a matching command
        if len(detected_commands)>0: 
            detected_command = detected_commands.pop()

            # get the original word if it was one of the synonyms
            detected_command = get_original_word(detected_command)
            print(f'Command detected: {detected_command}')

            # check if this command have a follow up command
            if detected_command in follow_up_command:
                detected_follow_ups = set(radical).intersection(follow_up_command[detected_command])

                # if there is a follow up command, extract it
                if len(detected_follow_ups)>0:
                    detected_follow_up = detected_follow_ups.pop()
                    print(f'Follow up command is: {detected_follow_up}')
                    if detected_follow_up=='objet':
                        handle_object_number()

            if detected_command in ["droite","gauche","avancer","reculer"]:
                distance = get_distance(detected_command)
