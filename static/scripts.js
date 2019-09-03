window.onload = function() {
    const filter_input = document.querySelector("#filter_input");
    // const filter_list = document.querySelector("#filter_list");
    // const filter_options = document.querySelectorAll(".filter_option");
    const checkbox_options = document.querySelectorAll(".checkbox-option")
    filter_input.addEventListener('keyup', function() {
        filter_func(this.value, checkbox_options);
    })
    filter_input.addEventListener('focus', function() {
        this.value = "";
        filter_func(this.value, checkbox_options);
    })
    
}

function filter_func(input_value, option_list) {
    option_list.forEach((element) => {
        if(!element.innerText.includes(input_value)){
            element.style.display = "none";
        }
        if(element.innerText.includes(input_value) || input_value == ''){
            element.style.display = '';
        }
    })
}