// Basic function to send a command and get the response.
function connectToServer(term, url) {
    if (url === "") url = "/api/v1/game/splash-screen";
    fetch(url, {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
        .then((resp) => resp.json()) // Transform the data into json
        .then(function(data) {

            term.clear()

            for (let i = 0; i < data.canvas.length; i++) term.print(data.canvas[i]);
            if (data.sound) document.getElementById(data.sound).play();

            term.input('', function (input) {
                connectToServer(term, constructUrl(data.game_token, input, term))
            })
        })
        .catch(error => console.log(error))
}

function constructUrl(gameToken, action, term) {
    if (!gameToken) {
        return '/api/v1/game/start'
    } else {
        return '/api/v1/game/' + gameToken + '/action/' + action
    }

}