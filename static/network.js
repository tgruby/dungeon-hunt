// Basic function to send a command and get the response.
function connectToServer(term, url) {
    fetch(url, {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
        .then((resp) => resp.json()) // Transform the data into json
        .then(function(data) {

            term.clear()

            for (let i = 0; i < data.canvas.length; i++) term.print(data.canvas[i]);
            if (data.sound) document.getElementById(data.sound).play();

            term.sleep(250)

            term.input('', function (input) {
                connectToServer(term, constructUrl(data.game_token, input))
            })
        })
        .catch(error => console.log(error))
}

function constructUrl(gameToken, action) {
    if (!gameToken) {
        return '/api/v1/start/action/' + action
    } else {
        return '/api/v1/game/' + gameToken + '/action/' + action
    }
}