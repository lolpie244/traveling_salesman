import { Backend } from "../services/backend.js";

const button = document.getElementById("signupButton");
const signup_form = document.getElementById("signupForm");

async function signup() {
    const data = new FormData(signup_form);
    const success = await Backend.sing_up(data.get("username"), data.get("password"), data.get("confirmed_password"));
    if(success)
        window.location = "../pages/index.html";

}

button.addEventListener("click", signup);