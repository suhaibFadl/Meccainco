const customer_username = JSON.parse(document.getElementById('customer-username').textContent);
const workshop_id = JSON.parse(document.getElementById('workshop_id').textContent);
console.log(document.querySelector('.reservations-container'))
const new_reservations_socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + `${workshop_id}reservations`
    + '/'
);

new_reservations_socket.onopen = function(e){
    console.log("NEW RESERVAIONS CONNECTION ESTABLISHED");
}

new_reservations_socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

new_reservations_socket.onerror = function(e){
    console.log("ERROR OCCURED");
    console.log(e)
}

new_reservations_socket.onmessage = function(e){
    console.log("HERE")
    const data = JSON.parse(e.data);
    const reservation = data.reservation
    console.log(reservation)
    // const reservation = data.reservation
    document.querySelector('.reservations-container').innerHTML += `
        <div class="filterDiv  ${reservation.status} show">
            <a href="{% url 'orders:workshop_reservation' id=${reservation.id} %}">Details</a>
            <p>${reservation.status}</p>
            <p>${reservation.customer}</p>
        </div>
        `;     

    // location.reload()
}