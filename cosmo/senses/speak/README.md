# COSMO 2 ❤
## TTS (Text To Speech) via Alexa Speaker😉❤❤❤ 

### I wanted to make better use of my Alexa speaker, so I cut the power wire and connected it to a Li-ion battery (fully disconnected from mains power), making it portable. I placed it inside COSMO’s head, secured the battery to the body with tape, and the robot started speaking. With ChatGPT added, COSMO talks far more intelligently than Alexa. Easily transportable, usable in any room. Sentiment analysis is included, and COSMO tailors replies for a kid. Contact me on [Discord Channel](https://discord.gg/dVgZ73tp6) if you need any help.

![IMG](speech.jpg)

Now COSMO Brain API is free!
You can use it absolutely for free, with a limit of 40 responses per hour — plenty for asking questions.
Each question can be up to 100 characters, enough to make a clear and logical query.
All answers are simplified for kids, easy to understand and fun!)

![IMG](cosmo_real.jpg)

# Usage and voice responses over Alexa speaker using native TTS
#### Use with COSMO brain API with rate limit 40/hour and 100 chars per question
    curl http://cosmo_tts_server_ip:8002/speak?t=hi
    curl http://46.224.122.101:8081/brain?q=atom

    Q: "atom" 
    A: An atom is like the tiniest LEGO brick that builds all the stuff you see, with a small center of protons and neutrons and buzzing electrons spinning around it. Try drawing different colored “atom blocks” on paper and then stack or swirl them together to create rainbow “mixes”—just like mixing paints or building a mini‑solar‑system game!

    Q: "was Jesus God or not?" 
    A: "That's a big question for a grown-up, but I'll explain it in a way that's easy to understand. Jesus is seen as a special person who was very close to God, but he's not considered God himself – think of him like a superhero sidekick who helps people and has special powers! 
    Imagine you're playing a game of superheroes where Luke Skywalker helps Han Solo on a quest. They're friends and work together, but Han Solo is still the main hero, while Luke serves alongside him and takes on his special roles."

    Q: "tell me some story from Bible about Jesus?" 
    A: Jesus amazed everyone when he walked on the ocean’s waves, showing that with faith you can do extraordinary things! You can try it at home by laying a blue blanket on the floor, hopping across it while pretending the “water” is steady beneath your feet.

    Q: "tell me how quickly light travel to Mars and back?"
    A: Light is super speedy, zooming around like a race car, but it still takes a while to get to Mars! It takes about 3 minutes for light to travel to Mars and another 3 minutes to come back, so about 6 minutes total - imagine playing a game of catch with a friend who lives really, really far away!

    Q: "cpu"
    A: A CPU is like the brain of a computer – it thinks super‑fast and decides what the computer does next, from playing a game to loading a video.  
    Try making a tiny game that makes an LED robot dance or a little sprite hop on screen – that’s a cool way to use its brainpower!

    Q: "raid5"
    A: RAID 5 is like a teamwork game where a file is split into secret parts that live on different drives, and if one drive goes sad, the computer can rebuild that missing part from the other drives to keep everything safe.  
    You can test it by making a tiny picture file, letting RAID spread it over three small disks, then deleting one—watch it figure out the missing piece like a detective puzzle!

    Q: "raid5"
    A: Raid 5 is like having multiple boxes to store toys, and when you lose one box, you can use the other boxes to find the missing toys because they all have pieces of a puzzle that matches. It's a type of super-safe way to store important computer data.

    Q: "what vitamins red pepper is rich with??" 
    A: Red pepper is super special because it has lots of vitamins A and C. These vitamins help keep you healthy and strong, and even make your eyes sight better like having a special superpower!  

    Q: "ESP32"
    A: An ESP32 is like a tiny, super-smart computer that can connect to the internet and talk to other devices – it's like giving toys brains! You can use an ESP32 to build a cool robot that sends you messages or a magical light that changes color when you clap your hands!

    Q: "if highest jumping dog jumps on moon how hight it will jump?"
    A: "On the moon, where gravity is only one‑sixth of Earth’s, a dog that jumps 1 meter high on Earth could hop about 6 meters, almost the length of a football field (but let’s pretend a dog with legs like a kangaroo could go even higher!). Imagine standing on a super‑bouncy trampoline that never pulls you down—when the dog leaps, it will float up, pause, then gently glide back down for a long, playful jump."

    Q: "Golf"
    A: "Golf is like a game where you try to hit a little ball into a hole using special sticks, and the person who does it with the fewest hits wins! You can have so much fun trying to aim and see how far you can whack the ball – maybe even pretend you're a super-famous golfer like Tiger Woods!

    Q: "Money"
    A: Money is like special tickets you earn for doing chores or getting allowance, and you can trade those tickets for toys, candy, or even a trip to the park! You could earn money by helping around the house, then save up to buy a cool new Lego set – that's super exciting!
    
    Q: "inflation" 
    A: Inflation is like a money-eating monster that makes things cost more money over time. Imagine you had $100 last year to buy 100 cookies, but now the price of cookies went up and you can only buy 80 cookies with the same $100.
        
    Q: "how to make money not working?"
    A: You can turn your extra toys, cards, or home‑made treats into quick money by setting up a little “market” in your park or hallway and asking friends to buy them with their allowance – it’s like a mini‑shop! Just plan out a fun banner, choose your favorite items, and start selling after school – it’s a play‑time fundraiser that turns play into coins.

    Q: "Investing"
    A: Investing is like planting a garden. You put money in (like seeds) and hopefully, it will grow into more money over time!

    Q: "game"
    A: Sure! Here’s a fun "Would You Rather" question for you:
    Would you rather have a pet tiger or a pet giraffe? Tigers are strong and fast, while giraffes are tall and have long necks. Which would you choose? Tigers might be quicker to chase you if they wanted to play! Giraffes would probably take longer to reach you, but they'd be really tall!    

    Q: "game" 
    A: Would you rather ride a friendly giraffe around the safari park or swim in a crystal‑clear lake with a dolphin that can splash you a cool mist?

    Q: "game"
    A:Let's play 'Would You Rather' Here's my first question:
    Would you rather have a pet dragonfly that could talk to you or a pet goldfish that could turn into a puppy?

# What you will need: 
Any [Alexa](https://www.amazon.com/b?node=9818047011&ref_=MARS_NAVSTRIPE_desktop_bar_Alexa%2B_shopall): (5 year old will work too). Any cheapest Echo Pop (shown above) for £25 will work as well.

### How to make COSMO speaking: 
### 1. Before running generate 'login_data.json' using:
    git clone https://github.com/chemelli74/aioamazondevices.git
    cd aioamazondevices/
    python library_test.py --email "your_amazon_alexa_email" --password "your_amazon_alexa_password"

    If OTP is not enabled in Alexa you will need to enable it:
    https://www.amazon.co.uk/gp/help/customer/display.html?nodeId=201962400
    https://www.amazon.co.uk/gp/css/account/info/view.html

### 2. Run python server 
    set path to your LOGIN_DATA_FILE = "2026-01-11-login_data.json" in cosmo_tts_server.py
    python cosmo_tts_server.py

![IMG](speak.jpg)
    
### 3. Use API
    curl http://cosmo_tts_server_ip:8002/speak?t=hi

#### Old Home Assitant Voice over Alexa (see [speak.ipynb](../../brain/brain.ipynb)) (not recommended)
    curl http://home_assistant_ip:8123/api/webhook/cosmo -H "Content-Type: application/json" -d '{"voice": "Raspberri PI"}'

    Q: "Raspberri PI"
    A: A Raspberry Pi is just a tiny computer tiny‑bit bigger than a postage stamp that fits right in your pocket—like a wizard’s brain all in a toy box. People play with it to build robots, paint moving pictures on a screen, play custom video game adventures, and even turn regular LEGO pieces into a dancing and buzzing robot buddy. 😃😻😺😹🙈🙊

#### Old OpenAI ChatGPT response paid (not recommended)
    curl http://home_assistant_ip:8123/api/webhook/cosmo_gpt -H "Content-Type: application/json" -d '{"voice": "1+1"}'

    Q: 1+1
    A: 1 + 1 equals 2! 🎉 It's like having one cookie and getting another — now you have two cookies to munch on! 🍪🍪

#### Home Assistant method (not recommended)
1. You’ll need [Home Assistant](https://www.home-assistant.io/) up and running
2. Install Home Assistant on Raspberry PI 5 or 4 or on [Linux](https://www.home-assistant.io/installation/linux/) (no Raspberry PI required)
3. Get ChatGPI API KEY and configure in Home Assistant: [config_screenshots](config_screenshots). Not needed if you use COSMO Brain API (free)
4. Integrate Alexa into Home Assistant: [config_screenshots](config_screenshots) or [cosmo.yaml](cosmo.yaml)

#### Test Home Assistant method (not recommended)
    curl -X POST -H "Authorization: Bearer YOUR_HOME_ASSISTANT_API_KEY" -H "Content-Type: application/json" -d '{"text": "1+1", "agent_id": "conversation.openai_conversation"}' http://home_assistant_ip:8123/api/conversation/process

#### Notes Home Assistant method (not recommended)
    home_assistant_ip - is your home Home Assistant IP
    YOUR_HOME_ASSISTANT_API_KEY is your Bearer Authorization API key in Home Assistant

# Honorable mentions
 * Thanks to God that gives...
 * To my father and my son: without them, this project would not exist
 * Amazon [Alexa](https://www.amazon.com/b?node=9818047011&ref_=MARS_NAVSTRIPE_desktop_bar_Alexa%2B_shopall) who offers £25 speakers with an excellent TTS capabilities
 * Simone Chemelli for Python [library](https://github.com/chemelli74/aioamazondevices) to control Amazon devices
 * Marcelo Trylesinski for [Uvicorn](https://github.com/Kludex/uvicorn) server on Python
 * Home Assistant for integrating Alexa, ChatGPT, Piper, Whisper, and multiple sensors
 * OpenAI for ChatGPI

### Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad. It is an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've listened before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

![Logo](https://cosmo.yes.app/poster_eng.jpg)

![Logo](https://cosmo.yes.app/promotion_eng.jpg)
![Logo](https://cosmo.yes.app/bonus_eng.jpg)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.