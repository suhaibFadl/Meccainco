function cancel_item(itemId) {
    $.ajax({
    url: cancel_item_url,
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