from tkinter import *
from tkinter import ttk
from googletrans import Translator, LANGUAGES
import speech_recognition as spr
from gtts import gTTS
import os
import threading


def recognize_speech(recog, mc):
    try:
        with mc as source:
            print("Speak 'Hello' to initiate the Translation!")
            print("~~")
            recog.adjust_for_ambient_noise(source, duration=0.2)
            audio = recog.listen(source)
            my_text = recog.recognize_google(audio)
            return my_text.lower()
    except spr.UnknownValueError:
        print("Unable to Understand the Input")
    except spr.RequestError as e:
        print("Unable to provide Required Output: {}".format(e))
    return None


def translate_text(recog, mc, src_lang, dest_lang):
    try:
        translator = Translator(service_urls=['translate.googleapis.com'])

        with mc as source:
            print("Speak a sentence...")
            recog.adjust_for_ambient_noise(source, duration=0.2)
            audio = recog.listen(source)
            get_sentence = recog.recognize_google(audio)

        print("Phrase to be Translated: " + get_sentence)
        text_to_translate = translator.translate(
            get_sentence, src=src_lang.get(), dest=dest_lang.get())
        text = text_to_translate.text
        print(text)

        speak = gTTS(text=text, lang="en", slow=False)
        speak.save("captured_voice.mp3")

        os.system("start captured_voice.mp3")

        return text
    except spr.UnknownValueError:
        print("Unable to Understand the Input")
    except spr.RequestError as e:
        print("Unable to provide Required Output: {}".format(e))
    return None


def on_translate_button_click():
    clear_output_text()
    threading.Thread(target=translate_worker).start()


def translate_worker():
    my_text = recognize_speech(recog1, mc)
    if my_text and 'hello' in my_text:
        translated_text = translate_text(recog1, mc, src_lang, dest_lang)
        if translated_text:
            Output_text.insert(END, translated_text)


def clear_output_text():
    Output_text.delete(1.0, END)


root = Tk()
root.geometry('1080x600')
root.resizable(0, 0)
root.config(bg='#eeebdd')
root.title("SPEECH TRANSLATOR")

Label(root, text="LINGUA - The Speech Translator", fg="#1b1717",
      font="century 20 italic", bg='#eeebdd', width=30, ).pack()
Label(root, text="AD-1 PROJECT", fg="#800000", font=("Lucida",
      20, "roman"), width=20, bg='#eeebdd').pack(side='bottom')

Label(root, text="->Select your language to translate", font='calibri 14 italic', fg="#1b1717", bg='#eeebdd').place(x=10,
                                                                                                                    y=130)

src_lang = ttk.Combobox(root, values=list(
    LANGUAGES.values()), width=21, font="Verdana 12 bold")
src_lang.place(x=20, y=60)
src_lang.set('choose input language')

dest_lang = ttk.Combobox(root, values=list(
    LANGUAGES.values()), width=21, font="Verdana 12 bold")
dest_lang.place(x=790, y=60)
dest_lang.set('choose output language')

Output_text = Text(root, font='Times 20 italic', height=7, wrap=WORD, padx=5, pady=5, width=32, borderwidth=3,
                   relief="solid")
Output_text.place(x=600, y=100)

trans_btn = Button(root, text='Translate', font='monaco 10 normal', pady=5, command=on_translate_button_click,
                   fg='#FFFFFF', activebackground='#FFD700', bg='#810000', borderwidth=3, relief="solid")
trans_btn.place(x=500, y=180)

# Speech recognition setup
recog1 = spr.Recognizer()
mc = spr.Microphone()

root.mainloop()
