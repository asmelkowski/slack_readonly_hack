window.onload = function () {
        const filter_input = document.querySelector("#filter_input");
        // const filter_list = document.querySelector("#filter_list");
        // const filter_options = document.querySelectorAll(".filter_option");
        const checkbox_options = document.querySelectorAll(".checkbox-option");
        const edit_panel = document.querySelector(".edit-panel");
        const edit_btns = document.querySelectorAll("#edit-btn");
        const exit_btn = document.querySelector("#exit-btn");

        filter_input.addEventListener('keyup', function () {
            filter_func(this.value, checkbox_options);
        })
        filter_input.addEventListener('focus', function () {
            this.value = "";
            filter_func(this.value, checkbox_options);
        })

        exit_btn.addEventListener('click', () => {
            edit_panel.classList.remove("edit-panel__active");
        })
        edit_btns.forEach(function (edit_btn) {
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

        function filter_func(input_value, option_list) {
            option_list.forEach((element) => {
                if (!element.innerText.includes(input_value)) {
                    element.style.display = "none";
                }
                if (element.innerText.includes(input_value) || input_value == '') {
                    element.style.display = '';
                }
            })
        }
    }