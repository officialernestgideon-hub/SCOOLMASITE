document.addEventListener("DOMContentLoaded", function () {

const passwordButtons = document.querySelectorAll(".password-toggle");

passwordButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        const targetId = button.getAttribute("data-target");
        const input = document.getElementById(targetId);

        if (!input) {
            return;
        }

        const icon = button.querySelector("i");

        if (input.type === "password") {

            input.type = "text";

            button.setAttribute(
                "aria-label",
                "Hide password"
            );

            if (icon) {
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");
            }

        } else {

            input.type = "password";

            button.setAttribute(
                "aria-label",
                "Show password"
            );

            if (icon) {
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
            }

        }

    });

});

});