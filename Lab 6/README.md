# Little Interactions Everywhere

1. Vikram Pandian (vip6@cornell.edu)
2. Abhishek Nair (an464@cornell.edu)

## Prep

1. Pull the new changes from the class interactive-lab-hub. (You should be familiar with this already!)
2. Install [MQTT Explorer](http://mqtt-explorer.com/) on your laptop. If you are using Mac, MQTT Explorer only works when installed from the [App Store](https://apps.apple.com/app/apple-store/id1455214828).
3. Readings before class:
   * [MQTT](#MQTT)
   * [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) and [video](https://vimeo.com/15932020)


## Overview

The point of this lab is to introduce you to distributed interaction. We have included some Natural Language Processing (NLP) and Generation (NLG) but those are not really the emphasis. Feel free to dig into the examples and play around the code which you can integrate into your projects if wanted. However, we want to emphasize that the grading will focus on your ability to develop interesting uses for messaging across distributed devices. Here are the four sections of the lab activity:

A) [MQTT](#part-a)

B) [Send and Receive on your Pi](#part-b)

C) [Streaming a Sensor](#part-c)

D) [The One True ColorNet](#part-d)

E) [Make It Your Own](#part-)

## Part 1.

### Part A
### MQTT

MQTT is a lightweight messaging portal invented in 1999 for low bandwidth networks. It was later adopted as a defacto standard for a variety of [Internet of Things (IoT)](https://en.wikipedia.org/wiki/Internet_of_things) devices. 

#### The Bits

* **Broker** - The central server node that receives all messages and sends them out to the interested clients. Our broker is hosted on the far lab server (Thanks David!) at `farlab.infosci.cornell.edu/8883`. Imagine that the Broker is the messaging center!
* **Client** - A device that subscribes or publishes information to/on the network.
* **Topic** - The location data gets published to. These are *hierarchical with subtopics*. For example, If you were making a network of IoT smart bulbs this might look like `home/livingroom/sidelamp/light_status` and `home/livingroom/sidelamp/voltage`. With this setup, the info/updates of the sidelamp's `light_status` and `voltage` will be store in the subtopics. Because we use this broker for a variety of projects you have access to read, write and create subtopics of `IDD`. This means `IDD/ilan/is/a/goof` is a valid topic you can send data messages to.
*  **Subscribe** - This is a way of telling the client to pay attention to messages the broker sends out on the topic. You can subscribe to a specific topic or subtopics. You can also unsubscribe. Following the previouse example of home IoT smart bulbs, subscribing to `home/livingroom/sidelamp/#` would give you message updates to both the light_status and the voltage.
* **Publish** - This is a way of sending messages to a topic. Again, with the previouse example, you can set up your IoT smart bulbs to publish info/updates to the topic or subtopic. Also, note that you can publish to topics you do not subscribe to. 


**Important note:** With the broker we set up for the class, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`. Also, setting up a broker is not much work, but for the purposes of this class, you should all use the broker we have set up for you!


#### Useful Tooling

Debugging and visualizing what's happening on your MQTT broker can be helpful. We like [MQTT Explorer](http://mqtt-explorer.com/). You can connect by putting in the settings from the image below.


![input settings](imgs/mqtt_explorer.png?raw=true)


Once connected, you should be able to see all the messages under the IDD topic. , go to the **Publish** tab and try publish something! From the interface you can send and plot messages as well. Remember, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`.


<img width="1026" alt="Screen Shot 2022-10-30 at 10 40 32 AM" src="https://user-images.githubusercontent.com/24699361/198885090-356f4af0-4706-4fb1-870f-41c15e030aba.png">



### Part B
### Send and Receive on your Pi

[sender.py](./sender.py) and and [reader.py](./reader.py) show you the basics of using the mqtt in python. Let's spend a few minutes running these and seeing how messages are transferred and shown up. Before working on your Pi, keep the connection of `farlab.infosci.cornell.edu/8883` with MQTT Explorer running on your laptop.

**Running Examples on Pi**

* Install the packages from `requirements.txt` under a virtual environment, we will continue to use the `circuitpython` environment we setup earlier this semester:

  ```
  pi@raspberrypi:~/Interactive-Lab-Hub $ source circuitpython/bin/activate
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub $ cd Lab\ 6
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ pip install -r requirements.txt
  ...
  ```
* Run `sender.py`, fill in a topic name (should start with `IDD/`), then start sending messages. You should be able to see them on MQTT Explorer.

  ```
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python sender.py
  >> topic: IDD/AlexandraTesting
  now writing to topic IDD/AlexandraTesting
  type new-topic to swich topics
  >> message: testtesttest
  ...
  ```
* Run `reader.py`, and you should see any messages being published to `IDD/` subtopics. Type a message inside MQTT explorer and see if you can receive it with `reader.py`.

  ```
  (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python reader.py
  ...
  ```

<img width="890" alt="Screen Shot 2022-10-30 at 10 47 52 AM" src="https://user-images.githubusercontent.com/24699361/198885135-a1d38d17-a78f-4bb2-91c7-17d014c3a0bd.png">


**\*\*\*Consider how you might use this messaging system on interactive devices, and draw/write down 5 ideas here.\*\*\***

1. LED Control: using a pair of Raspberry Pis, one could send a message to the other to trigger an LED light event. For exmaple, a message (JSON message: {ledstatus: on}) could be sent from one Pi to another receiver Pi to turn on a LED light connected to it. 

2. Smart Shopping List: using a webcam placed in a fridge, a connected sender Pi can detect the number of eggs and bread currently in the fridge using computer vision to send it to a receiver Pi with a grocery list on a connected display displaying the number of eggs and bread currently in the fridge.

3. Greenhouse Temperature Monitor: using a temperature sensor, a sender Pi can send the current temperature in a greenhouse to a receiver Pi with a display connected to it to display the current temperature of the greenhouse. The receiver Pi can also send a message to the sender Pi to turn on a fan to cool down the greenhouse if the temperature is too high.

4. Smart Doorbell: using a camera, a sender Pi can detect when someone is at the door and send a message to a receiver Pi with a display connected to it to display a message saying that someone is at the door along with the number of people detected. The receiver Pi can also send messages to the doorbell pi to output messages to the person at the door with text to speech. 

5. GPS enabled Run Tracker: using a GPS sensor, a sender pi can stream the current location of a runner to a receiver pi located at the runner's home. The receiver pi is booted using Ubuntu and connected to a monitor which can be used to analyze the runs in great detail later on based on the data saved on the receiver pi.

### Part C
### Streaming a Sensor

We have included an updated example from [lab 4](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Fall2021/Lab%204) that streams the [capacitor sensor](https://learn.adafruit.com/adafruit-mpr121-gator) inputs over MQTT. We will also be running this example under `circuitpython` virtual environment.

Plug in the capacitive sensor board with the Qwiic connector. Use the alligator clips to connect a Twizzler (or any other things you used back in Lab 4) and run the example script:

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
<img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150"/>
<img src="https://media.discordapp.net/attachments/679721816318803975/823299613812719666/PXL_20210321_205742253.jpg" height="150">
</p>

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python distributed_twizzlers_sender.py
 ...
 ```

**\*\*\*Include a picture of your setup here: what did you see on MQTT Explorer?\*\*\***

**\*\*\*Pick another part in your kit and try to implement the data streaming with it.\*\*\***

<p align="center">
  <img src="https://github.com/abhisheknair10/Interactive-Lab-Hub/blob/Fall2022/Lab%206/1.png" height="600" />
</p>

<p align="center">
  <img src="https://github.com/abhisheknair10/Interactive-Lab-Hub/blob/Fall2022/Lab%206/2.jpeg" height="600" />
</p>


### Part D
### The One True ColorNet

It is with great fortitude and resilience that we shall worship at the altar of the *OneColor*. Through unity of the collective RGB, we too can find unity in our heart, minds and souls. With the help of machines, we can overthrow the bourgeoisie, get on the same wavelength (this was also a color pun) and establish [Fully Automated Luxury Communism](https://en.wikipedia.org/wiki/Fully_Automated_Luxury_Communism).

The first step on the path to *collective* enlightenment, plug the [APDS-9960 Proximity, Light, RGB, and Gesture Sensor](https://www.adafruit.com/product/3595) into the [MiniPiTFT Display](https://www.adafruit.com/product/4393). You are almost there!

<p float="left">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
  <img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
  <img src="https://cdn-shop.adafruit.com/970x728/3595-03.jpg" height="150">
</p>


The second step to achieving our great enlightenment is to run `color.py`. We have talked about this sensor back in Lab 2 and Lab 4, this script is similar to what you have done before! Remember to activate the `circuitpython` virtual environment you have been using during this semester before running the script:

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python color.py
 ...
 ```

By running the script, wou will find the two squares on the display. Half is showing an approximation of the output from the color sensor. The other half is up to the collective. Press the top button to share your color with the class. Your color is now our color, our color is now your color. We are one.

(A message from the previous TA, Ilan: I was not super careful with handling the loop so you may need to press more than once if the timing isn't quite right. Also, I haven't load-tested it so things might just immediately break when everyone pushes the button at once.)

You may ask "but what if I missed class?" Am I not admitted into the collective enlightenment of the *OneColor*?

Of course not! You can go to [https://one-true-colornet.glitch.me/](https://one-true-colornet.glitch.me/) and become one with the ColorNet on the inter-webs. Glitch is a great tool for prototyping sites, interfaces and web-apps that's worth taking some time to get familiar with if you have a chance. Its not super pertinent for the class but good to know either way.


### Part E
### Make it your own

Find at least one class (more are okay) partner, and design a distributed application together based on the exercise we asked you to do in this lab.

**\*\*\*1. Explain your design\*\*\*** For example, if you made a remote controlled banana piano, explain why anyone would want such a thing.

**\*\*\*2. Diagram the architecture of the system.\*\*\*** Be clear to document where input, output and computation occur, and label all parts and connections. For example, where is the banana, who is the banana player, where does the sound get played, and who is listening to the banana music?

**\*\*\*3. Build a working prototype of the system.\*\*\*** Do think about the user interface: if someone encountered these bananas somewhere in the wild, would they know how to interact with them? Should they know what to expect?

**\*\*\*4. Document the working prototype in use.\*\*\*** It may be helpful to record a Zoom session where you should the input in one location clearly causing response in another location.

<!--**\*\*\*5. BONUS (Wendy didn't approve this so you should probably ignore it)\*\*\*** get the whole class to run your code and make your distributed system BIGGER.-->

# Remote Artist

## System Design
Over the past few years, distributed computing has become a hot topic in the tech industry. The rise of cloud computing and the Internet of Things has made it possible to build distributed systems that are both powerful and accessible. In this lab, we will explore the basics of distributed computing by building a distributed system.

With remote robotic surgery, we can now perform surgery on patients from anywhere in the world. This lab takes that concept as inspiration to remotely draw diagrams and figures using the input of a sender Raspberry Pi to a receiver Raspberry Pi that renders the drawing on the receiver's screen.

Essentially, a sender Raspberry Pi is connected to a joystick and reads the joystick's input. The sender then streams the joystick's input to the receiver Raspberry Pi, which then uses the input to draw on the receiver's screen. The drawing is rendered on the screen by accurately mapping the joystick input to the display based on it's appropriate dimensions. The sender and receiver are connected through MQTT, a protocol that allows for communication between devices.

## System Architecture

Below is a figure depicting the architecture of said system.

<p align="center">
  <img src="https://github.com/abhisheknair10/Interactive-Lab-Hub/blob/Fall2022/Lab%206/Part%20E/arch.png" height="600" />
</p>

## System Implementation and User Interface Considerations

The implementation of this system is available at [Remote Artist](https://github.com/abhisheknair10/Interactive-Lab-Hub/tree/Fall2022/Lab%206/Part%20E) in the subdirectory `Lab 6/Part E/`.

The technical steps involved are listed below:

1. Sender - connect to the MQTT broker

```python
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883
)
```

2. Sender - read data from Joystick

```python
myJoystick.begin()
x = myJoystick.horizontal
y = myJoystick.vertical
button = myJoystick.button
```

3. Sender - publish data to MQTT broker

```python
client.publish(
    'an464vip6/joystick',
    str(
      {
            "x": x,
            "y": y, 
            "button": button
        }
    )
)
```

4. Receiver - connect to the MQTT broker, subscribe to the topic and read the data

```python
if msg.topic=='IDD/an464vip6/joystick':
    data = ast.literal_eval(msg.payload.decode('UTF-8'))

    xVal = data['x']
    yVal = data['y']
    buttonVal = data['button']
```

5. Convert scale of joystick to display and render pixel on display

```python
width=135
height=240
xRes = int(width*int(xVal)/1023)
yRes = int(height*int(yVal)/1023)
display.pixel(xRes,yRes,color565(31, 63, 31))
display.pixel(xRes+1,yRes,color565(31, 63, 31))
display.pixel(xRes-1,yRes,color565(31, 63, 31))
display.pixel(xRes,yRes+1,color565(31, 63, 31))
display.pixel(xRes,yRes-1,color565(31, 63, 31))
display.pixel(xRes+1,yRes+1,color565(31, 63, 31))
display.pixel(xRes-1,yRes-1,color565(31, 63, 31))
display.pixel(xRes+1,yRes-1,color565(31, 63, 31))
display.pixel(xRes-1,yRes+1,color565(31, 63, 31))
```

6. Draw something with system


The joystick is a very obvious and intuitive tool to work with by moving it up, down, left and right. Based on this, the user should pretty easily know how to interact with the system.

## Working Prototype

Below is a link to a video of the working prototype.

[Demonstration 1](https://drive.google.com/file/d/1queNMKs1cklf2GTSqMuZLQL4tcB8RdmQ/view?usp=sharing)

[Demonstration 2](https://drive.google.com/file/d/1T3NX9fjoG0vo3Tu7-GH0dXscbHsRcLEl/view?usp=sharing)