// const customer_username = JSON.parse(document.getElementById('customer-username').textContent);
// const store_id = JSON.parse(document.getElementById('store_id').textContent);
console.log('Update_orders_list')
const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + `${store_id}orders`
    + '/'
);

socket.onopen = function(e){
    console.log("NEW RESERVAIONS CONNECTION ESTABLISHED");
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
    console.log(order)
    // if(customer_username != order.customer){
        document.querySelector('.orders-container').innerHTML += `
        <div class="filterDiv ${order.status} show">
            <hr>
            <a href="{% url 'orders:store_order' id=${order.id} %}">Details...</a>
            <p>${order.customer}</p>
            <p>${order.city}</p>
            ${order.status}
            <p>Total = ${order.total}</p>
        </div>`;
        // }else{
        //     document.getElementById('orders-nav').innerHTML += `
        //     <span class="lbl new bg-danger">New</span>    
        //     `;
        // }      
    }
    
    document.getElementById(`store-orders`).innerHTML = `${count}`;
    // location.reload()
