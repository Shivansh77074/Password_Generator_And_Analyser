
class UIController {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.themeIcon = document.querySelector('.theme-icon');
        this.body = document.body;
        this.bulkModal = document.getElementById('bulk-modal');
        this.bulkCount = document.getElementById('bulk-count');
        this.bulkLengthSlider = document.getElementById('bulk-length');
        this.bulkLengthValue = document.getElementById('bulk-length-value');
        this.bulkGenerateConfirm = document.getElementById('bulk-generate-confirm');
        this.bulkResults = document.getElementById('bulk-results');
        this.currentBulkPasswords = [];
        
        this.init();
        this.loadTheme();
        this.initTabs();
    }
    
    init() {
        console.log('Initializing UI Controller...');
        
        // Theme toggle
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Bulk length slider
        if (this.bulkLengthSlider) {
            this.bulkLengthSlider.addEventListener('input', () => this.updateBulkLength());
        }
        
        // Modal controls
        const modalClose = document.querySelector('.modal-close');
        if (modalClose) {
            modalClose.addEventListener('click', () => this.closeModal());
        }
        
        this.bulkModal.addEventListener('click', (e) => {
            if (e.target === this.bulkModal) this.closeModal();
        });
        
        // Bulk generation
        this.bulkGenerateConfirm.addEventListener('click', () => this.generateBulk());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeModal();
            if (e.ctrlKey && e.key === 'd') {
                e.preventDefault();
                this.toggleTheme();
            }
        });
        
        console.log('UI Controller initialized');
    }
    
    initTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.getAttribute('data-tab');
                
                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked button and corresponding content
                button.classList.add('active');
                document.getElementById(`${tabName}-tab`).classList.add('active');
                
                // Show notification
                this.showNotification(`Switched to ${button.textContent.trim()}`, 'info', 2000);
            });
        });
    }
    
    showNotification(message, type = 'info', duration = 3000) {
        const container = document.getElementById('notification-container');
        if (!container) return;
        
        const notification = document.createElement('div');
        notification.className = 'notification';
        
        const colors = {
            success: '#4CAF50',
            error: '#F44336',
            warning: '#FF9800',
            info: '#2196F3'
        };
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        notification.style.background = colors[type];
        notification.innerHTML = `
            <span style="font-size: 1.3rem;">${icons[type]}</span>
            <span style="flex: 1;">${message}</span>
        `;
        
        container.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
    
    toggleTheme() {
        const isDark = this.body.classList.contains('dark-theme');
        
        if (isDark) {
            this.body.classList.remove('dark-theme');
            this.themeIcon.textContent = '🌙';
            localStorage.setItem('theme', 'light');
            this.showNotification('Light theme activated ☀️', 'success', 2000);
        } else {
            this.body.classList.add('dark-theme');
            this.themeIcon.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
            this.showNotification('Dark theme activated 🌙', 'success', 2000);
        }
    }
    
    loadTheme() {
        const savedTheme = localStorage.getItem('theme');
        
        // Default to light theme
        if (savedTheme === 'dark') {
            this.body.classList.add('dark-theme');
            this.themeIcon.textContent = '☀️';
        } else {
            this.body.classList.remove('dark-theme');
            this.themeIcon.textContent = '🌙';
        }
    }
    
    updateBulkLength() {
        if (this.bulkLengthValue) {
            this.bulkLengthValue.textContent = this.bulkLengthSlider.value;
        }
    }
    
    closeModal() {
        this.bulkModal.classList.add('hidden');
        this.bulkResults.innerHTML = '';
        this.bulkResults.classList.add('hidden');
    }
    
    async generateBulk() {
        const count = parseInt(this.bulkCount.value);
        
        if (count < 1 || count > 50) {
            this.showNotification('Count must be between 1 and 50', 'warning');
            return;
        }
        
        const generator = window.app.generator;
        const options = generator.getOptions();
        const length = parseInt(this.bulkLengthSlider.value);
        
        if (!Object.values(options).some(v => v)) {
            this.showNotification('Please select at least one character set', 'warning');
            return;
        }
        
        // Show loading with progress
        this.bulkGenerateConfirm.disabled = true;
        this.bulkGenerateConfirm.innerHTML = `
            <span class="loading"></span> Generating ${count} passwords...
        `;
        
        try {
            const result = await apiCall('/generate/bulk', 'POST', {
                length,
                count,
                options
            });
            
            this.displayBulkResults(result.passwords);
            this.showNotification(`✓ Generated ${result.passwords.length} passwords!`, 'success');
            
        } catch (error) {
            this.showNotification(`Error: ${error.message}`, 'error');
        } finally {
            this.bulkGenerateConfirm.disabled = false;
            this.bulkGenerateConfirm.textContent = 'Generate';
        }
    }
    
    displayBulkResults(passwords) {
        this.bulkResults.innerHTML = '';
        this.bulkResults.classList.remove('hidden');
        
        const header = document.createElement('div');
        header.style.cssText = 'padding: 16px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;';
        header.innerHTML = `
            <h4 style="margin: 0;">✓ Generated ${passwords.length} Passwords</h4>
            <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary" id="copy-all-bulk-btn" style="padding: 8px 16px;">
                    📋 Copy All
                </button>
                <button class="btn btn-secondary" id="download-bulk-btn" style="padding: 8px 16px;">
                    💾 Download
                </button>
            </div>
        `;
        this.bulkResults.appendChild(header);
        
        setTimeout(() => {
            document.getElementById('copy-all-bulk-btn').addEventListener('click', () => {
                this.copyAllPasswords();
            });
            document.getElementById('download-bulk-btn').addEventListener('click', () => {
                this.downloadPasswords(passwords);
            });
        }, 0);
        
        const container = document.createElement('div');
        container.style.padding = '16px';
        
        passwords.forEach((password, index) => {
            const item = document.createElement('div');
            item.className = 'bulk-password-item fade-in';
            item.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                margin-bottom: 8px;
                background: var(--bg-secondary);
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                animation-delay: ${index * 0.05}s;
            `;
            
            const passwordSpan = document.createElement('span');
            passwordSpan.textContent = password;
            
            const copyButton = document.createElement('button');
            copyButton.className = 'btn-icon';
            copyButton.textContent = '📋';
            copyButton.title = 'Copy';
            copyButton.addEventListener('click', () => this.copyBulkPassword(password, copyButton));
            
            item.appendChild(passwordSpan);
            item.appendChild(copyButton);
            container.appendChild(item);
        });
        
        this.bulkResults.appendChild(container);
        this.currentBulkPasswords = passwords;
    }
    
    async copyBulkPassword(password, button) {
        const success = await copyToClipboard(password);
        if (success) {
            button.textContent = '✓';
            button.style.background = 'var(--success)';
            button.style.color = 'white';
            setTimeout(() => {
                button.textContent = '📋';
                button.style.background = '';
                button.style.color = '';
            }, 1500);
        }
    }
    
    async copyAllPasswords() {
        if (!this.currentBulkPasswords || this.currentBulkPasswords.length === 0) return;
        
        const text = this.currentBulkPasswords.join('\n');
        const success = await copyToClipboard(text);
        
        if (success) {
            this.showNotification(`✓ Copied ${this.currentBulkPasswords.length} passwords!`, 'success');
        } else {
            this.showNotification('Failed to copy passwords', 'error');
        }
    }
    
    downloadPasswords(passwords) {
        const text = passwords.join('\n');
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `secure-passwords-${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('✓ Passwords downloaded!', 'success');
    }
}

function showAbout() {
    if (window.app && window.app.ui) {
        window.app.ui.showNotification('Secure Password Utility v2.0 - Enterprise-grade security', 'info', 4000);
    }
}

function showPrivacy() {
    if (window.app && window.app.ui) {
        window.app.ui.showNotification('All operations in-memory only. Zero data persistence.', 'info', 4000);
    }
}


