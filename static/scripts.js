<<<<<<< Updated upstream
window.onload = () => {
    getState()
    let run_btn = document.getElementById("run_app")
    run_btn.addEventListener('click', () => {
        postData('state', data = {
            'set_state': 'on'
        })
        getState();
=======
window.onload = function() {
    const filter_input = document.querySelector("#filter_input");
    // const filter_list = document.querySelector("#filter_list");
    // const filter_options = document.querySelectorAll(".filter_option");
    const checkbox_options = document.querySelectorAll(".checkbox-option")
    const edit_panel = document.querySelector(".edit-panel");
    const edit_btns = document.querySelectorAll("#edit-btn");
    const exit_btn = document.querySelector("#exit-btn")

    filter_input.addEventListener('keyup', function() {
        filter_func(this.value, checkbox_options);
>>>>>>> Stashed changes
    })
    let stop_btn = document.getElementById("stop_app")
    stop_btn.addEventListener('click', () => {
        postData('state', data = {
            'set_state': 'off'
        })
        getState();
    })
<<<<<<< Updated upstream
=======
    exit_btn.addEventListener('click', () => {
        edit_panel.classList.remove("edit-panel__active");
    })
    edit_btns.forEach(function(edit_btn) {
        edit_btn.addEventListener("click", () => {
            edit_panel.classList.toggle("edit-panel__active")
            var inputs = edit_panel.querySelectorAll("input");
            var id = edit_btn.parentElement.parentElement.querySelector(".row_id").innerText;
            var channel = edit_btn.parentElement.parentElement.querySelector(".row_channel").innerText;
            var whitelist = edit_btn.parentElement.parentElement.querySelector(".row_whitelist").innerText;
            console.log(whitelist);
            inputs[0].value = parseInt(id, 10);
            inputs[1].value = channel;
            inputs[2].value = whitelist;
        })

    })
    
>>>>>>> Stashed changes
}


function postData(url = '', data = {}) {
    // Default options are marked with *
    return fetch(url, {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // no-referrer, *client
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        })
        .then(response => response.json()); // parses JSON response into native JavaScript objects
    }

function getState(){
    fetch('/state')
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            document.getElementById("app_state").innerText = `App is ${myJson['current_state']}`
        })
}