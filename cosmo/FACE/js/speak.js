// Send simple GET request to your local server
function sendFaceCommand() {
    fetch("http://192.168.1.109:1888/ask")
        .then(res => console.log("COSMO asked:", res.status))
        .catch(err => console.log("COSMO is not listening; Import cosmo/listen.txt into tasker", err));
}

// Add click listeners when page loads
window.addEventListener("DOMContentLoaded", () => {
    // Trigger on click anywhere
    window.addEventListener("click", sendFaceCommand);
});