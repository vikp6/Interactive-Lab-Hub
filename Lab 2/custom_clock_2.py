import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from adafruit_rgb_display.rgb import color565
import webcolors
from datetime import datetime
from datetime import timedelta
import busio
import adafruit_apds9960.apds9960
import time
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_proximity = True
sensor.enable_gesture = True
gesture = sensor.gesture()

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))




rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image)

# image = Image.open("red.jpg")
# backlight = digitalio.DigitalInOut(board.D22)
# backlight.switch_to_output()
# backlight.value = True
# image = image.resize((50, 50), Image.BICUBIC)

# # Scale the image to the smaller screen dimension
# image_ratio = image.width / image.height
# screen_ratio = width / height
# if screen_ratio < image_ratio:
#     scaled_width = image.width * height // image.height
#     scaled_height = height
# else:
#     scaled_width = width
#     scaled_height = image.height * width // image.width

# Crop and center the image
# x = scaled_width // 2 - width // 2
# y = scaled_height // 2 - height // 2
# image = image.crop((x, y, x + width, y + height))

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


# Image to represent each Season
image_Summer = Image.open("summer.jpg")
image_Summer = image_Summer.resize((100, 100), Image.BICUBIC)
image_Fall = Image.open("fall.jpg")
image_Fall = image_Fall.resize((100, 100), Image.BICUBIC)
image_Winter = Image.open("winter.jpg")
image_Winter = image_Winter.resize((100, 100), Image.BICUBIC)
image_Spring = Image.open("spring.jpg")
image_Spring = image_Spring.resize((100, 100), Image.BICUBIC)

#Datetime to represent start of each next season
nextSummer = datetime(2023, 6, 21)
nextFall = datetime(2022, 9, 22)
nextWinter = datetime(2022, 12, 21)
nextSpring = datetime(2023, 3, 21)


#0 is Summer, 1 is Fall, 2 is Winter, 3 is Spring
#List of tuples carrying all season related objects

seasonsList = [("Summer",nextSummer,image_Summer),
               ("Fall",nextFall,image_Fall),
               ("Winter",nextWinter,image_Winter),
               ("Spring",nextSpring,image_Spring)]

currSeason = 0
clearflag = 0
birthday = None
while True:
    
    #Displays Image representing season
    if not buttonA.value:
#         disp.image(seasonsList[currSeason][2])
    #Switches Season
        clearflag = 1
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, width, height), outline=0, fill=0)
#             print (strftime("%m/%d/%Y %H:%M:%S"), end="", flush=True)


        td = seasonsList[currSeason][1] - datetime.now()
        #print(str(timedelta(seconds=td.seconds)))
        #print("\r", end="", flush=True)
        y = top
        
        sznstring = seasonsList[currSeason][0]
        draw.text((0,0),"Time Until Next "+str(sznstring), font=font, fill="#FFFFFF")
        draw.text((0, 25),"Days: "+str(td.days) , font=font, fill="#FFFFFF")
        draw.text((0, 50),"HMS: "+str(timedelta(seconds=td.seconds)) , font=font, fill="#FFFFFF")
        
        # Display image.
        disp.image(image, rotation)

        time.sleep(1)

    else:
        if clearflag==1:
            image = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            disp.image(image, rotation)
            clearflag = 0
            
        disp.image(seasonsList[currSeason][2])
        gesture = sensor.gesture()
        
        #Find time from birthday
        if not buttonB.value:
            time.sleep(.1)
            done = 0
            selector = 0
            month = 1
            day = 1
            year = 2022
            while done==0:
                image = Image.new("RGB", (width, height))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                
                draw.text((0,0),"Month: "+str(month), font=font, fill="#FFFFFF")
                draw.text((0,25),"Day: "+str(day), font=font, fill="#FFFFFF")
                year = datetime.now().year
                
                bdayDatetime = datetime(year, month, day)
                if bdayDatetime < datetime.now():
                    bdayDatetime = datetime(year+1, month, day)
                td2 = bdayDatetime - datetime.now()
                
                #draw.text((0,50),"Current Day: "+str(datetime.now().year), font=font, fill="#FFFFFF")
                draw.text((0, 50),"Days: "+str(td2.days) , font=font, fill="#FFFFFF")
                draw.text((0, 75),"HMS: "+str(timedelta(seconds=td2.seconds)) , font=font, fill="#FFFFFF")
               
                disp.image(image, rotation)
                
                
                gesture = sensor.gesture()
                if gesture == 0x01 and selector ==0:
                    if month==12:
                        month=1
                    else:
                        month+=1
                elif gesture == 0x02 and selector ==0:
                    if month==1:
                        month = 12
                    else:
                        month-=1
                elif gesture == 0x01 and selector ==1:
                    if day==31:
                        day = 1
                    else:
                        day+=1
                elif gesture == 0x02 and selector ==1:
                    if day==1:
                        day = 31
                    else:
                        day-=1
               
                if not buttonA.value:
                   selector = not selector
                   print(selector)
                   time.sleep(.1)
                
                if not buttonB.value:
                    done=1
                    clearflag=1
                    time.sleep(.1)
                    
        else:
            if gesture == 0x04:
                print("right")
                if currSeason == 3:
                    currSeason = 0
                else:
                    currSeason += 1
            elif gesture == 0x03:
                print("left")
                if currSeason == 0:
                    currSeason = 3
                else:
                    currSeason -= 1


