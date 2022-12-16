import { Backend } from "../services/backend.js";





const button = document.getElementById("logInButton");
const login_form = document.getElementById("loginForm");

async function login() {
    const data = new FormData(login_form);
    const success = await Backend.log_in(data.get("username"), data.get("password"));
    if(success)
        window.location = "../pages/index.html";

}

button.addEventListener("click", login);