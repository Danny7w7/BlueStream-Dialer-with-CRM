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
    clearInput()
}

function addMessageInTheBox(message, send) {
    const chatBoxDiv = document.getElementById('chat-box');

    // Crear un nuevo div con las clases 'd-flex' y 'justify-content-end' o 'justify-content-start'
    const messageBoxDiv = document.createElement('div');
    messageBoxDiv.classList.add('d-flex', send ? 'justify-content-end' : 'justify-content-start');

    // Crear un nuevo p con las clases 'message-box' y 'me-5' o 'ms-5'
    const newP = document.createElement('p');
    newP.classList.add('message-box', send ? 'ms-5' : 'me-5');

    // Verificar si el mensaje contiene un enlace de consentimiento y convertirlo a HTML
    const linkPattern = /(Consent #\d \((https:\/\/segurodesaludgratis\.com\/[^\)]+)\)|www\.segurodesaludgratis\.com\/enlaces)/g;
    message = message.replace(linkPattern, (match, p1, p2) => {
        if (p2) {
            return `Consent #1 (<a href="${p2}">Click aquí</a>)`;
        } else {
            return `<a href="https://${match}">${match}</a>`;
        }
    });

    // Verificar si el mensaje contiene un número de teléfono y convertirlo a un enlace 'tel:'
    const phonePattern = /18559636900/g;
    message = message.replace(phonePattern, (match) => {
        return `<a href="tel:${match}">${match}</a>`;
    });

    // Asignar el contenido HTML al nuevo p
    newP.innerHTML = message;

    // Agregar el p al nuevo div
    messageBoxDiv.appendChild(newP);

    // Agregar el nuevo div al chat box
    chatBoxDiv.appendChild(messageBoxDiv);
}

function hasMessagesInChatBox() {
    chatBoxDiv = document.getElementById('chat-box')
    // Devuelve 0 si chatBoxDiv no tiene mensajes, de lo contrario devuelve la ID
    // EL 1 SE TIENE QUE CAMBIAR AL HACER LA FUNCION DE QUE TE CARGUE LOS DIFERENTES CHATS
    return chatBoxDiv.children.length === 0 ? 0 : 1;
}

function clearInput(){
    document.getElementById('message').value = ''
}