# ASTRA ❤
ASTRA Project Overview 😉❤❤❤ 

![Logo](https://cosmo.yes.app/astra/astra.jpg)

The ASTRA project began after my son asked me to build a **robot** for his granddad, who is disabled. In the UK alone, there are over 3 million people with similar conditions, yet the market lacks accessible and effective products to meet their needs. Seeing this gap, we started an open-source project to develop a small, user-friendly robot designed specifically to help my dad.

### Further down, at the end, you’ll find links to support the project by purchasing one of my books. The [COSMO](https://cosmo.yes.app) book is available now, and the ASTRA book is coming soon… ✅

Initially evolved as a streaming platform for my disabled dad, connected to an old 40" TV. Its purpose was to automatically stream preselected YouTube content via a Raspberry Pi while I was away. It had a simple scheduler that ran a "python stream.py" script every hour (while another device would switch ON the TV at a specific time)

# Usage
    0 * * * * python stream.py

Later, after my father passed away, my son asked if I could set it up in his room to watch cartoons😊. Since his room was too small for a TV, I purchased a cheapest [HY 320 mini projector](https://magcubic.com/products/protable-projector-hy320-mini). This marked the beginning of a new project. ASTRA has become a friend of COSMO, and together they work as a pair. ASTRA can project onto a wall two meters wide in my son’s room, showing bedtime stories at 8PM, simulating asteroids falling in the night sky, or simply playing cartoons. 

    No more dealing with bulky TVs, tangled HDMI cables, 
    or complicated speakers — everything is small and simple...

    No more wasting time switching it on or hunting for cartoons...

    I’ve curated a playlist of predefined topics: 
    math, physics, space experiments, and more and added it to the database ('db' folder). 

    Now, it runs automatically on schedule, and my son drifts off to sleep peacefully ❤

### Support the project by purchasing my book [COSMO](https://cosmo.yes.app) All proceeds will be donated to charity and individuals in need, like my dad. [COSMO](https://cosmo.yes.app) an audio book — a captivating and original puzzle book inspired by my dad. It's unlike any other book you've read before, blending mystery and emotion with a unique structure that keeps you guessing until the fascinating and unexpected ending.

![Logo](https://cosmo.yes.app/poster_eng.jpg)

Currently, we have integrated a straeming core service called "astra", which combines several key technologies:

    1. Affordable mini projector for £30 (HY 320 mini projector). Any Projector with HDMI will work.
    2. Chromecast - for streaming content (works on any device, even 10-year-old ones, for just £6)
    3. Raspberry Pi (any model £10) - used as a streamer to Chromecast (though any headless Linux Python executor could be substituted). No need to install KODI, and could be plain Linux OS
    Optional: 
    KODI (OpenELEC) - selected to explore potential value from this integration, with the flexibility to replace it with another Linux-based solution or plain vanilla Linux in the future

Since my dad cannot operate a TV on his own, we needed a system that could automatically play video, audio, and online services (like YouTube, Netflix, and Spotify) on a set schedule. Another major issue we encountered was the inability to control content recommendations from platforms like YouTube and Spotify. Their algorithms are designed to maximize engagement, not necessarily to provide meaningful or beneficial content. I've seen this problem with using iPads, the algorithm takes over, feeding them content it thinks is relevant, often leading down a rabbit hole of low-quality or inappropriate material like war, politics, or mindless distractions. 

The same problem arose with my dad. He would watch YouTube on his iPad, but there was no way to filter out content and create a controlled, beneficial viewing experience. Despite trying various solutions like setting limits, marking content as "disliked," and using parental controls it felt like a constant battle against the algorithm rather than a real solution. This highlighted the need for a system where we, as caregivers, could curate content directly, ensuring that only positive, engaging, and beneficial material reaches him.
Together with my son, we realized this setup could go beyond entertainment it could deliver educational programs, learning materials, films, audiobooks, meditation, and relaxation content, improving my dad's mood and cognitive engagement.

To solve this, I created a predefined list of videos and built a simple database of curated content tailored specifically to his needs. This includes:

    bible.txt       -> Bible 
    films.txt       -> Free YouTube films ID's in his native language
    robots.txt      -> As a talented engineer, he loves DIY projects, electronics, robotics, solar tech, and EVs.
    books.txt       -> Free YouTube Audiobooks (also in his native language)
    exercises.txt   -> Guided exercises
    travel.txt      -> Travel videos
    meditation      -> Meditation sessions
    relax.txt       -> Simple nature sounds: rain, ocean etc. 

Technically, I created these playlists of YouTube videos outside of YouTube by compiling a folder-based database (DB) containing the IDs of preselected videos. This way, the content is directly accessible without relying on YouTube's recommendation algorithm. While this setup could eventually evolve into a structured database, for now, I'm following the KISS principle (Keep It Simple, Stupid) maintaining a straightforward, easy-to-manage system that just works.

Currently, the system simply streams a random file from the curated list on a schedule. This approach helps keep things simple and quick to implement. In the future, I plan to add a memory feature that will track which videos have already been played and prioritize unplayed content. This will prevent the same content from appearing twice and ensure a more varied and engaging experience over time. For now, the random approach works well for quick deployment and testing.

Looking ahead, this solution has the potential to serve broader applications beyond personal use. It could be adapted for schools, kids and parent controlled streaming, clubs, restaurants, bars, exhibition centers, libraries, corporate events, receptions, and hotels - essentially any setting where scheduled content delivery could enhance the user experience.

- [Dependencies](#dependencies)
- [Honorable mentions](#honorable-mentions)

# Dependencies

None! this script is written in pure vanilla Python 3+.

# Honorable mentions
 * To my father and my son: without them, this project would not exist
 * Anton Hvornum Aka Torxed https://github.com/Torxed/chromecast
 * [Perth Linux User Group](http://plug.org.au/)'s [talk from 2016](https://docs.google.com/presentation/d/1X1BdFunVnLkF7L0BgevH2zzkcSe0_gtdTJ_pMdEuakQ/htmlpresent)
 * [pychromecast](https://github.com/home-assistant-libs/pychromecast) Which had a lot of `URN`'s that could be re-used
 * [casttube](https://github.com/ur1katz/casttube) Which had all the YouTube Web-API's to manage a YouTube lounge
 * Google for inventing [Chromecast](https://en.wikipedia.org/wiki/Chromecast) in 2013 and making the [ProtoBuf](https://developers.google.com/protocol-buffers/docs/encoding) protocol very open and easy to deconstruct; 
 * Chad Hurley, Steve Chen, and Jawed Karim for inventing [YouTube](https://www.youtube.com)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.

![Logo](https://cosmo.yes.app/promotion_eng.jpg)
![Logo](https://cosmo.yes.app/bonus_eng.jpg)

## Support the project by purchasing my book [COSMO](https://cosmo.yes.app). All proceeds will be donated to charity and individuals in need, like my dad.
