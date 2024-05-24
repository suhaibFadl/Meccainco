const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + `${store_id}orders`
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
    const order = data.data
    document.querySelector('.orders-container').innerHTML += `
    <div class="filterDiv ${order.status}">
        <hr>
        <a href="{% url 'orders:store_order' id=${order.id} %}">Details...</a>
        <p>${order.costumer}</p>
        ${order.status}
        <p>Total = ${order.total}</p>
    </div>`;
    document.querySelector('#store-orders').innerHTML += `
    
    `;

    location.reload()
}