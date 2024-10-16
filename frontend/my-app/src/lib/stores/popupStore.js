import { writable } from 'svelte/store';

const popupStore = writable({
    message: '',
    type: '',
    isVisible: false,
    duration: 3000,
    startTime: 0, 
});

let timeoutId;

function showNotification(message, type, duration = 3000) {
    if (timeoutId) {
        clearTimeout(timeoutId);
    }

    const startTime = Date.now();

    popupStore.set({ message, type, isVisible: true, duration, startTime });
    timeoutId = setTimeout(() => {
        popupStore.update(current => ({ ...current, isVisible: false }));
    }, duration);
}

export { popupStore, showNotification };
