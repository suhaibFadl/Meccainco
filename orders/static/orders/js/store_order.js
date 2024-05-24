function removeClassById() {
    // Get the element by its ID
    var element = document.getElementById("collapseExample");

    // Check if the element exists
    if (element) {
        // Remove the class from the element
        element.classList.remove("show");
    }
}

function update_store_order(orderId, new_status) {
    $.ajax({
        url: update_store_order_url,
        data: {
            'orderId': orderId,
            'newStatus': new_status
        },
        success: function (data) {
            location.reload()   
        }
    });
};
function store_confirm_order(orderId) {
    $.ajax({
    url: store_confirm_order_url,
    data: {
        'orderId': orderId
    },
    success: function (data) {
        document.getElementById('confirm-order').remove();
        document.querySelectorAll(".not-available").forEach(el => el.remove());
        // document.getElementsByClassName('order-control').remove();
        document.getElementById('order-status').innerHTML = 'In Progress';        
    }
    });

};

function cancel_order(orderId) {
    $.ajax({
    url: cancel_order_url,
    data: {
        'orderId': orderId
    },
    success: function (data) {
        document.referrer ? window.location = document.referrer : history.back()
    }
    });

};

function delivered_order(orderId) {
    $.ajax({
    url: delivered_order_url,
    data: {
        'orderId': orderId
    },
    success: function (data) {
        document.getElementById('order-control').remove()
        document.getElementById('order-status').innerHTML = 'Delivered';
    }
    });

};

function notAvailable(itemId) {
    $.ajax({
    url: notAvailable_url,
    data: {
        'itemId': itemId
    },
    success: function (data) {
        
        if(data.data == 'reload') location.reload();
        else{
            document.getElementById('update-btn').remove()
            unavailableBtn = document.getElementById(`unavailable-btn-${itemId}`)
            unavailableBtn.innerHTML = '<button class="btn border disabled">Unvailable</button>'
        }
        // console.log(data['data']);
        // if(data['data'] == 'back')
        //     document.referrer ? window.location = document.referrer : history.back();
        // btn = document.getElementById(`not-available-${itemId}`);
        // btn.setAttribute('disabled', 'disabled');
        // document.getElementById('order-control').remove()
        // document.getElementById('order-status').innerHTML = 'Canceled';

    }
    });
};
