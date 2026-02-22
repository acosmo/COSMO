// Single click handler
helloCosmo.addEventListener('click', async () => {
    // 1️⃣ Play the first sound immediately (blink)
        if (typeof eyes !== 'undefined') {
            eyes.blink();
            sounds.blink.currentTime = 0;
            const playPromise = sounds.blink.play();
            if (playPromise !== undefined) {
                playPromise.catch(e => console.warn('Blink blocked:', e));
            }
        }

        // 2️⃣ Reset and unlock all other sounds
        for (let key in sounds) {
            if (key !== 'blink') {
                sounds[key].pause();
                sounds[key].currentTime = 0;
                try {
                    sounds[key].play();
                    sounds[key].pause();
                } catch(e) {}
            }
        }

        // 3️⃣ Start COSMO
        getStarted();

        // 4️⃣ Hide button
        helloCosmo.style.opacity = 0;
        setTimeout(() => helloCosmo.style.display = 'none', 300);
});

const output = document.getElementById('output');

function log(message) {
    output.innerHTML += '<p>' + message + '</p>';
    console.log(message);
}

async function getStarted() {
    const realtimeClient = new Ably.Realtime({
        key: ABLY_KEY,
        clientId: 'cosmo_face'
    });

    await realtimeClient.connection.once('connected');
    //log('Made my first connection!');

    const channel = realtimeClient.channels.get('cosmo_face');

    await channel.subscribe((message) => {
        //log(`Received message: ${message.data}`);

        // If the message is "smile", make COSMO happy
        if (message.data === 'smile') {
            eyes.express({ type: 'happy' });
            sounds.smile.currentTime = 0;
            sounds.smile.play();
        }
        if (message.data === 'smell') {
            eyes.express({ type: 'focused' });
            sounds.smell.currentTime = 0;
            sounds.smell.play();
        }
        if (message.data === 'cough') {
            eyes.express({ type: 'angry' });
            sounds.cough.currentTime = 0;
            sounds.cough.play();
        }
        if (message.data === 'air') {
            eyes.express({ type: 'angry' });
            sounds.air.currentTime = 0;
            sounds.air.play();
        }           
        // Blinking
        if (message.data === 'blink') {
            eyes.blink()
            sounds.blink.currentTime = 0;
            sounds.blink.play();
        }
        // Other emotions
        if (message.data === 'sad') {
            eyes.express({ type: 'sad' });
            sounds.sad.currentTime = 0;
            sounds.sad.play();
        }
        if (message.data === 'angry') {
            eyes.express({ type: 'angry' });
            sounds.angry.currentTime = 0;
            sounds.angry.play();
        }
        if (message.data === 'focused') {
            eyes.express({ type: 'focused' });
            sounds.focused.currentTime = 0;
            sounds.focused.play();
        }
        if (message.data === 'confused') {
            eyes.express({ type: 'confused' });
            sounds.focused.currentTime = 0;
            sounds.focused.play();
        }
        if (message.data === 'think') {
            eyes.express({ type: 'happy' });
            sounds.think.currentTime = 0;
            sounds.think.play();
        }
        if (message.data === 'cat') {
            eyes.express({ type: 'happy' });
            sounds.cat.currentTime = 0;
            sounds.cat.play();
        }
        if (message.data === 'forest') {
            eyes.express({ type: 'startBlinking' });
            sounds.forest.currentTime = 0;
            sounds.forest.play();
        }                
        if (message.data === 'startBlinking') {
            eyes.startBlinking()
            sounds.blinking.currentTime = 0;
            sounds.blinking.play();
        }
        if (message.data === 'stopBlinking') {
            eyes.stopBlinking()
        }                                                 
    });
}

getStarted();