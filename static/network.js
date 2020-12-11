// function to make setTimeout act as a java sleep(): https://medium.com/dev-genius/how-to-make-javascript-sleep-or-wait-d95d33c99909
const sleepNow = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

// Basic function to send a command and get the response.
function connect(term, url) {
    fetch(url, {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
    .then((resp) => resp.json()) // Transform the data into json
    .then(function(data) {
        process(term, data.canvas, data.sound, data.delay, data.interaction_type)
    })
    .catch((error) => console.error("DoT Error: " + error.message))
}

async function process(term, canvas, sound, delay, interactionType) {
    term.clear()

    for (let i = 0; i < canvas.length; i++) term.print(canvas[i]);
    if (sound) document.getElementById(sound).play();

    // Pause the functioning thread
    await sleepNow(delay)

    if (interactionType === 'key_press') {
        term.key('', function (action) { connect(term, '/api/v1/game/action/' + action) })
    } else {
        term.input('', function (action) { connect(term, '/api/v1/game/action/' + action) })
    }
}

// Basic function to send a command and get the response.
function endGame() {
    fetch('/api/v1/game/end-game', {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
        .then((resp) => resp.json()) // Transform the data into json
        .then(function(data) {
            // do nothing...
        })
        .catch((error) => console.error("DoT Error: " + error.message))
}