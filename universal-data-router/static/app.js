/**
 * Universal Data Router (Revvel) - Frontend Application
 */

const API_BASE = 'http://localhost:8000';

// State
let selectedItems = new Set();
let currentFilter = {};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadItems();
    setupEventListeners();
    setupWebSocket();
});

// Setup event listeners
function setupEventListeners() {
    // Auto-sort button
    document.getElementById('auto-sort-btn').addEventListener('click', runAutoSort);
    
    // Auto-download button
    document.getElementById('auto-download-btn').addEventListener('click', runAutoDownload);
    
    // Export button
    document.getElementById('export-btn').addEventListener('click', openRoutingModal);
    
    // Delete button
    document.getElementById('delete-btn').addEventListener('click', deleteSelected);
    
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const range = e.target.dataset.range;
            const category = e.target.dataset.category;
            const source = e.target.dataset.source;
            
            if (range) applyDateRangeFilter(range);
            if (category) applyFilter('category', category);
            if (source) applyFilter('source', source);
            
            // Visual feedback
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
        });
    });
    
    // Modal actions
    document.getElementById('send-btn').addEventListener('click', sendToDestinations);
    document.getElementById('cancel-btn').addEventListener('click', closeRoutingModal);
    
    // Search
    document.getElementById('search-bar').addEventListener('input', debounce(handleSearch, 300));
}

// Load items from API
async function loadItems(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE}/items?${params}`);
        const data = await response.json();
        
        renderItems(data.items);
    } catch (error) {
        console.error('Failed to load items:', error);
        showNotification('Failed to load items', 'error');
    }
}

// Render items
function renderItems(items) {
    const container = document.getElementById('items-list');
    container.innerHTML = '';
    
    if (items.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No items found</p>';
        return;
    }
    
    items.forEach(item => {
        const card = createItemCard(item);
        container.appendChild(card);
    });
}

// Create item card
function createItemCard(item) {
    const card = document.createElement('div');
    card.className = 'item-card';
    card.dataset.itemId = item.id;
    
    const timeAgo = getTimeAgo(new Date(item.created_at));
    
    card.innerHTML = `
        <input type="checkbox" class="item-checkbox" aria-label="Select item ${item.id}">
        <div class="item-content">
            <h4>${item.metadata?.subject || item.metadata?.filename || 'Untitled'}</h4>
            <p class="item-meta">
                ${item.metadata?.from || 'Unknown source'} | 
                ${item.category || 'Uncategorized'} | 
                ${timeAgo}
            </p>
            <div class="item-tags">
                ${item.tags ? item.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : ''}
            </div>
        </div>
    `;
    
    // Checkbox handler
    const checkbox = card.querySelector('.item-checkbox');
    checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            selectedItems.add(item.id);
        } else {
            selectedItems.delete(item.id);
        }
    });
    
    return card;
}

// Apply filter
function applyFilter(type, value) {
    currentFilter = { ...currentFilter, [type]: value };
    loadItems(currentFilter);
}

// Apply date range filter
async function applyDateRangeFilter(range) {
    try {
        const response = await fetch(`${API_BASE}/items/date-range/${range}`);
        const data = await response.json();
        renderItems(data.items);
    } catch (error) {
        console.error('Failed to apply date range filter:', error);
    }
}

// Handle search
function handleSearch(e) {
    const query = e.target.value;
    // TODO: Implement full-text search
    console.log('Searching for:', query);
}

// Run auto-sort
async function runAutoSort() {
    try {
        const response = await fetch(`${API_BASE}/processing/auto-sort/run`, {
            method: 'POST'
        });
        const data = await response.json();
        showNotification(`Auto-sort queued for ${data.items} items`, 'success');
        setTimeout(() => loadItems(), 2000);
    } catch (error) {
        console.error('Failed to run auto-sort:', error);
        showNotification('Failed to run auto-sort', 'error');
    }
}

// Run auto-download
async function runAutoDownload() {
    try {
        const response = await fetch(`${API_BASE}/processing/auto-download/run`, {
            method: 'POST'
        });
        showNotification('Auto-download started', 'success');
    } catch (error) {
        console.error('Failed to run auto-download:', error);
        showNotification('Failed to run auto-download', 'error');
    }
}

// Open routing modal
function openRoutingModal() {
    if (selectedItems.size === 0) {
        showNotification('Please select items to export', 'error');
        return;
    }
    
    const modal = document.getElementById('routing-modal');
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
}

// Close routing modal
function closeRoutingModal() {
    const modal = document.getElementById('routing-modal');
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
}

// Send to destinations
async function sendToDestinations() {
    const selectedDestinations = [];
    document.querySelectorAll('.destination-list input:checked').forEach(input => {
        selectedDestinations.push(input.value);
    });
    
    if (selectedDestinations.length === 0) {
        showNotification('Please select at least one destination', 'error');
        return;
    }
    
    try {
        // TODO: Map destination names to IDs
        const response = await fetch(`${API_BASE}/routing/jobs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                item_ids: Array.from(selectedItems),
                destination_ids: [1, 2] // Placeholder
            })
        });
        
        const data = await response.json();
        showNotification(`Routing job created: ${data.id}`, 'success');
        closeRoutingModal();
        selectedItems.clear();
        loadItems();
    } catch (error) {
        console.error('Failed to create routing job:', error);
        showNotification('Failed to create routing job', 'error');
    }
}

// Delete selected items
async function deleteSelected() {
    if (selectedItems.size === 0) {
        showNotification('Please select items to delete', 'error');
        return;
    }
    
    if (!confirm(`Delete ${selectedItems.size} items?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/items`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Array.from(selectedItems))
        });
        
        const data = await response.json();
        showNotification(`Deleted ${data.deleted} items`, 'success');
        selectedItems.clear();
        loadItems();
    } catch (error) {
        console.error('Failed to delete items:', error);
        showNotification('Failed to delete items', 'error');
    }
}

// Setup WebSocket for real-time updates
function setupWebSocket() {
    const ws = new WebSocket('ws://localhost:8000/ws/updates');
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('WebSocket message:', data);
        
        if (data.type === 'ITEM_ADDED' || data.type === 'ITEM_UPDATED') {
            loadItems();
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

// Utility: Show notification
function showNotification(message, type = 'info') {
    // Visual notification for accessibility
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'polite');
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Utility: Get time ago
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
}

// Utility: Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
