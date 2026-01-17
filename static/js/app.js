class PasswordUtilityApp {
    constructor() {
        this.generator = null;
        this.analyzer = null;
        this.ui = null;
        this.init();
    }
    
    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeModules());
        } else {
            this.initializeModules();
        }
    }
    
    initializeModules() {
        console.log('🔐 Initializing Secure Password Utility...');
        
        try {
            this.ui = new UIController();
            this.generator = new PasswordGenerator();
            this.analyzer = new PasswordAnalyzer();
            
            console.log('✅ Application initialized successfully');
            this.checkAPIHealth();
        } catch (error) {
            console.error('❌ Initialization error:', error);
            alert('Failed to initialize application. Please refresh the page.');
        }
    }
    
    async checkAPIHealth() {
        try {
            const result = await apiCall('/health', 'GET');
            if (result.success) {
                console.log(`✅ API Status: ${result.status}`);
            }
        } catch (error) {
            console.warn('⚠️ API health check failed:', error);
        }
    }
}

window.app = new PasswordUtilityApp();