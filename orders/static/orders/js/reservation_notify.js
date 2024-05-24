const reservation_notify_socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    +'reservation-notify/'
)

reservation_notify_socket.onopen = function(e){
    console.log("CONNECTED TO RESERVATION NOTIFICATION");
}

reservation_notify_socket.onmessage = function(e){
    const data = JSON.parse(e.data) 
    console.log(data) 
    document.getElementById('services-nav').innerHTML += `
                    <span class="lbl new bg-danger">New</span>
                   `
    if(data.receiver_type == 'workshop')
        var tab = document.getElementById('workshop-reservations');
    else if(data.receiver_type == 'customer')
        var tab = document.getElementById('customer-reservations');
        
    if(data.count < 9) var count = data.count;
    else var count = '+9';
    tab.innerHTML = `<span  class="rounded bg-danger text-white float-right p-1">
    ${count}
    </span>`
    

    console.log(data.count)
}

reservation_notify_socket.onclose = function(e){
    console.log("DISCONNECTED FROM RESERVATION NOTIFICATION");
}