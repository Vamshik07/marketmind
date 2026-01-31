/**
 * History Tracker - Automatically logs user actions to backend
 * Tracks: clicks, searches, form submissions, and more
 * Sends data via fetch API - no page reloads needed
 */

class HistoryTracker {
    constructor() {
        this.debounceDelay = 500; // Prevent duplicate logs within 500ms
        this.lastLoggedActions = new Map();
        this.init();
    }

    init() {
        // Attach event listeners to document
        document.addEventListener('click', (e) => this.trackClick(e), true);
        document.addEventListener('input', (e) => this.trackInput(e), true);
        document.addEventListener('change', (e) => this.trackChange(e), true);
        document.addEventListener('submit', (e) => this.trackSubmit(e), true);
        
        // Track search input specifically
        const searchInputs = document.querySelectorAll('[type="search"], [placeholder*="search" i]');
        searchInputs.forEach(input => {
            input.addEventListener('input', (e) => this.trackSearch(e));
        });
    }

    /**
     * Check if action should be logged (debounce logic)
     */
    shouldLog(key) {
        const now = Date.now();
        const lastLog = this.lastLoggedActions.get(key) || 0;
        
        if (now - lastLog > this.debounceDelay) {
            this.lastLoggedActions.set(key, now);
            return true;
        }
        return false;
    }

    /**
     * Track button/link clicks
     */
    trackClick(event) {
        const target = event.target.closest('button, a, [role="button"]');
        if (!target) return;

        // Don't track navigation links (they trigger page visits)
        if (target.tagName === 'A' && target.href && !target.href.includes('#')) {
            return;
        }

        const key = `click_${target.id || target.textContent.slice(0, 20)}`;
        if (!this.shouldLog(key)) return;

        this.logAction({
            action_type: 'click',
            metadata: {
                element_type: target.tagName,
                element_text: target.textContent.slice(0, 100),
                element_id: target.id,
                element_class: target.className
            }
        });
    }

    /**
     * Track search queries
     */
    trackSearch(event) {
        const searchTerm = event.target.value.trim();
        if (!searchTerm || searchTerm.length < 2) return;

        const key = `search_${searchTerm.slice(0, 20)}`;
        if (!this.shouldLog(key)) return;

        this.logAction({
            action_type: 'search',
            metadata: {
                search_term: searchTerm,
                search_source: event.target.placeholder || 'search'
            }
        });
    }

    /**
     * Track form input changes
     */
    trackInput(event) {
        const input = event.target;
        if (!input.name && !input.id) return;

        const key = `input_${input.name || input.id}`;
        if (!this.shouldLog(key)) return;

        this.logAction({
            action_type: 'form_input',
            metadata: {
                field_name: input.name,
                field_type: input.type,
                field_id: input.id
            }
        });
    }

    /**
     * Track select/checkbox changes
     */
    trackChange(event) {
        const input = event.target;
        if (input.tagName !== 'SELECT' && input.type !== 'checkbox' && input.type !== 'radio') return;

        const key = `change_${input.name || input.id}`;
        if (!this.shouldLog(key)) return;

        this.logAction({
            action_type: 'form_change',
            metadata: {
                field_name: input.name,
                field_type: input.tagName === 'SELECT' ? 'select' : input.type,
                field_value: input.value
            }
        });
    }

    /**
     * Track form submissions
     */
    trackSubmit(event) {
        const form = event.target;
        const key = `submit_${form.id || form.name || 'form'}`;
        
        if (!this.shouldLog(key)) return;

        this.logAction({
            action_type: 'submit',
            metadata: {
                form_id: form.id,
                form_name: form.name,
                form_action: form.action
            }
        });
    }

    /**
     * Send action to backend API
     */
    logAction(data) {
        const payload = {
            action_type: data.action_type,
            page_url: window.location.pathname,
            page_title: document.title,
            metadata: data.metadata
        };

        fetch('/api/history/log-action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }).catch(err => {
            // Fail silently - don't interrupt user experience
            console.debug('History log failed:', err);
        });
    }

    /**
     * Manually log custom actions (for API responses, etc)
     */
    logCustomAction(actionType, metadata = {}) {
        this.logAction({
            action_type: actionType,
            metadata: metadata
        });
    }
}

// Initialize tracker when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.historyTracker = new HistoryTracker();
    });
} else {
    window.historyTracker = new HistoryTracker();
}
