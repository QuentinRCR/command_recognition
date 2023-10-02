import speech_recognition as sr
import spacy

# elements to detect
list_commands = set(["avancer","stopper","gauche","droite","faire","transporter"])
list_actions = ['prendre','déposer']
list_products = ['bâton','planche']


follow_up_command = {'faire': list_actions, 'transporter':list_products}

# language processing
nlp = spacy.load('fr_core_news_md')

# Speech to text
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening")
    audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="fr-FR")
    except sr.UnknownValueError:
        print("Could not understand audio")


#tokenise
tokens = nlp(recognized_text) 
print(tokens)

# transform to radicals
radical = [token.lemma_ for token in tokens] 
print(radical)


radical = set(radical)
detected_commands = radical.intersection(list_commands) #get intersection 

if len(detected_commands)>0: # if there is a matching command
    detected_command = detected_commands.pop()
    print(f'Command detected: {detected_command}')


    if detected_command in follow_up_command: # check if this command have a follow up command
        detected_follow_ups = radical.intersection(follow_up_command[detected_command])
        if len(detected_follow_ups)>0:
            detected_follow_up = detected_follow_ups.pop()
            print(f'Follow up command is: {detected_follow_up}')