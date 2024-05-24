const notify_socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    +'notify/'
)

notify_socket.onopen = function(e){
    console.log("CONNECTED TO NOTIFICATION");
}

// var count_badge = document.getElementById('inbox-nav')

notify_socket.onmessage = function(e){
   
    const data = JSON.parse(e.data)    
    document.getElementById('inbox-nav').innerHTML += `
                    <span class="lbl new bg-danger">New</span>
                   `
    if(data.count < 9) var count = data.count;
    else var count = '+9'

    var typeElement = document.getElementById(`type-${data.inbx_type}`);

    // Check if the element has a child "span" element
    if (typeElement.querySelector("span") !== null) {
        // If it has a child "span" element, remove it
        typeElement.querySelector("span").remove();
    }
    document.getElementById(`type-${data.inbx_type}`).innerHTML += `<span  class="rounded bg-danger text-white float-right p-1">
    ${count}
    </span>`

    // count_badge.innerHTML = data.count
}

notify_socket.onclose = function(e){
    console.log("DISCONNECTED FROM NOTIFICATION");
}