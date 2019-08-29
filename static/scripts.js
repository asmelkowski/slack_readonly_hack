window.onload = () => {
    var submit = document.getElementById('submit-btn');
    submit.addEventListener('click', function () {
        let channel = document.forms[0][0].value;
        let whitelist = document.forms[0][1].value;
        document.forms[0][0].value = '';
        document.forms[0][1].value = '';
        postData('/channels', data = {
                "channel": channel,
                "whitelist": whitelist
            })
            .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
            .catch(error => console.error(error));

        fetch('/channels')
            .then(function (response) {
                return response.json();
            })
            .then(function (myJson) {
                myJson.forEach(function (channel) {
                    document.getElementById("table").insertAdjacentElement('beforeend', `<tr><td>channel['id']</td><td>channel['channel']</td><td>channel['whitelist']</td></tr>`})
                console.log(JSON.stringify(myJson));
            });
    })
}

// postData('http://example.com/answer', {
//         answer: 42
//     })
//     .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
//     .catch(error => console.error(error));

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