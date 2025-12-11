# COSMO 2 ❤
COSMO 2 Project (COSMO, living in my son’s phone) 😉❤❤❤ 

Later an idea came to build a helper for my son. He was bombarding me with questions, and since he cannot use Google yet, I decided to automate it. I bought him a simple [£100 phone](https://www.gsmarena.com/motorola_moto_g35-13288.php) and installed [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en_GB), which redirects all his questions to ChatGPT. Using Google TTS (Text-to-Speech) and STT (Speech-to-Text), COSMO explains the answers in a way that matches his age.

![Logo](https://cosmo.yes.app/cosmo2/cosmo2.jpg)

The Motorola G35 has a side button, so now a double press lets COSMO know he can ask a question. Previously, this was triggered by shaking the phone, but I decided to switch back to using the double press.

All questions and answers are recorded in my Google Drive, and the entire setup took only about an hour (no coding required). Tasker is highly configurable, so COSMO has become much smarter — it can answer many questions, and handling around 100 questions costs me only about $0.01.

I can continuously improve the answers by tuning the STT output, refining how queries are formed for the API, and adjusting how the AI responds. I have also added a personality layer: with every reply, COSMO reads a personality file and randomly chooses one of 100 custom phrases taken from our shared memories or encouraging messages. These “end phrases” are appended to each answer using a simple rand() algorithm connected to a file (cosmo_el.csv) in my Google Drive.

Importantly, this solution does not need high-bandwidth Internet content, as it only uses pure API calls and text uploads. It follows the KISS (Keep It Simple) principle, is fully independent, and is entirely serverless. It doesn’t require any third-party servers, doesn’t need sign-ups or paid subscriptions, and doesn’t send or record voice data. It gives full control over the code, offering maximum flexibility and customization. Configuration is done easily through the simple Tasker UI, making it a practical and beneficial solution for both my son and me.

Every conversation is saved, so I have full visibility into what my son asks and how COSMO responds. This helps me tune COSMO better over time. All interactions are stored in my Google Drive in cosmo.csv.

# Usage

    shake phone and magic happends... 😉❤❤❤ 

To make it running: 
1. Get [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en_GB)
If you don’t have a subscription, you can use the [7-day trial version](https://tasker.joaoapps.com/download.html)
 to set it up quickly. COSMO will continue working after the trial ends. I still encourage you to support João Dias by purchasing the app (£3.99), as he created an excellent tool.
2. Generate [ChatGPT API Keys](https://platform.openai.com/settings/organization/api-keys)
3. Replace all XXXXXX placeholders in [COSMO Task](face/tasker/COSMO_task.prf.txt) with your variables, then either import the file or manually set the steps following my screenshot (folder: [config_screenshots](config_screenshots))
3. COSMO (ChatGPT) is inside. Shake the phone — it should work. If not, check the config_screenshots:

![Logo](https://cosmo.yes.app/cosmo2/a4.jpg)
![Logo](https://cosmo.yes.app/cosmo2/c1.jpg)
![Logo](https://cosmo.yes.app/cosmo2/c9.jpg)
![Logo](https://cosmo.yes.app/cosmo2/c10.jpg)
![Logo](https://cosmo.yes.app/cosmo2/c12.jpg)

Known issues: 
1. The cosmo_end_talk.xls file needs to be in your Google Drive folder, and you can update with your own short personality prefixes that will be added at end talk. It need to be shared with link as on picture below.
2. The cosmo.csv file needs to be in your GoogleDrive folder so it can store and be updated with logs of questions, answers, and timestamps.

![Logo](https://cosmo.yes.app/cosmo2/c16.jpg)

# Honorable mentions
 * To my father and my son: without them, this project would not exist
 * João Dias [Tasker Android APP](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) and his [homepage](https://tasker.joaoapps.com)
 * ApenAI and [ChatGPT](https://chatgpt.com)
 * Google for Google Drive and [Android](https://www.android.com)


### Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad. It is an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've listened before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

![Logo](https://cosmo.yes.app/poster_eng.jpg)

![Logo](https://cosmo.yes.app/promotion_eng.jpg)
![Logo](https://cosmo.yes.app/bonus_eng.jpg)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.