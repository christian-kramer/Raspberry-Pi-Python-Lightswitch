# Raspberry-Pi-Python-Lightswitch
An update to the "Workbench Light" project that adds manual control to the WiFi outlets

___

Previously, [I had created a .NET Framework Windows Service](https://github.com/christian-kramer/workbench-light) to turn the lights above my workbench on and off at the same time as my bench computer. This was extremely convenient, as I only had to press one button on my wireless keyboard/trackpad combo to setup my entire workbench space when I wanted to use it... but there were some slight drawbacks.

Firstly, my bench computer takes a while to start up and trigger the outlet. I mean, it has an SSD and fast RAM so it's not like I have to go get a coffee while I wait, but when I just need to work on something quickly that doesn't need the computer... it's annoying to not have light instantly when I need it.

Secondly, I had lights below my workbench that I wanted to turn on and off, too. But I didn't want these to also be controlled by the PC power state, because most of the time they're unnecessary... Only when I'm looking underneath at my stored items do I need them on.

Finally, my bench computer has a very annoying habit of exiting sleep mode in the middle of the night to re-sync the hardware clock to NTP time. I have done everything I can possibly think of to prevent this from happening, short of always shutting it down, but... see point #1. I want light quickly, and preferably not suddenly in the middle of the night while I'm trying to sleep.

So... it was pretty clear to me that I should have at least an auxiliary physical interface with which to turn the lights on and off. And, since I had a few Raspberry Pis laying around... it definitely sounded like a project I could tackle!

Since I already had a Pi to work with, my first step was figuring out what I wanted for the physical switch. In my head, I envisioned a light switch, but instead of a conventional "on/off", the switch would rest in the center position and be able to be "bumped" up and down to toggle the top and bottom lights, respectively. This way, if I decided to turn the lights on, then my computer, and then finally shut down the computer to turn everything off... the lights wouldn't be "held" in the on state. The switch would always return to center after interacting with it. Basically, a 3-position momentary switch.

Time to head to Axman to find one!

Eventually, I stumbled upon one that seemed like it would work. It was much bigger than I had imagined... several times longer than it was tall, but it had the advantage of appearing to fit within a standard wall plate (and hopefully a standard junction box).

I picked up one of each at the local hardware store, and test-fit the Pi and switch inside the wall plate and junction box, using some old CAT5 I had lying around to connect the switch terminals to the Pi's GPIO.

![Pi Zero Switch](https://i.imgur.com/KQTtCf2.jpg)

Perfect! Time to write some code to get the switch interacting with the Outlets' API.

I ended up taking a multi-threaded approach, mostly to try it out in Python, and secondly to let more powerful dual-core Pi's in the future schedule each switch process concurrently. Hey, turning on lights can benefit from performance scaling too, ya know.

I'm aware that the way it's currently written is fairly verbose and redundant, but for as simple as it is, it'd be incredibly easy to condense in the future when I've got an hour to throw at it.

Anywho, this isn't the end of it yet. I need this switch to be completely self-sufficient. If there's a power outage or if I need to unplug it for any reason, I need the Pi to start up with this script running ASAP. It should be an appliance, basically.

For that, I turned to utilizing sytemd... the software suite running at the heart of every sane Linux distro out there, including Raspbian. Systemd, like Windows, offers a way for you to write small "services" that run at boot. Think SSH, nginx/Apache, etc. None of those (usually) require logging in and starting them up manually. You just set 'em and forget 'em. I want that, but for my python script!

So, it turns out, writing a systemd service is stupidly simple. Much simpler than a Windows service, in my opinion.

Here's my entire unit file:

![switch.service](https://i.imgur.com/m9W5zCN.png)

(transcript)

```[Unit]
Description=Workbench Lights
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/bin/switch.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```

And after setting permissions and enabling the service using systemctl...

![Service Success](https://i.imgur.com/goHU3z7.png)

Ta da! Now I don't need to worry about restarting my light switch script every time I unplug my Pi.