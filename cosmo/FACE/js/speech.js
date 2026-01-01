// Send simple GET request to your local server
function askCOSMO() {
    fetch(COSMO_HTTP)
        .then(res => console.log("COSMO asked:", res.status))
        .catch(err => console.log("COSMO is not listening; Import cosmo/senses/listen/COSMO_listen.prf.txt into Tasker", err));
}

// Add click listeners when page loads
window.addEventListener("DOMContentLoaded", () => {
    // Trigger on click anywhere
    const face = document.querySelector(".face");
    face.addEventListener("click", askCOSMO);
});