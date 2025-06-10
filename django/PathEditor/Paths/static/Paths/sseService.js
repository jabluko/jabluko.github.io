"use strict";
console.log("loaded");
class SSENotificationService {
    constructor(endpoint) {
        this.eventSource = null;
        this.endpoint = endpoint;
    }
    start() {
        if (this.eventSource)
            return;
        console.log('Starting SSE connection to:', this.endpoint);
        this.eventSource = new EventSource(this.endpoint);
        this.eventSource.onopen = () => console.log('SSE connected.');
        this.eventSource.onerror = (e) => {
            var _a;
            console.error('SSE error:', e);
            (_a = this.eventSource) === null || _a === void 0 ? void 0 : _a.close();
            this.eventSource = null;
            setTimeout(() => this.start(), 5000);
        };
        this.eventSource.addEventListener('newBoard', (event) => {
            console.log("event:" + event.data);
            const data = JSON.parse(event.data);
            showToast(`Utworzono nową planszę: ${data.board_name}.`, 'success');
        });
        this.eventSource.addEventListener('newPath', (event) => {
            console.log("event:" + event.data);
            const data = JSON.parse(event.data);
            showToast(`Użytkownik ${data.creator_username} zapisał ścieżkę na planszy: ${data.background_name}.`, 'info');
        });
    }
    stop() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
            console.log('SSE disconnected.');
        }
    }
}
const sseService = new SSENotificationService('/sse/notifications/');
function showToast(message, type) {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('Toast container not found.');
        return;
    }
    console.log('Showing toast:', message, 'Type:', type);
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.backgroundColor = type === 'success' ? '#4CAF50' : type === 'info' ? '#2196F3' : '#f44336';
    toast.style.color = 'white';
    toast.style.padding = '10px 15px';
    toast.style.borderRadius = '5px';
    toast.style.opacity = '1';
    toast.style.transition = 'opacity 0.5s ease-in-out';
    container.appendChild(toast);
    setTimeout(() => {
        console.log('Removing toast:', message);
        toast.remove();
    }, 5000);
}
//# sourceMappingURL=sseService.js.map