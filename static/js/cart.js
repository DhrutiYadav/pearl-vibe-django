var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {

		var productId = this.dataset.product;
		var action = this.dataset.action;

		// ✅ Try to get size & color from button (cart page)
		var size = this.dataset.size || "";
        var color = this.dataset.color || "";


		// ✅ If not found, get from selected inputs (product detail page)
		if (!size) {
	        var sizeInput = document.getElementById("selected-size");
	        if (sizeInput && sizeInput.value) {
		        size = sizeInput.value;
	        } else {
		        size = "";
	        }
        }


		if (!color) {
	        var colorInput = document.getElementById("selected-color");
	        if (colorInput && colorInput.value) {
		        color = colorInput.value;
	        } else {
		        color = "";
	        }
        }
        }


		console.log('productId:', productId, 'Action:', action, 'Size:', size, 'Color:', color);
		console.log('USER:', user);

		if (user === 'AnonymousUser') {
			addCookieItem(productId, action, size, color);
		} else {
			updateUserOrder(productId, action, size, color);
		}
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

/* ---------- ANONYMOUS USER ---------- */

function addCookieItem(productId, action, size, color) {
	console.log('User is not logged in');

	var key = productId + "_" + size + "_" + color;   // ✅ unique per variant

	if(action == 'add'){
        updateUserOrder(productId, action, size, color)
    }
    else if(action == 'remove'){
        updateUserOrder(productId, action, size, color)
    }
    else if(action == 'delete'){
        // send remove until item disappears
        updateUserOrder(productId, 'remove', size, color)
    }



	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
	location.reload();
}
