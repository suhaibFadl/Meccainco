const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + `${order_id}order`
    + '/'
);

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
    console.log(e)
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    document.querySelector('#order-status').innerHTML += `${data.status}`;
}