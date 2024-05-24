function confirm() {
    var order_note = document.getElementById('order-note');
    console.log(order_note.value)
    el = document.getElementsByClassName('quantity');
    var items_dict = {};
    for( var i =0; i < el.length; i++ ) {
        console.log(el[i])
        items_dict[el[i].getAttribute('item-id')] = el[i].value;
    }
    console.log(JSON.stringify(items_dict, null, 2));
    $.ajax({
        //url: '{% url 'orders:confirm_order'%}',
        url: confirm_order_url,
        data: {
          'items_dict': JSON.stringify(items_dict, null, 2),
          'order_note': order_note.value,
        },
        success: function (data) {
            location.reload();

        }
    });    
}

function decrement(id, min_qty) {
    var quantity = document.getElementById(`quantity-${id}`);
    var item_price = document.getElementById(`item-price-${id}`);
    var total_item_price = document.getElementById(`total-item-${id}`);
    var order_total = document.getElementById('order-total');
    var item_quantity = document.getElementById(`item-quantity-${id}`);

    if(quantity.value > min_qty || quantity.value == '') {
        quantity.value -= 1;
        order_total.innerHTML -= parseInt(item_price.innerHTML)
        item_quantity.innerHTML = quantity.value
        total_item_price.innerHTML = `\$${parseInt(quantity.value) * parseInt(item_price.innerHTML)}`

    }
    
}

function increment(id, max_qty) {
    console.log(id)
    var quantity = document.getElementById(`quantity-${id}`);
    var item_price = document.getElementById(`item-price-${id}`);
    var total_item_price = document.getElementById(`total-item-${id}`);
    var order_total = document.getElementById('order-total');
    // var item_quantity = document.getElementById(`item-quantity-${id}`);

    if(quantity.value < max_qty || quantity.value == ''){
    quantity.value = parseInt(quantity.value) + 1
    // console.log(`\$ ${item_price.innerHTML}`)
    // console.log(`${parseInt(quantity.value)}`)
    quantity.innerHTML = quantity.innerHTML
    total_item_price.innerHTML = `\$${parseInt(quantity.value) * parseInt(item_price.innerHTML)}`
    console.log(parseInt(order_total.innerHTML) , parseInt(item_price.innerHTML))
    order_total.innerHTML = parseInt(order_total.innerHTML) + parseInt(item_price.innerHTML)
    }
}

function cancel_order(itemId) {
    $.ajax({
    url: cancel_order_url,
    data: {
        'orderId': itemId,
        'user': 'customer'
    },
    success: function (data) {
        
    }
    });
};

function update_order(orderId, new_status) {
        $.ajax({
        url: update_order_url,
        data: {
            'orderId': orderId,
            'newStatus': new_status
        },
        success: function (data) {
            location.reload()   
        }
    });
};

function cancel_item(itemId) {
    $.ajax({
    url: '../../ajax/cancel_item',
    data: {
        'itemId': itemId
    },
    success: function (data) {
        if(data['data'] == 'back')
            document.referrer ? window.location = document.referrer : history.back();
        document.getElementById(`item-${itemId}`).remove()
        
    }
    });
};