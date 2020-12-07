// function to make setTimeout act as a java sleep(): https://medium.com/dev-genius/how-to-make-javascript-sleep-or-wait-d95d33c99909
const sleepNow = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

// Send the Gamer Tag to the server and then display the leaderboard.
function collectGamerTag(tag) {
    if (tag.trim().length > 0) {
        fetch('/api/v1/gamer-tag/' + tag, {
            method: 'Get',
            headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
        })
        .then((resp) => resp.json()) // Transform the data into json
        .then(function(data) {
            displayLeaderBoard();
        })
        .catch((error) => console.error("DoT Error: " + error.message))
    }
}

function displayLeaderBoard() {
    fetch('/api/v1/leader-board', {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
    .then((resp) => resp.json()) // Transform the data into json
    .then(function(data) {
        term.clear()

        for (let i = 0; i < data.canvas.length; i++) term.print(data.canvas[i]);
        if (data.sound) document.getElementById(data.sound).play();

        term.input('', function (input) {
            connectToServer(term, '/api/v1/start');
        })
    })
    .catch((error) => console.error("DoT Error: " + error.message))
}

// Basic function to send a command and get the response.
function connectToServer(term, url) {
    fetch(url, {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
    .then((resp) => resp.json()) // Transform the data into json
    .then(function(data) {
        processResponse(term, data.game_token, data.canvas, data.sound, data.sleep)
    })
    .catch((error) => console.error("DoT Error: " + error.message))
}

async function processResponse(term, token, canvas, sound, sleep) {
    term.clear()

    for (let i = 0; i < canvas.length; i++) term.print(canvas[i]);
    if (sound) document.getElementById(sound).play();

    // Pause the functioning thread
    await sleepNow(sleep)

    term.key('', function (input) {
        connectToServer(term, constructUrl(token, input))
    })
}

function constructUrl(gameToken, action) {
    if (typeof gameToken === 'undefined') {
        return '/api/v1/leader-board'
    } else {
        return '/api/v1/game/action/' + action
    }
}
