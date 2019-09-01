window.onload = () => {
    getState()
    let run_btn = document.getElementById("run_app")
    run_btn.addEventListener('click', () => {
        postData('state', data = {
            'set_state': 'on'
        })
        getState();
    })
    let stop_btn = document.getElementById("stop_app")
    stop_btn.addEventListener('click', () => {
        postData('state', data = {
            'set_state': 'off'
        })
        getState();
    })
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