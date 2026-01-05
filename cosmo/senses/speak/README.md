# COSMO 2 ❤
Prototype TTS (Text To Speach) via Alexa Speaker😉❤❤❤ 

I wanted to make better use of my Alexa speaker, so I cut the power wire and connected it to a Li-ion battery (fully disconnected from mains power), making it portable. I placed it inside COSMO’s head, secured the battery to the body with tape, and the robot started speaking. With ChatGPT added, COSMO talks far more intelligently than Alexa. Easily transportable, usable in any room. Sentiment analysis is included, and COSMO tailors replies for a 4-year-old kid. Contact me on [Discord Channel](https://discord.gg/dVgZ73tp6) if you need any help.

# Usage
    curl http://192.168.1.211:8123/api/webhook/cosmo -H "Content-Type: application/json" -d '{"text": "1+1"}'

# Voice Response over Alexa speaker using native TTS
    1 + 1 equals 2! 🎉 It's like having one cookie and getting another — now you have two cookies to munch on! 🍪🍪

![IMG](cosmo_real.jpg)

# To make it running: 
1. You’ll need [Home Assistant](https://www.home-assistant.io/) up and running
2. Install Home Assistant on Raspberry PI 5 or 4 or on [Linux](https://www.home-assistant.io/installation/linux/) (no Raspberry PI required)
3. Get ChatGPI API KEY and configure in Home Assistant: [config_screenshots](config_screenshots)
4. Get any Alexa: 5 year old [Alexa](https://www.amazon.com/b?node=9818047011&ref_=MARS_NAVSTRIPE_desktop_bar_Alexa%2B_shopall) speaker will work The cheapest Echo Pop (shown above) for £25 will work as well.
5. Integrate Alexa into Home Assistant: [config_screenshots](config_screenshots) or [ha.yaml](ha.yaml)

# Test
    curl -X POST -H "Authorization: Bearer YOUR_HOME_ASSISTANT_API_KEY" -H "Content-Type: application/json" -d '{"text": "1+1", "agent_id": "conversation.openai_conversation"}' http://192.168.1.211:8123/api/conversation/process

# Notes
    192.168.1.211 - is your home Home Assistant IP
    YOUR_HOME_ASSISTANT_API_KEY is your Bearer Authorization API key in Home Assistant

# Honorable mentions
 * Thanks to God that gives...
 * To my father and my son: without them, this project would not exist
 * Amazon Alexa offers £25 speakers with an excellent TTS API
 * Home Assistant for integrating Alexa, ChatGPT, Piper, Whisper, and multiple sensors
 * OpenAI for ChatGPI

### Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad. It is an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've listened before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

![Logo](https://cosmo.yes.app/poster_eng.jpg)

![Logo](https://cosmo.yes.app/promotion_eng.jpg)
![Logo](https://cosmo.yes.app/bonus_eng.jpg)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.