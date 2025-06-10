class SSENotificationService {
    constructor(endpoint) {
        this.eventSource = null;
        this.endpoint = endpoint;
    }
    start() {
        if (this.eventSource)
            return;
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
            const data = JSON.parse(event.data);
            showToast(`Utworzobo nową planszę: ${data.board_name}.`, 'success');
        });
        this.eventSource.addEventListener('newPath', (event) => {
            const data = JSON.parse(event.data);
            showToast(`Użytkownik ${data.user_username} zapisał ścieżkę na planszy: ${data.board_name}.`, 'info');
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
// Globalna instancja usługi (możesz ją dostosować do swojego frameworka)
export const sseService = new SSENotificationService('/sse/notifications/');
// Prosta funkcja do wyświetlania toastów (definicja poniżej lub w osobnym pliku)
function showToast(message, type) {
    const container = document.getElementById('toast-container') || (() => {
        const div = document.createElement('div');
        div.id = 'toast-container';
        Object.assign(div.style, {
            position: 'fixed', bottom: '20px', right: '20px', zIndex: '1000',
            display: 'flex', flexDirection: 'column', gap: '10px'
        });
        document.body.appendChild(div);
        return div;
    })();
    const toast = document.createElement('div');
    toast.textContent = message;
    Object.assign(toast.style, {
        backgroundColor: type === 'success' ? '#4CAF50' : type === 'info' ? '#2196F3' : '#f44336',
        color: 'white', padding: '10px 15px', borderRadius: '5px', boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
        opacity: '1', transition: 'opacity 0.5s ease-in-out', pointerEvents: 'all'
    });
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500); // Usuń po animacji
    }, 5000); // Toast znika po 5 sekundach
}
//# sourceMappingURL=sseService.js.map