async function sendMessage() {
    const message = document.getElementById("message").value;
    const response = await fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
    });

    const data = await response.json();
    // document.getElementById("response").innerText = data.response;
    console.log(data.response)
}