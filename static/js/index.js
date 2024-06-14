async function sendMessage() {
    const message = document.getElementById("message").value;
    const response = await fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
            message: message,
            newChat: hasMessagesInChatBox()
        }),
    });

    const data = await response.json();
    addMessageInTheBox(message, true)
    addMessageInTheBox(data.response, false)
}

function addMessageInTheBox(message, send) {
    chatBoxDiv  = document.getElementById('chat-box')
    // Creo un nuevo div con las clases 'd-flex' y 'justify-content-end'
    const messageBoxDiv = document.createElement('div');
    messageBoxDiv.classList.add('d-flex', send ? 'justify-content-end' : 'justify-content-start');

    // Creo un nuevo p con las clases 'message-box' y 'me-5'
    const newP = document.createElement('p');
    newP.classList.add('message-box', send ? 'ms-5': 'me-5');
    newP.textContent = message;

    // Agrego el p al nuevo div
    messageBoxDiv.appendChild(newP);

    // Agrego el nuevo div al chat box
    chatBoxDiv.appendChild(messageBoxDiv);
}

function hasMessagesInChatBox() {
    chatBoxDiv = document.getElementById('chat-box')
    // Devuelve 0 si chatBoxDiv no tiene mensajes, de lo contrario devuelve la ID
    // EL 1 SE TIENE QUE CAMBIAR AL HACER LA FUNCION DE QUE TE CARGUE LOS DIFERENTES CHATS
    return chatBoxDiv.children.length === 0 ? 0 : 1;
}