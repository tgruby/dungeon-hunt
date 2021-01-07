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

    if (animation) confetti.start(3000);

    // Pause the functioning thread
    await sleepNow(delay)

    if (interactionType === 'key_press') {
        term.key('', function (action) { connect(term, '/api/v1/game/action/' + action) })
    } else {
        term.input('', function (action) { connect(term, '/api/v1/game/action/' + action) })
    }
}

// Buttons on game page to emulate key presses, making it easier to play on a mobile device.
function mobileButtonPushed(emulatedKeyPress) {
    let nodes = document.querySelectorAll('input');
    for (let i = 0; i < nodes.length; i++) {
        nodes[i].onkeyup(new KeyboardEvent('keyup',{'key': emulatedKeyPress}));
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

let itemsRendered = false;

// Toggles the equipment viewer modal display
function toggleModal() {

    if (!itemsRendered) {
        initializeModelingEngine();
        itemsRendered = true;
    }

    let modal = document.getElementById("modal"); // Get the canvas element
    if (modal.style.display === 'none') modal.style.display = 'block';
    else modal.style.display = 'none';
}

function initializeModelingEngine() {
    let canvas = document.getElementById("canvas"); // Get the canvas element
    let engine = new BABYLON.Engine(canvas, true); // Generate the BABYLON 3D engine

    /******* Add the create scene function ******/
    let createScene = function () {

        // Create the scene space
        const scene = new BABYLON.Scene(engine);
        scene.clearColor = BABYLON.Color3(0, 0, 0);

        // Add a camera to the scene and attach it to the canvas
        // Parameters: name, alpha, beta, radius, target position, scene
        const camera = new BABYLON.ArcRotateCamera("camera", 0, 2, 2, new BABYLON.Vector3(0, 0, 0));
        camera.attachControl(canvas, true);

        // Add lights to the scene
        // const light1 = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(1, 0, 1));
        const light2 = new BABYLON.HemisphericLight("light2", new BABYLON.Vector3(0, 1, 0));
        // light1.intensity = 1;
        light2.intensity = 20;

        // Add and manipulate meshes in the scene
        BABYLON.SceneLoader.ImportMeshAsync("", "/resources/models/", "broad_sword.glb");

        // Rotate the camera slightly.  Scenes render 60 frames a second.
        scene.registerBeforeRender(function () {
            camera.alpha = camera.alpha + 0.01;
        });

        return scene;
    };
    /******* End of the create scene function ******/

    let scene = createScene(); //Call the createScene function

    // Register a render loop to repeatedly render the scene
    engine.runRenderLoop(function () {
        scene.render();
    });
}