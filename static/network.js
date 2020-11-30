// function to make setTimeout act as a java sleep(): https://medium.com/dev-genius/how-to-make-javascript-sleep-or-wait-d95d33c99909
const sleepNow = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

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

    term.input('', function (input) {
        connectToServer(term, constructUrl(token, input))
    })
}

function constructUrl(gameToken, action) {
    if (typeof gameToken === 'undefined') {
        return '/api/v1/splash-screen'
    } else if (!gameToken) {
        return '/api/v1/start/action/' + action
    } else {
        return '/api/v1/game/' + gameToken + '/action/' + action
    }
}