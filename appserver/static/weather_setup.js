require([
    "splunkjs/mvc",
    "splunkjs/mvc/simplexml/ready!"
], function(mvc) {
    const mydiv = document.getElementById("my_form");
    const form = document.createElement("form");
    const service = mvc.createService({ owner: "nobody" });

    const label = document.createElement("label");
    label.textContent = "API Token";
    label.htmlFor = "myinput";
    label.id="mylabel"
    
    const input = document.createElement("input");
    input.type = "password";
    input.id = "myinput";
    input.placeholder = "Enter Your API Token Here";

    const submit_button = document.createElement("button");
    submit_button.type = "submit";
    submit_button.textContent = "Submit";
    submit_button.id="submit_btn"

    form.appendChild(label);
    // form.appendChild(document.createElement("br"));
    form.appendChild(input);
    form.appendChild(document.createElement("br"));
    form.appendChild(submit_button);
    mydiv.appendChild(form);

    function clean_message(){
        const existingNotifiers = document.querySelectorAll("#notifier_success, #notifier_fail");
        existingNotifiers.forEach(function(notifier) {
            notifier.remove()
        })
    }

    function handlesubmit(event) {
        event.preventDefault();
        const inputvalue = input.value;
        var ready = 1

        if (inputvalue === ""){
            clean_message()
            const notify_fail = document.createElement("p");
            notify_fail.id = "notifier_fail";
            notify_fail.textContent="Please Enter Your API Token...!";
            mydiv.appendChild(notify_fail);
            var ready = 0
        }
        if (ready==1){
            service.post('/services/resthandler', { "api_token": inputvalue })
                .then(function(response) {
                    clean_message()
                    const notify_success = document.createElement("p");
                    notify_success.textContent = response;
                    notify_success.id = "notifier_success";
                    mydiv.appendChild(notify_success);
                })
                .catch(function(error) {
                    clean_message()
                    console.error('Error:', error);
                    const notify_fail = document.createElement("p");
                    notify_fail.id = "notifier_fail";
                    notify_fail.textContent="Submission failed. Please try again.";
                    mydiv.appendChild(notify_fail);

                });
        }
    }
    form.addEventListener('submit', handlesubmit);
});
