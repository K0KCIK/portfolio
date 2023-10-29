
import time
import os
import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import subprocess
import pyautogui
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from gtts import gTTS

global text
global task1
global task2
path_to_browser = r"path\to\your\browser"

muted = ["False"]
# Functions
def speak_response(response_text):
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    os.system("ffplay -nodisp -autoexit response.mp3")
def play_audio(audio_file_path):
    import subprocess
    subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])
def hello(recognizer):
    recognizer.pause_threshold = 0.5
    play_audio("gm.mp3")
def set_volume_level(text):
    digits = [char for char in text if char.isdigit()]
    if digits:
        volume_2 = int(''.join(digits))  # This and the next line
        print(f"{text}: {volume_2}")
        play_audio("commands/setting_volume.mp3")
        speak_response(str(volume_2))
        if 0 <= volume_2 <= 100:
            volume_2 = volume_2 * -1
            print(volume_2)
            set_volume(volume_2)  # This and the next line
        else:
            print("Invalid volume level")
    else:
        print("Volume value not found")
def unmute_volume(muted):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    if muted[0] == "True":
        volume.SetMute(1, None)
        muted[0] = "False"
        print(muted)
        speak_response("Muting volume")
    elif muted[0] == "False":
        volume.SetMute(0, None)
        muted[0] = "True"
        print(muted)
        speak_response("Unmuting volume")
def close_browser():
    subprocess.call(["taskkill", "/F", "/IM", "chrome.exe"])
def set_volume(volume_level):

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(volume_level, None)
def find_movie(text):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    if "find movie" in text.lower():
        text = text.replace("find movie", "").strip()
        play_audio("commands/Searching_for_a_movie.mp3")
        speak_response(text)
    print(text)
    driver.get("https://uakino.club")  # web site
    time.sleep(4)
    driver.find_element(By.ID, "show-search").click()  # search
    time.sleep(1)
    search = driver.find_element(By.ID, "ajax_search")
    search.click()
    search.send_keys(text)
    driver.find_element(By.XPATH, '//*[@id="quicksearch"]/div/button').click()
    try:
        film_link = driver.find_element(By.CSS_SELECTOR, ".movie-item.short-item a")
        film_link = film_link.get_attribute("href")
        subprocess.call([path_to_browser, f"{film_link}"])
        start_listening()
    except:
        print("Not found")
        start_listening()
def youtube_search(text):
    find_index = int(text.index("youtube"))
    text = text[find_index+7:]
    try:
        speak_response(text)
        subprocess.call([path_to_browser, f"https://www.youtube.com/results?search_query={text}"])
    except:
        print("Error")
def clock_time():
    full_time = []
    t = time.localtime()
    sec = t.tm_sec
    minute = t.tm_min
    hour = t.tm_hour
    full_time.append(sec)
    full_time.append(minute)
    full_time.append(hour)
    speak_response(f"{hour} o'clock,{minute} minutes and {sec} seconds")
def next_song():
    pyautogui.press("nexttrack")

def prev_song():
    pyautogui.press("prevTrack")
def pause():
    pyautogui.press("playpause")

class Search():
    def __init__(self, path_to_browser):
        self.path_to_browser = path_to_browser

    def youtube(text):
        find_index = int(text.index("youtube"))
        text = text[find_index + 7:]
        try:
            speak_response(text)
            subprocess.call([path_to_browser, f"https://www.youtube.com/results?search_query={text}"])
        except:
            print("Query request is empty")
    def google(text):
        if "find" and "google" in text.lower():
            words = text.split(" ")
            index = words.index("google")
            req = "+".join(words[index + 1:])
            re = req.split("+")
            re = "".join(map(str, re))
            speak_response(re)
            print(req)
            subprocess.call([path_to_browser, f"https://www.google.com/search?q={req}"])
def turn_off(text):
    digits = []
    for elem in text:
        if elem.isdigit():
            digits.append(elem)
        else:
            pass
    digits = "".join(map(str, digits))
    print(int(digits))
    speak_response(f"in {digits} seconds")
    subprocess.run(["shutdown", "/s", "/f", "/t", digits], shell=True)
def start_listening():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='us')
        text = text.lower()
        print(text)

        if text.lower() == "good morning":
            hello(recognizer)
        elif any(action_keyword in text.lower() for action_keyword in ["set", "volume"]):
            for number, word in [("1", "one"), ("2", "two"), ("3", "three"), ("4", "four"), ("5", "five"), ("6", "six"),
                                 ("7", "seven"), ("8", "eight"), ("9", "nine"), ("10", "ten")]:
                if word in text:
                    text = number
                    set_volume_level(text)
                    break
        elif any(action_keyword in text.lower() for action_keyword in ["mute volume", "unmute volume"]):
            play_audio("commands/Unmuting.mp3")
            unmute_volume(muted)
        elif "find movie" in text.lower():
            find_movie(text)
        elif "close browser" in text.lower():
            play_audio("commands/Closing_a_browser.mp3")
            close_browser()
        elif "time" in text.lower():
            play_audio("commands/Time.mp3")
            clock_time()
        elif "next song" in text.lower():
            play_audio("commands/Next_Song.mp3")
            next_song()
        elif any(action_keyword in text.lower() for action_keyword in ["song", "pause"]):
            play_audio("commands/Pause_Song.mp3")
            pause()
        elif all(trigger_phrase in text.lower() for trigger_phrase in ["find", "google"]):
            play_audio("commands/Searching_On_Google.mp3")
            Search.google(text)
        elif all(trigger_phrase in text.lower() for trigger_phrase in ["find", "youtube"]):
            play_audio("commands/Opening_YouTube.mp3")
            Search.youtube(text)
        elif "turn off" in text.lower():
            play_audio("commands/Shutdown.mp3")
            turn_off(text)
    except sr.UnknownValueError:
        print("Speech not recognized.")
    except sr.RequestError as e:
        print("Google request error: %s" % e)
# Start
if __name__ == "__main__":
    play_audio("GGM.mp3")
    while True:
        start_listening()
# Start
