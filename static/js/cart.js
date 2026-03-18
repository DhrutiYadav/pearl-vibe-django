document.addEventListener('DOMContentLoaded', function () {
    var updateBtns = document.getElementsByClassName('update-cart');

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {

            var productId = this.dataset.product;
            var action = this.dataset.action;

            // ✅ Try to get size & color from button (cart page)
            var size = this.dataset.size || "";
            var color = this.dataset.color || "";

            // 🔒 Fix Django None → JS string issue
            if (size === "None") size = "";
            if (color === "None") color = "";

            if (user === 'AnonymousUser') {
                alert("Please login to manage cart");
                return;
            }

            // ✅ If not found, get from selected inputs (product detail page)
            if (!size) {
                var sizeInput = document.getElementById("selected-size");
                if (sizeInput && sizeInput.value) {
                    size = sizeInput.value;
                }
            }

            if (!color) {
                var colorInput = document.getElementById("selected-color");
                if (colorInput && colorInput.value) {
                    color = colorInput.value;
                }
            }
            // 🚨 VALIDATION
            var sizeOptions = document.querySelectorAll(".size-option") || [];
            var colorOptions = document.querySelectorAll(".color-option") || [];

            var hasSizeOptions = sizeOptions.length > 0;
            var hasColorOptions = colorOptions.length > 0;

            if (hasSizeOptions && !size) {
                alert("Please select size");
                return;
            }

            if (hasColorOptions && !color) {
                alert("Please select color");
                return;
            }
            console.log("🛒 FINAL DATA:", {
                productId,
                action,
                size,
                color
            });
            // ✅ Send to backend
            updateUserOrder(productId, action, size, color);
        });
    }
    /* ---------- LOGGED IN USER ---------- */
    function updateUserOrder(productId, action, size, color) {
        console.log('User is logged in, sending data..');

        var url = '/update_item/';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action,
                'size': size,
                'color': color
            })
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Data:', data);
            location.reload();
        });
    }
    checkEnableButton();
});