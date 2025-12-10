# COSMO
COSMO Face ❤❤

While looking at my old iPhone sitting in the drawer, I thought, this could be a COSMO face.
I turned to my son and asked, “Would you want COSMO to have its own face?”...

Recent studies show that people often prefer a digital face over a physical one. A screen-based face is easy to build, customize, and update. I can create any combination of eyes, smiles, gestures, and templates — and even let the face grow and age over time alongside the robot. Plus, I can display technical information, like debug data, right on the screen.

And so, my old iPhone XS became the perfect candidate for COSMO’s new face.

![Logo](https://cosmo.yes.app/face/face.jpg)

# Usage: open in your PC or old phone / tablet (in full screen 'F11')
    https://cosmo.yes.app/face/

# Send Smile Command
    curl -X POST https://rest.ably.io/channels/cosmo_face/messages -u "CClXdw.Z3P7Fw:G1W_WXLZYUpqqnjvplbv_GDmUJ3TB4lk1bs54DblqpE" -H "Content-Type: application/json" --data '{ "name":"cURL","data": "smile" }'

    curl -X POST https://rest.ably.io/channels/cosmo_face/messages -u "CClXdw.Z3P7Fw:G1W_WXLZYUpqqnjvplbv_GDmUJ3TB4lk1bs54DblqpE" -H "Content-Type: application/json" --data '{ "name":"cURL","data": "blink" }'

# Emotions
    blink|smile|sad|angry|focused|confused|startBlinking|stopBlinking

# TODO:
 * Use my API key, and both your COSMO and mine will smile at the same time 😄. Feel free to try it out for testing!
 * Implement more mouth emotions to see the magic.


# Honorable mentions
 * To my father and my son: without them, this project would not exist ❤❤
 * Michael Jae-Yoon Chung and his minimalist tablet [tablet-robot-face](https://github.com/mjyc/tablet-robot-face) eyes
 * [Ably](https://ably.com) for SSE (Server-Sent Events) – plus 6 million free COSMO smiles every month! 😄
 * Thanks to [Apple](https://www.apple.com/), my old iPhone XS has become a brand-new COSMO face