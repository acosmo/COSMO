// Send simple GET request to your local server
function askCOSMO() {
    fetch(COSMO_HTTP)
        .then(res => console.log("COSMO asked:", res.status))
        .catch(err => console.log("COSMO is not listening; Import cosmo/senses/listen/COSMO_listen.prf.txt into Tasker", err));
    
    // ✅ Trigger smile animation
    if (typeof eyes !== 'undefined') {
        eyes.express({ type: 'happy' });  // make eyes happy
    }
    if (sounds.think) {
        sounds.think.currentTime = 0;
        sounds.think.play();
    }    
}

// Add click listeners when page loads
window.addEventListener("DOMContentLoaded", () => {
    // Trigger on click anywhere
    const face = document.querySelector(".face");
    face.addEventListener("click", askCOSMO);
});