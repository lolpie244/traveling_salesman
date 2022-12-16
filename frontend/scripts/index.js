import { Backend } from "../services/backend.js"
import { Canvas } from "../services/canvas.js";


const canvas = new Canvas(document.getElementById("canvas"));
const clear_button = document.getElementById("clear_button");
const start_button = document.getElementById("start_button");
const stop_button = document.getElementById("stop_button");
const delay_range = document.getElementById("delay_range");
const history_button = document.getElementById("history_button")
const logout_button = document.getElementById("logout_button")
const length_text = document.getElementById("length_text")


let webSocket = null;

Backend.is_logged().then((is_logged) => {
    if(is_logged === false)
        window.location = "../pages/login.html";
});

async function add_point(event) {
    if(delay_range.value * canvas.points.length > 60)
        alert("Task should take less than 1 minutes, please reduce the number of points or delay")
    canvas.addPoint({"x": event.pageX, "y": event.pageY});
}

function switch_state(state) {

    let edit_mode_enabled = [clear_button, start_button, canvas, delay_range]
    let edit_mode_disabled = [stop_button]

    edit_mode_enabled.forEach(element => {
        element.disabled = !state
    })
    edit_mode_disabled.forEach(element => {
        element.disabled = state
    })
}

async function start(event) {
    const port = (await Backend.get_worker()).port
    canvas.clearPath();

    webSocket = new WebSocket(`ws://127.0.0.1:${port}/solver/nearest`);

    webSocket.onopen = (event) => {
        switch_state(false);
        webSocket.send(JSON.stringify({points: canvas.getRealPoints(), delay: delay_range.value}));
    }
    webSocket.onclose = (event) => {
        console.log(`Exit with code ${event.reason}`);
        switch_state(true);
    }
    webSocket.onmessage = async (event) => {
        const data = JSON.parse(event.data);
        if(data.length !== undefined) {
            length_text.textContent = data.length;
            await Backend.record_history(canvas.path, data.length);
        }
        else
            canvas.addPathPoint(data.point, data.at_start);
    }
}

async function stop(event) {
    webSocket.close();
}

async function clear(event) {
    canvas.clear();
}

async function history(event) {
    window.location = "../pages/history.html";
}

async function logout(event) {
    await Backend.log_out();
    window.location = "../pages/login.html";
}

canvas.canvas.addEventListener("click", add_point);
clear_button.addEventListener("click", clear);
start_button.addEventListener("click", start);
stop_button.addEventListener("click", stop);
history_button.addEventListener("click", history);
logout_button.addEventListener("click", logout);

window.onload = function() {
    switch_state(true)
}

