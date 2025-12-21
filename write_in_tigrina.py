

from pynput.keyboard import Listener as KeyboardListener,Key,Controller
from pynput import keyboard
from tkinter import *
import threading
keyboard_ctl = Controller()
new_start=[]
dictionary = {
    "h": "ህ",
    "ህe": "ሀ",
    "ህu": "ሁ",
    "ህi": "ሂ",
    "ህa": "ሃ",
    "ሂe":"ሄ",
    "ህo": "ሆ",
    "ልe": "ለ",
    "ልu": "ሉ",
    "ልi": "ሊ",
    "ልa": "ላ",
    "ሊe": "ሌ",
    "l": "ል",
    "ልo": "ሎ",
    "ሕe": "ሐ",
    "ሕu": "ሑ",
    "ሕi": "ሒ",
    "ሕa": "ሓ",
    "ሒe": "ሔ",
    "H": "ሕ",
    "ሕo": "ሖ",
    "ምe": "መ",
    "ምu": "ሙ",
    "ምi": "ሚ",
    "ምa": "ማ",
    "ሚe": "ሜ",
    "m": "ም",
    "ምo": "ሞ",
    "ሥ2e": "ሠ",
    "ሥ2u": "ሡ",
    "ሥ2i": "ሢ",
    "ሥ2a": "ሣ",
    "ሢe": "ሤ",
    "ሥ2": "ሥ",
    "ሥ2o": "ሦ",
    "ርe": "ረ",
    "ርu": "ሩ",
    "ርi": "ሪ",
    "ርa": "ራ",
    "ሪe": "ሬ",
    "r": "ር",
    "ርo": "ሮ",
    "ስe": "ሰ",
    "ስu": "ሱ",
    "ስi": "ሲ",
    "ስa": "ሳ",
    "ሲe": "ሴ",
    "s": "ስ",
    "ስo": "ሶ",
    "ሽe": "ሸ",
    "ሽu": "ሹ",
    "ሽi": "ሺ",
    "ሽa": "ሻ",
    "ሺe": "ሼ",
    "S": "ሽ",
    "ሽo": "ሾ",
    "ቅe": "ቀ",
    "ቅu": "ቁ",
    "ቅi": "ቂ",
    "ቅa": "ቃ",
    "ቂe": "ቄ",
    "q": "ቅ",
    "ቅo": "ቆ",
    "ቕe": "ቐ",
    "ቕu": "ቑ",
    "ቕi": "ቒ",
    "ቕa": "ቓ",
    "ቒe": "ቔ",
    "Q": "ቕ",
    "ቕo": "ቖ",
    "ብe": "በ",
    "ብu": "ቡ",
    "ብi": "ቢ",
    "ብa": "ባ",
    "ቢe": "ቤ",
    "b": "ብ",
    "ብo": "ቦ",
    "ቭe": "ቨ",
    "ቭu": "ቩ",
    "ቭi": "ቪ",
    "ቭa": "ቫ",
    "ቪe": "ቬ",
    "v": "ቭ",
    "ቭo": "ቮ",
    "ትe": "ተ",
    "ትu": "ቱ",
    "ትi": "ቲ",
    "ትa": "ታ",
    "ቲe": "ቴ",
    "t": "ት",
    "ትo": "ቶ",
    "ችe": "ቸ",
    "ችu": "ቹ",
    "ችi": "ቺ",
    "ችa": "ቻ",
    "ቺe": "ቼ",
    "c": "ች",
    "ችo": "ቾ",
    "ኅe": "ኀ",
    "ኅu": "ኁ",
    "ኅi": "ኂ",
    "ኅa": "ኃ",
    "ኂe": "ኄ",
    "ህ2": "ኅ",
    "ኅo": "ኆ",

    "ኍe": "ኈ",
    "ኍi": "ኊ",
    "ኍa": "ኋ",
    "ኊe": "ኌ",
    "ሕ2": "ኍ",

    "ንe": "ነ",
    "ንu": "ኑ",
    "ንi": "ኒ",
    "ንa": "ና",
    "ኒe": "ኔ",
    "n": "ን",
    "ንo": "ኖ",
    "ኝe": "ኘ",
    "ኝu": "ኙ",
    "ኝi": "ኚ",
    "ኝa": "ኛ",
    "ኚe": "ኜ",
    "N": "ኝ",
    "ኝo": "ኞ",
    "እe": "አ",
    "እu": "ኡ",
    "እi": "ኢ",
    "እa": "ኣ",
    "ኢe": "ኤ",
    "A": "እ",
    "እo": "ኦ",
    "ክe": "ከ",
    "ክu": "ኩ",
    "ክi": "ኪ",
    "ክa": "ካ",
    "ኪe": "ኬ",
    "k": "ክ",
    "ክo": "ኮ",
    "ኩe": "ኰ",
    "ኩi": "ኲ",
    "ኩa": "ኳ",
    "ኩe": "ኴ",
    "ኩu": "ኵ",
    "ኽe": "ኸ",
    "ኽu": "ኹ",
    "ኽi": "ኺ",
    "ኽa": "ኻ",
    "ኺe": "ኼ",
    "K": "ኽ",
    "ኽo": "ኾ",

    "ኹe": "ዀ",
    "ኹi": "ዂ",
    "ኹa": "ዃ",
    "ኹe": "ዄ",
    "ኹw": "ዅ",

    "ውe": "ወ",
    "ውu": "ዉ",
    "ውi": "ዊ",
    "ውa": "ዋ",
    "ዊe": "ዌ",
    "w": "ው",
    "ውo": "ዎ",
    "ዕe": "ዐ",
    "ዕu": "ዑ",
    "ዕi": "ዒ",
    "ዕa": "ዓ",
    "ዒe": "ዔ",
    "O": "ዕ",
    "ዕo": "ዖ",
    "ዝe": "ዘ",
    "ዝu": "ዙ",
    "ዝi": "ዚ",
    "ዝa": "ዛ",
    "ዚe": "ዜ",
    "z": "ዝ",
    "ዝo": "ዞ",
    "ዥe": "ዠ",
    "ዥu": "ዡ",
    "ዥi": "ዢ",
    "ዥa": "ዣ",
    "ዢe": "ዤ",
    "Z": "ዥ",
    "ዥo": "ዦ",
    "ይe": "የ",
    "ይu": "ዩ",
    "ይi": "ዪ",
    "ይa": "ያ",
    "ዪe": "ዬ",
    "y": "ይ",
    "ይo": "ዮ",
    "ድe": "ደ",
    "ድu": "ዱ",
    "ድi": "ዲ",
    "ድa": "ዳ",
    "ዲe": "ዴ",
    "d": "ድ",
    "ድo": "ዶ",
    "ጅe": "ጀ",
    "ጅu": "ጁ",
    "ጅi": "ጂ",
    "ጅa": "ጃ",
    "ጂe": "ጄ",
    "j": "ጅ",
    "ጅo": "ጆ",
    "ግe": "ገ",
    "ግu": "ጉ",
    "ግi": "ጊ",
    "ግa": "ጋ",
    "ጊe": "ጌ",
    "g": "ግ",
    "ግo": "ጎ",
    "ጒe": "ጐ",
    "ጒi": "ጒ",
    "ጒa": "ጓ",
    "ጒe": "ጔ",
    "ግu": "ጕ",
    "ጥe": "ጠ",
    "ጥu": "ጡ",
    "ጥi": "ጢ",
    "ጥa": "ጣ",
    "ጢe": "ጤ",
    "T": "ጥ",
    "ጥo": "ጦ",
    "ጭe": "ጨ",
    "ጭu": "ጩ",
    "ጭi": "ጪ",
    "ጭa": "ጫ",
    "ጪe": "ጬ",
    "C": "ጭ",
    "ጭo": "ጮ",
    "ጵe": "ጰ",
    "ጵu": "ጱ",
    "ጵi": "ጲ",
    "ጵa": "ጳ",
    "ጲe": "ጴ",
    "P": "ጵ",
    "ጵo": "ጶ",
    "ጽe": "ጸ",
    "ጽu": "ጹ",
    "ጽi": "ጺ",
    "ጽa": "ጻ",
    "ጺe": "ጼ",
    "x": "ጽ",
    "ጽo": "ጾ",
    "ፅe": "ፀ",
    "ፅu": "ፁ",
    "ፅi": "ፂ",
    "ፅa": "ፃ",
    "ፂe": "ፄ",
    "ጽ2": "ፅ",
    "ፅo": "ፆ",
    "ፍe": "ፈ",
    "ፍu": "ፉ",
    "ፍi": "ፊ",
    "ፍa": "ፋ",
    "ፊe": "ፌ",
    "f": "ፍ",
    "ፍo": "ፎ",
    "ፕe": "ፐ",
    "ፕu": "ፑ",
    "ፕi": "ፒ",
    "ፕa": "ፓ",
    "ፒe": "ፔ",
    "p": "ፕ",
    "ፕo": "ፖ",
    ";": "፡",
    ",": "፣",
    ":": "፥",
    "::": "፤",
    ";-": "፦",
    "ጝe": "ጘ",
    "ጝu": "ጙ",
    "ጝi": "ጚ",
    "ጝa": "ጛ",
    "ጚe": "ጜ",
    "ጝ": "ጝ",
    "ጝo": "ጞ",
    "ጝue": "ⶓ",
    "ጝui": "ⶔ",
    "ጝua": "ጟ",
    "ⶔe": "ⶕ",
    "ጝW": "ⶖ",
    "ሆa": "ሇ",
    "ሉa": "ሏ",
    "ሑa": "ሗ",
    "ሙa": "ሟ",
    "ሷ2a": "ሧ",
    "ua": "ሯ",
    "ሱa": "ሷ",
    "ሹa": "ሿ",
    "ቆa": "ቇ",
    "ቡa": "ቧ",
    "ቩa": "ቯ",
    "ቱa": "ቷ",
    "ቹa": "ቿ",
    "ኑa": "ኗ",
    "ኛa": "ኟ",
    "ua": "ኧ",
    "ኮa": "ኯ",
    "ኹa": "ዃ",
    "ዉa": "ዏ",
    "ዙa": "ዟ",
    "ዡa": "ዧ",
    "ዮa": "ዯ",
    "ዱa": "ዷ",
    "ጁa": "ጇ",
    "ጎa": "ጏ",
    "ጡa": "ጧ",
    "ጩa": "ጯ",
    "ጱa": "ጷ",
    "ጹa": "ጿ",
    "ጿ2a": "ፇ",
    "ፉa": "ፏ",
    "ፑa": "ፗ",
    "ዽe": "ዸ",
    "ዽu": "ዹ",
    "ዽi": "ዺ",
    "ዽa": "ዻ",
    "ዺe": "ዼ",
    "ድ2": "ዽ",
    "ዽo": "ዾ",
    "ዹa": "ዿ",
    "ሪ2": "ፘ",
    "ሚ2": "ፙ",
    "ፊ2": "ፚ",
    "ቐe": "ቘ",
    "ቑi": "ቚ",
    "ቓa": "ቛ",
    "ቚe": "ቜ",
    "ቕu": "ቝ"
}

class KeyboardListenerHandler:
        def __init__(self):
            self.listener_running = False
            self.listener_thread = None
            self.hotKeyListener = keyboard.GlobalHotKeys({
                '<ctrl>+<shift>': self.toggle_listener,
                '<ctrl>+x': self.stop_listeners  # Stop listener with <ctrl>+x
            })
            self.arr1=(keyboard.Key.enter,keyboard.Key.esc,keyboard.Key.tab,keyboard.Key.shift,keyboard.Key.shift_r,keyboard.Key.ctrl,
            keyboard.Key.down,keyboard.Key.up,keyboard.Key.right,keyboard.Key.left,keyboard.Key.caps_lock,keyboard.Key.cmd,keyboard.Key.cmd_r,
            keyboard.Key.alt,keyboard.Key.space,keyboard.Key.alt_r,keyboard.Key.media_play_pause,keyboard.Key.media_volume_mute,keyboard.Key.media_volume_down,
            )
            
            self.keyboardStoped=False
           
            
        def getAlphabet(self,key):
             threading.Thread(target=self._process_key, args=(key,)).start()
             
        def _process_key(self, key):
            try:
                # Handle space key
                if key == 'space':
                    self.new_start.clear()
                    keyboard.press("")
                    return
                # Check if the key or combination is in the dictionary
                if key.char in dictionary:
                    # Single key match
                    keyboard_ctl.press(Key.backspace)
                    keyboard_ctl.type(dictionary[key.char])
                    new_start.append(dictionary[key.char])
                else:
                    # Handle combinations
                    if new_start:
                        last_char = new_start[-1]  # Last character from new_start
                        combination = last_char + key.char

                        if combination in dictionary:
                            keyboard_ctl.type("\b\b" + dictionary[combination])  # Erase last two characters and replace
                            new_start.pop()  # Remove last character
                            new_start.append(dictionary[combination])  # Add new translation
                            return

                    # Handle vowel addition (e.g., "እ" + vowel)
                    if key.char in ['a', 'e', 'i', 'o', 'u']:
                        char = "እ" + key.char
                        if char in dictionary:
                            keyboard_ctl.press(Key.backspace)
                            keyboard_ctl.type(dictionary[char])
                            new_start.append(dictionary[char])
                
                # Maintain a maximum length for new_start to avoid unnecessary buildup
                if len(new_start) > 2:
                    new_start.pop(0)

            except Exception as error:
                return ""
        
        def on_press(self,key):
            pass
        def on_release(self,key):
            try:
                if key == keyboard.Key.esc :
                    pass
                elif key == keyboard.Key.ctrl_l:
                    pass
                elif key in self.arr1:
                    if key==keyboard.Key.space:
                        self.getAlphabet("space")
                    else:
                        pass
                else:
                    if self.keyboardStoped==False:
                        self.getAlphabet(key)
            except Exception as error:
                return ""
        def onActivate(self):
            if self.listener_running:
                self.keyboardStoped=False

        def onDeactivate(self):
            if self.listener_running:
                self.keyboardStoped=True
                

        def toggle_listener(self):
            # self.listener_running = not self.listener_running
            print("self.listener_running:",self.listener_running)
            print("self.keyboardStoped:",self.keyboardStoped)
            if self.listener_running:
                if self.keyboardStoped:
                    self.keyboardStoped=False
                else:
                    self.keyboardStoped=True
                print("Keyboard listener activated.")
            else:
                print("Keyboard listener deactivated.")
        def stop_listeners(self):
            # global listener_running
            self.listener_running = False

        def start_listeners(self):
            """Start the keyboard listeners."""
            # if not self.listener_running:
            self.listener_running = True
            self.listener_thread = threading.Thread(target=self.run_listeners)
            self.listener_thread.daemon = True
            self.listener_thread.start()
            self.hotKeyListener.start()
            print("Keyboard listener started.")
            # else:
            #     print("Keyboard listener is already running.")
        def run_listeners(self):
            """Thread target to listen to keyboard events."""
            with KeyboardListener(on_press=self.on_press, on_release=self.on_release) as keyboard_listener:
                # while self.listener_running:
                #     pass
                keyboard_listener.join()
            print("Keyboard listener thread exiting.")
        def stop(self):
            """Stop the keyboard listener."""
            self.listener_running = False
            
