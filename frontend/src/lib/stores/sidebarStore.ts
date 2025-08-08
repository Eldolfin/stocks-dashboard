import { writable } from 'svelte/store';

const SIDEBAR_COLLAPSED_KEY = 'sidebarCollapsed';

// Initialize with value from localStorage or default to false
const initialCollapsedState =
	typeof localStorage !== 'undefined'
		? JSON.parse(localStorage.getItem(SIDEBAR_COLLAPSED_KEY) || 'false')
		: false;

export const isSidebarCollapsed = writable<boolean>(initialCollapsedState);

// Subscribe to changes and update localStorage
isSidebarCollapsed.subscribe((value) => {
	if (typeof localStorage !== 'undefined') {
		localStorage.setItem(SIDEBAR_COLLAPSED_KEY, JSON.stringify(value));
	}
});
