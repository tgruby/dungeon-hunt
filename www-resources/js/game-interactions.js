// function to make setTimeout act as a java sleep(): https://medium.com/dev-genius/how-to-make-javascript-sleep-or-wait-d95d33c99909
const sleepNow = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

// Function to send a command to the server.
function connect(term, url) {
    fetch(url, {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
    .then((resp) => resp.json()) // Transform the data into json
    .then(function(data) {
        process(term, data.canvas, data.sound, data.delay, data.animation, data.interaction_type)
    })
    .catch((error) => console.error("DoT Error: " + error.message))
}

// Refresh the screen and process the response from the server.
async function process(term, canvas, sound, delay, animation, interactionType) {
    term.clear()

    for (let i = 0; i < canvas.length; i++) term.print(canvas[i]);
    if (sound) document.getElementById(sound).play();

    if (animation) {
        if (animation === "confetti") confetti.start(3000);
        if (animation === "fireworks") await fireworks();
    }


    // Pause the functioning thread
    await sleepNow(delay)

    if (interactionType === 'key_press') {
        term.key('', function (action) { connect(term, '/api/v1/game/action/' + action) })
    } else {
        term.input('', function (action) { connect(term, '/api/v1/game/action/' + action) })
    }
}

// Function to send a kill request to the game, ending the game and removing the game token from the session.
function endGame() {
    fetch('/api/v1/game/end-game', {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
        .then((resp) => resp.json()) // Transform the data into json
        .then(function(data) {
            // do nothing with the response...
            location.reload(true);
        })
        .catch((error) => console.error("DoT Error: " + error.message))
}

// Function to make it easier for the user to zoom in the screen.
function zoom(percentChange) {
    let pageZoom = document.body.style.zoom
    if (pageZoom.length === 0) pageZoom = "100%";
    pageZoom = pageZoom.slice(0, -1)
    pageZoom = parseInt(pageZoom)
    pageZoom = pageZoom + percentChange
    document.body.style.zoom = pageZoom + "%";
}

async function fireworks() {

    animate();
    launchInterval();

    let fireworksBlur = document.getElementById("blurCanvas");
    let fireworksRender = document.getElementById("renderingCanvas");
    fireworksBlur.style.zIndex = "1";
    fireworksRender.style.zIndex = "1";

    for (let i = 0; i < 10; i++) {
        launchFuse(i);
        await sleepNow(200);
    }

    await sleepNow(10000);
    fireworksBlur.style.zIndex = "-1";
    fireworksRender.style.zIndex = "-1";
}