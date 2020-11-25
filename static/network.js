// Basic function to send a command and get the response.
function connectToServer(term, url_modifier, action) {
    if (action === "") action = "<>";
    fetch(url_modifier+'/action/'+action, {
        method: 'Get',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
    })
        .then((resp) => resp.json()) // Transform the data into json
        .then(function(data) {
            term.clear()
            for (let i = 0; i < data.canvas.length; i++) {
                term.print(data.canvas[i]);
            }
            if (data.sound) {
                document.getElementById(data.sound).play();
            }

            term.input('', function (input) {
                connectToServer(term, url_modifier, input)
            })
        })
        .catch(error => console.log(error))
}
