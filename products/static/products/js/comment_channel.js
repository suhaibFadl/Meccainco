const product_id = JSON.parse(document.getElementById('product_id').textContent);
const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + `${product_id}product`
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
    console.log('HEEEEEEEEEEEEEre', e)
    const data = JSON.parse(e.data);
    // console.log(data.data);
    console.log("comment",data.comment);
    // for (const key in data.data) {
    //     console.log(`Key ${key}: value ${data[key]}`);
    // }
    
    document.querySelector('#comments').innerHTML += `
    <h3> <b>${data.comment.author} : </b> ${data.comment.content}</h3>
    `;
}
