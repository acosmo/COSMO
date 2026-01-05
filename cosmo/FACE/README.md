# COSMO ❤
COSMO Face

While looking at my old iPad sitting in the drawer, I thought, this could be a COSMO face.
I turned to my son and asked, “Would you want COSMO to have its own face?”...

### Recent studies show that people often prefer a digital face over a physical one. A screen-based face is easy to build, customize, and update. I can create any combination of eyes, smiles, gestures, and templates — and even let the face grow and age over time alongside the robot. Plus, I can display technical information, like debug data, right on the screen.

And so, my old iPad mini became the perfect candidate for COSMO’s new face.

#### I’m currently using two separate devices for COSMO (you can use one, but read below)
    * One is an Android phone running COSMO, which acts as the “brain” and handles voice processing (Samsung or Google: TTS/STT, Tasker, ChatGPT API, web server). Its screen stays off, but it can still receive HTTP GET requests
    * The other is an old iPad Mini running COSMO Face, which serves as the UI and display

For now, keeping the devices separate during the prototype phase is much more convenient. In this setup, the Android phone stays locked with the screen off, handling logic, voice processing, and commands, while iPad stays always on, providing the interface and activating voice interactions (ChatGPT responses on tap) back to COSMO. Essentially, COSMO has the brain, ears, and voice, and now face a visual.

### Support the project by purchasing my book [COSMO](https://cosmo.yes.app) All proceeds will be donated to charity and individuals in need, like my dad. It is an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've listened before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

# Usage: open in your PC (in full screen 'F11') or old phone (turn phone horizontally) or on tablet
1. Open [https://cosmo.yes.app/](http://46.224.122.101/face/) works from Chrome PC, Android, iPad, iPhone
2. Import [COSMO Listen Profile](tasker/COSMO_listen.prf.txt) into your Tasker and link with [COSMO Task](tasker/COSMO_task.prf.txt)

![Logo](face.jpg)

# Send 'smile' command
    curl -X POST https://rest.ably.io/channels/cosmo_face/messages -u "CClXdw.Z3P7Fw:G1W_WXLZYUpqqnjvplbv_GDmUJ3TB4lk1bs54DblqpE" -H "Content-Type: application/json" --data '{ "name":"cURL","data": "smile" }'

# Send 'blink' command
    curl -X POST https://rest.ably.io/channels/cosmo_face/messages -u "CClXdw.Z3P7Fw:G1W_WXLZYUpqqnjvplbv_GDmUJ3TB4lk1bs54DblqpE" -H "Content-Type: application/json" --data '{ "name":"cURL","data": "blink" }'

# Emotions
    blink|smile|sad|angry|focused|confused|startBlinking|stopBlinking|think|cat|forest

# Emotions
    Pressing on COSMO face should activate "ChatGPT" in phone tasker

![IMG](luna_face.jpg)
![IMG](../cosmo_real.jpg)

# Known Issues:
 1. On older iPads (10+ years), COSMO may not blink in response to API commands. To fix this, go to Settings → Safari → Advanced and enable Web Animation.
 2. For COSMO Face, it’s best to use the direct IP: http://46.224.122.101/face/ rather than https://cosmo.yes.app/face/. This ensures it works reliably on all devices — PC, old iPads, iPhones, and Android — across all browsers. If you decide to run your own web server on a Raspberry Pi (ASTRA), you’re welcome to do so.
 3. For your Android Tasker, it’s best to have COSMO Face send commands using the local IP: http://192.168.1.109:1888/ask4. Alternatively, you can modify config.js.
 4. Do not use HTTPS. If you choose to use HTTPS for COSMO Face, be prepared for several challenges. Tapping on the face sends a request to http://192.168.1.109:1888/ask4 (HTTP). Browsers like Firefox and Safari will block this as “mixed active content”, causing errors. The easiest workaround is to use Chrome on PC or Android and allow the necessary permissions.
 
![permission](../senses/listen/config_screenshots/pc_chrome_mixed_active_content.JPG)

or run COSMO Face locally via HTTP (e.g., just openeing index.html) so that both the page and the request use the same protocol, avoiding mixed content restrictions

# TODO:
 * Use my API key, and both your COSMO and mine will smile at the same time 😄. Feel free to try it out for testing!
 * Implement more mouth emotions to see the magic
 * Wake-on-key-word for COSMO


# Honorable mentions
 * Thanks to God that gives...
 * To my father and my son: without them, this project would not exist ❤❤
 * Michael Jae-Yoon Chung and his minimalist tablet [tablet-robot-face](https://github.com/mjyc/tablet-robot-face) eyes
 * [Ably](https://ably.com) for SSE (Server-Sent Events) – plus 6 million free COSMO smiles every month! 😄
 * Thanks to [Apple](https://www.apple.com/), my old iPad mini has become a brand-new COSMO face
 * Thanks to [Pixabay](https://pixabay.com), [Oleg Fedak](https://pixabay.com/users/30064790/), and many more creators for sounds
 * Big thanks to [Tim Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee) for developing HTML in 1991
 * Microsoft for [VS Code](https://code.visualstudio.com/)


### Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad. It is an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've listened before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

![Logo](https://cosmo.yes.app/poster_eng.jpg)

![Logo](https://cosmo.yes.app/promotion_eng.jpg)
![Logo](https://cosmo.yes.app/bonus_eng.jpg)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.