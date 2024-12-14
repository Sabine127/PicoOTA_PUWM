# Bibliotheken laden
from ota import OTAUpdater
import network
from WIFI_CONFIG import SSID, PASSWORD
#from machine import RTC
from time import sleep
from machine import Pin,ADC
import neopixel
import machine
import owntime

#Update-Folder PlattUhrWohnMobil
firmware_url="https://raw.githubusercontent.com/Sabine127/PicoOTA_PUWM/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
ota_updater.download_and_install_update_if_available()


lightPin=28
LightPin=ADC(lightPin)
lightFaktor=0.5

# Zeitzone
TZ_OFFSET = +1

# GPIO-Pin für WS2812
pin_np = 0

# Anzahl der LEDs
leds = 136

# Helligkeit: 0 bis 255
brightness=0.1 #Wert zwischen 0 und 1
redVal = 0
greenVal = 0
blueVal = 0

# Initialisierung WS2812/NeoPixel
np = neopixel.NeoPixel(Pin(pin_np, Pin.OUT), leds)

# Ländereinstellung
network.country('DE')

# Client-Betrieb
wlan = network.WLAN(network.STA_IF)

# WLAN-Interface aktivieren
wlan.active(True)

# WLAN-Verbindung herstellen
wlan.connect(SSID, PASSWORD)

# WLAN-Verbindungsstatus prüfen
import time
print('Warten auf WLAN-Verbindung')
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)
print('WLAN-Verbindung hergestellt / Status:', wlan.status())

if wlan.isconnected():
    # Zeit setzen
    owntime.setTime()
    print('Zeit wurde aus dem Wlan geholt')
# Echtzeituhr im Mikrocontroller initialisieren
#rtc = RTC()

while True:
    lightVal=LightPin.read_u16()
    brightness=lightFaktor*lightVal/65550
    print(lightFaktor,lightVal,brightness)
    # Datum und Uhrzeit lesen
    # Uhrzeit ändern
    datetime = owntime.localTime(TZ_OFFSET)
#    datetime = [2024,13,4,13,13,23,50]
    sec_von_hour = datetime[5]*60+datetime[6]

    hours=datetime[4]
    minutes=datetime[5]
    seconds=datetime[6]+1

    if seconds%60==0 and minutes%5==0:
        print('   Minute:', minutes)
        print('  Sekunde:', seconds)
        print('SecVonHour: ',sec_von_hour)
        print('   Stunde:', hours)
        for i in range (leds):
            np[i] = (0, 0, 0)
            # np.write()
    #Red    
    if sec_von_hour>=3000 and sec_von_hour<3600:
        redVal=int(((sec_von_hour-3000)*(255/600))*brightness)
    if sec_von_hour>=0 and sec_von_hour<1800:
        redVal=int((255)*brightness)
    if sec_von_hour>=1800 and sec_von_hour<2400:
        redVal=int((255-((sec_von_hour-1800)*(255/600)))*brightness)
    if sec_von_hour>=2400 and sec_von_hour<3000:
        redVal=int(0*brightness)
        
    #green    
    if sec_von_hour>=2400 and sec_von_hour<2700:
        greenVal=int(((sec_von_hour-2400)*(255/300))*brightness)
    if sec_von_hour>=2700 and sec_von_hour<3600:
        greenVal=int((255)*brightness)
    if sec_von_hour>=0 and sec_von_hour<900:
        greenVal=int((255-((sec_von_hour-0)*(255/900)))*brightness)
    if sec_von_hour>=900 and sec_von_hour<2400:
        greenVal=int(0*brightness)
        
    #blue
    if sec_von_hour>=900 and sec_von_hour<1800:
        blueVal=int(((sec_von_hour-900)*(255/900))*brightness)
    if sec_von_hour>=1800 and sec_von_hour<2700:
        blueVal=int((255)*brightness)
    if sec_von_hour>=2700 and sec_von_hour<3000:
        blueVal=int((255-((sec_von_hour-2700)*(255/300)))*brightness)
    if sec_von_hour>=3000 and sec_von_hour<900:
        blueVal=int(0*brightness)

    # Minuten-LEDs
    if datetime[5]%5>=1:
        for i in range (135,136):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()
    if datetime[5]%5>=2:
        for i in range (122,123):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()
    if datetime[5]%5>=3:
        for i in range (0,1):
            np[i] = (redVal, greenVal, blueVal)
            # # np.write()           
    if datetime[5]%5>=4:
        for i in range (13,14):
            np[i] = (redVal, greenVal, blueVal)
            # # np.write()    

    ## Immer
    # DAT
    for i in range (132,135):
        np[i] = (redVal, greenVal, blueVal)
        # # # np.write()      

    # IS
    for i in range (129,131):
        np[i] = (redVal, greenVal, blueVal)
        # np.write()



    # Volle Stunde: KLOCK
    if seconds<=58 and minutes<=4:
        for i in range (123,128):
            np[i] = (redVal, greenVal, blueVal)
            # # np.write()               

    ## Stunden-Wörter
    # EEN (vor Eins)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==0 or hours==12):
        for i in range (80,83):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()
            
    # EEN (nach Eins)
    if seconds<=58 and \
        (minutes>=0 and minutes<=24) and \
        (hours==1 or hours==13):
        for i in range (80,83):
            np[i] = (redVal, greenVal, blueVal)
            # # np.write()           
        
    # TWEE (vor Zwei)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==1 or hours==13):       
        for i in range (82,86):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()
            
    # TWEE (nach Zwei)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==2 or hours==14):
        for i in range (82,86):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # DREE (vor Drei)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==2 or hours==14):
        for i in range (34,38):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # DREE (nach Drei)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==3 or hours==15):
        for i in range (34,38):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # VEER (vor Vier)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==3 or hours==15):
        for i in range (66,70):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # VEER (nach Vier)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==4 or hours==16):
        for i in range (66,70):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # FIEF (vor Fünf)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==4 or hours==16):     
        for i in range (62,66):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # FIEF (nach Fünf)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==5 or hours==17):    
        for i in range (62,66):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # SÖSS (vor Sechs)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==5 or hours==17):     
        for i in range (57,61):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # SÖSS (nach Sechs)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==6 or hours==18):      
        for i in range (57,61):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()


    # SÖVEN (vor Sieben)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==6 or hours==18):     
        for i in range (50,55):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # SÖVEN (nach Sieben)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==7 or hours==19): 
        for i in range (50,55):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # ACHT (vor Acht)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==7 or hours==19):         
        for i in range (70,74):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # ACHT (nach Acht)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==8 or hours==20): 
        for i in range (70,74):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # NEGEN (vor Neun)
    if seconds<=58 and\
        (minutes>=25 and minutes<=59) and \
        (hours==8 or hours==20):
        for i in range (76,81):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # NEGEN (nach Neun)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==9 or hours==21):
        for i in range (76,81):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # TEIHN (vor Zehn)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==9 or hours==21):
        for i in range (28,33):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # TEIHN (nach Zehn)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==10 or hours==22):
        for i in range (28,33):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # ÖLVEN (vor Elf)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==10 or hours==22):
        for i in range (43,48):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # ÖLVEN (nach Elf)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==11 or hours==23):
        for i in range (43,48):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # TWÖLF (vor Zwölf)
    if seconds<=58 and \
       (minutes>=25 and minutes<=59) and \
       (hours==11 or hours==23):
        for i in range (38,43):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # TWÖLF (nach Zwölf)
    if seconds<=58 and \
       (minutes>=0 and minutes<=24) and \
       (hours==12 or hours==0):
        for i in range (38,43):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    ## Minuuten-Wörter
    # FIEF
    if seconds<=58 and \
       (minutes>=5 and minutes<=9) or \
       (minutes>=25 and minutes<=29) or \
       (minutes>=35 and minutes<=39) or \
       (minutes>=55 and minutes<=59):
        for i in range (110,114):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # TEIHN
    if seconds<=58 and \
       (minutes>=10 and minutes<=14) or \
       (minutes>=50 and minutes<=54):
        for i in range (105,110):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # VEERTEL (VIDDEL)
    if seconds<=58 and \
       (minutes>=15 and minutes<=19) or \
       (minutes>=45 and minutes<=49):
        for i in range (98,105):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # TWINTIG
    if seconds<=58 and \
       (minutes>=20 and minutes<=24) or \
       (minutes>=40 and minutes<=44):
        for i in range (114,121):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # HALV
    if seconds<=58 and \
       (minutes>=25 and minutes<=39):
        for i in range (94,98):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    ## Binde-Wörter
    # VÖR
    if seconds<=58 and \
       (minutes>=25 and minutes<=29) or \
       (minutes>=40 and minutes<=59):
        for i in range (90,93):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # NA
    if seconds<=58 and \
       (minutes>=5 and minutes<=24) or \
       (minutes>=35 and minutes<=39):
        for i in range (86,88):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()
            
    ## Tageszeiten
    # VÖR (MEDDAGS)
    if seconds<=58 and \
       (hours>=5 and hours<=11):
        for i in range (14,17):
            np[i] = (redVal, greenVal, blueVal)
            # # np.write()   

    # MEDDAGS
    if seconds<=58 and \
       (hours>=5 and hours<=17):        
        for i in range (19,26):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # NA(MEDDAGS)
    if seconds<=58 and \
       (hours>=14 and hours<=17):
        for i in range (17,19):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # AVENDS
    if seconds<=58 and \
       (hours>=18 and hours<=21):
        for i in range (7,13):
            np[i] = (redVal, greenVal, blueVal)
            # np.write()

    # SNACHTS
    if seconds<=58 and \
       (hours>=0 and hours<=4) or\
       (hours>=22 and hours<=23):
        for i in range (1,8):
            np[i] = (redVal, greenVal, blueVal)
            # # np.write()      

    np.write()
    sleep(1)


