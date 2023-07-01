document.getElementById("get-verse-btn").addEventListener("click", getVerse);

function getVerse() {
    fetch("/v1/verses/random")
        .then(response => response.json())
        .then(data => {
            document.getElementById("verse-text").textContent = data.text;
        })
        .catch(error => {
            console.log("Error:", error);
        });
}