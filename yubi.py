import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import webbrowser
import tempfile
import requests
import re

# Speak Function
def speak(text):
    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            path = fp.name
        tts.save(path)
        playsound(path)
    except Exception as e:
        messagebox.showerror("Voice Error", f"BOLNE mein dikkat aayi: {e}")

# Search and Play Function using regex
def search_youtube_and_play(query):
    try:
        search_url = f"https://www.youtube.com/results?search_query={query}"
        response = requests.get(search_url)
        video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
        if video_ids:
            video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
            webbrowser.open(video_url)
        else:
            speak("Koi video nahi mili.")
            result_label.config(text="Koi video nahi mili.")
    except Exception as e:
        messagebox.showerror("Search Error", str(e))
        result_label.config(text="Search karne mein dikkat aayi.")

# Listen Function
def start_listening():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        result_label.config(text="Sun rahi hoon...")
        window.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language="en-IN")
            result_label.config(text=f"Aapne kaha: {query}")
            speak(f"Aapne kaha {query}. Main YouTube par dhoondh rahi hoon.")
            search_youtube_and_play(query)
        except sr.WaitTimeoutError:
            result_label.config(text="Kuch suna nahi gaya.")
            speak("Kuch suna nahi gaya. Dobara boliye.")
        except sr.UnknownValueError:
            result_label.config(text="Samajh nahi paayi.")
            speak("Maaf kijiye, main samajh nahi paayi.")
        except Exception as e:
            result_label.config(text="Error aayi hai.")
            messagebox.showerror("Error", str(e))

# GUI
window = tk.Tk()
window.title("Yubi - Voice YouTube Search")
window.geometry("400x300")
window.configure(bg="#f2f2f2")

title_label = tk.Label(window, text="👋 Main Yubi hoon!", font=("Helvetica", 18, "bold"), bg="#f2f2f2", fg="#333")
title_label.pack(pady=10)

info_label = tk.Label(window, text="Aap YouTube par jo play karna chahte hain, kripya niche mic ka button dabaiye aur fir boliye.", font=("Helvetica", 10), wraplength=350, bg="#f2f2f2")
info_label.pack(pady=5)

listen_button = tk.Button(window, text="🎤 Boliye", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=start_listening)
listen_button.pack(pady=20)

result_label = tk.Label(window, text="", font=("Helvetica", 12), wraplength=350, bg="#f2f2f2", fg="blue")
result_label.pack(pady=10)

window.after(500, lambda: speak("Main Yubi hoon. Aap YouTube par jo play karna chahte hain, kripya Niche maaic ka button dabaiye aur fir boliye."))

window.mainloop()
