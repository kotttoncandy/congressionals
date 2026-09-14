import { userData } from './userData.js';

export function saveData() {
    localStorage.setItem('userData', JSON.stringify(userData));
}