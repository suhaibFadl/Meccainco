var chatBody = document.querySelector('#chat-body');
chatBody.scrollTop = chatBody.scrollHeight;

function getCurrentDateTime() {
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    const currentDate = new Date();

    const month = months[currentDate.getMonth()];
    const day = currentDate.getDate();
    const year = currentDate.getFullYear();
    let hour = currentDate.getHours();
    let ampm = "a.m.";

    // Convert hour to 12-hour format and determine "a.m." or "p.m."
    if (hour >= 12) {
        ampm = "p.m.";
        if (hour > 12) {
            hour -= 12;
        }
    }

    const minutes = currentDate.getMinutes();

    // Add leading zeros to minutes if it's a single digit
    const formattedMinutes = (minutes < 10) ? `0${minutes}` : minutes;

    const formattedDateTime = `${month} ${day}, ${year}, ${hour}:${formattedMinutes} ${ampm}`;
    return formattedDateTime;
}

const receiver_id = JSON.parse(document.getElementById('receiverId').textContent);
const sender_id = JSON.parse(document.getElementById('senderId').textContent);
const sender = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('receiver-username').textContent);
const my_image = JSON.parse(document.getElementById('my-image').textContent);
const contact_image = JSON.parse(document.getElementById('contact-image').textContent);
console.log(my_image, contact_image);
const chat_socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + receiver_id
    + '-'
    + sender_id
    + '/'
);

chat_socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

chat_socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

chat_socket.onerror = function(e){
    console.log("ERROR OCCURED");
    console.log(e)
}

chat_socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    console.log(data)
    console.log(data.sender, sender)
    if(data.sender == sender){
        document.querySelector('#chat-body').innerHTML += `
        <div class="chat-message-right pb-4">
        <div> 
            <img src="${my_image}" class="rounded-circle mr-1" alt="Chris Wood" width="40" height="40"> 
           
            
        </div>
        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
            <div class="font-weight-bold mb-1">${data.sender}</div>
            <p>${data.message}</p>
            <div class="text-muted small text-nowrap mt-2">${getCurrentDateTime()}</div>
        </div>
    </div>`
    }else{
        document.querySelector('#chat-body').innerHTML += `
        <div class="chat-message-left pb-4">
        <div> 
            <img src="${contact_image}"
                class="rounded-circle mr-1" alt="Chris Wood" width="40" height="40" alt="Pic"> 
           
            
        </div>
        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
            <div class="font-weight-bold mb-1">${data.sender}</div>
            <p>${data.message}</p>
            <div class="text-muted small text-nowrap mt-2">${getCurrentDateTime()}</div>
        </div>
    </div>`
    }
}
const message_input = document.querySelector('#message_input');
function sendMessage(){
    // const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    chat_socket.send(JSON.stringify({
        'message':message,
        'sender':sender,
        'receiver':receiver
    }));

    message_input.value = '';
}

document.querySelector('#chat-message-submit').onclick = function(e){
    sendMessage()
}

message_input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default Enter key behavior (line break)
        sendMessage(); // Call the sendMessage function
    }
});