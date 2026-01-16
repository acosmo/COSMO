const sounds = {
    smile: new Audio('sounds/smile.mp3'),
    blink: new Audio('sounds/blink.mp3'),
    smell: new Audio('sounds/smell.mp3'),
    cough: new Audio('sounds/cough.mp3'),
    sad: new Audio('sounds/sad.mp3'),
    angry: new Audio('sounds/angry.mp3'),
    focused: new Audio('sounds/focused.mp3'),
    confused: new Audio('sounds/confused.mp3'),
    think: new Audio('sounds/think.mp3'),
    cat: new Audio('sounds/cat.mp3'),
    forest: new Audio('sounds/forest.mp3'),
    blinking: new Audio('sounds/blinking.mp3')
};

for (let key in sounds) {
    sounds[key].preload = 'auto';
}