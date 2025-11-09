// Elementos del DOM
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const quickButtons = document.querySelectorAll('.quick-btn');

// Configurar hora inicial del mensaje de bienvenida
document.getElementById('initialTime').textContent = getCurrentTime();

// Event Listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize del textarea
userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
});

// Quick action buttons
quickButtons.forEach(button => {
    button.addEventListener('click', () => {
        const text = button.getAttribute('data-text');
        userInput.value = text;
        sendMessage();
    });
});

// Funciones principales
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
}

function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // Agregar mensaje del usuario al chat
    addUserMessage(message);

    // Limpiar input
    userInput.value = '';
    userInput.style.height = 'auto';

    // Mostrar indicador de escritura
    showTypingIndicator();

    // Enviar mensaje al servidor
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remover indicador de escritura
        removeTypingIndicator();

        // Agregar respuesta del bot
        addBotMessage(data.respuesta);
    })
    .catch(error => {
        console.error('Error:', error);
        removeTypingIndicator();
        addBotMessage('Lo siento, hubo un error. Por favor intenta nuevamente. 😔');
    });
}

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="message-bubble">
                <p>${escapeHtml(message)}</p>
            </div>
            <span class="message-time">${getCurrentTime()}</span>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    // Convertir saltos de línea a <br> y procesar el formato
    const formattedMessage = formatBotMessage(message);

    messageDiv.innerHTML = `
        <div class="message-avatar bot-avatar">
            <img src="/static/images/bot-avatar.svg" alt="Bot">
        </div>
        <div class="message-content">
            <div class="message-bubble">
                ${formattedMessage}
            </div>
            <span class="message-time">${getCurrentTime()}</span>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function formatBotMessage(message) {
    // Escapar HTML
    let formatted = escapeHtml(message);

    // Convertir saltos de línea a <br>
    formatted = formatted.replace(/\n/g, '<br>');

    // Convertir ** en negritas (Markdown style)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Convertir listas con • o -
    formatted = formatted.replace(/^[•\-]\s(.+)$/gm, '<li>$1</li>');

    // Si hay <li>, envolverlos en <ul>
    if (formatted.includes('<li>')) {
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }

    return formatted;
}

function showTypingIndicator() {
    const template = document.getElementById('typingTemplate');
    const clone = template.content.cloneNode(true);
    clone.querySelector('.typing-indicator').id = 'typingIndicator';
    chatMessages.appendChild(clone);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Easter egg: Shake animation cuando se recibe un mensaje muy positivo
function celebratePositiveMessage() {
    const emojis = ['🎉', '✨', '🌟', '💫', '🎊'];
    const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];

    // Cambiar temporalmente el icono del logo
    const logoIcon = document.querySelector('.logo-icon');
    const originalEmoji = logoIcon.textContent;
    logoIcon.textContent = randomEmoji;

    setTimeout(() => {
        logoIcon.textContent = originalEmoji;
    }, 2000);
}

// Focus automático en el input al cargar
userInput.focus();

// Prevenir submit del formulario si se presiona Enter
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat Motivacional cargado correctamente 💙');
});
