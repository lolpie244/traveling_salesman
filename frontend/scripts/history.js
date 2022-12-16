import { Canvas } from "../services/canvas.js";
import { Backend } from "../services/backend.js";

const table = document.getElementById("table");
const canvas = new Canvas(document.getElementById("canvas"));
const modal = document.getElementById("modal");

modal.addEventListener("click", () => {modal.hidden = true});

let elements = await Backend.get_history();
const keys_order = ["id", "length", "created_at"]
let id = 0

function create_button(path) {
    let btn = document.createElement("button");
    btn.innerHTML = "Display";
    btn.classList = ["btn btn-primary"];

    btn.onclick = () => {
        modal.hidden = false;
        canvas.setPath(path);
    };
    return btn;
}
function format_date(str_date) {
    const date = new Date(str_date);
    return `${date.getDate()}-${date.getMonth()}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`
}

elements.forEach(element => {
    element.id = id++;
    element.created_at = format_date(element.created_at);

    let row = table.insertRow(0);
    keys_order.forEach(key => {
        let cell = row.insertCell();
        cell.innerHTML = element[key]
    });

    let cell = row.insertCell();
    cell.appendChild(create_button(element.path));
});