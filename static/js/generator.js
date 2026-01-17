class PasswordGenerator {
    constructor() {
        this.lengthSlider = document.getElementById('length-slider');
        this.lengthValue = document.getElementById('length-value');
        this.optUppercase = document.getElementById('opt-uppercase');
        this.optLowercase = document.getElementById('opt-lowercase');
        this.optNumbers = document.getElementById('opt-numbers');
        this.optSymbols = document.getElementById('opt-symbols');
        this.generateBtn = document.getElementById('generate-btn');
        this.bulkGenerateBtn = document.getElementById('bulk-generate-btn');
        this.passwordInput = document.getElementById('generated-password');
        this.copyBtn = document.getElementById('copy-btn');
        this.visibilityToggle = document.getElementById('visibility-toggle');
        this.entropyValue = document.getElementById('entropy-value');
        this.entropyRating = document.getElementById('entropy-rating');
        this.copyFeedback = document.getElementById('copy-feedback');
        this.init();
    }
    
    init() {
        console.log('Initializing Password Generator...');
        
        this.lengthSlider.addEventListener('input', () => this.updateLength());
        [this.optUppercase, this.optLowercase, this.optNumbers, this.optSymbols]
            .forEach(opt => opt.addEventListener('change', () => this.updateEntropy()));
        
        this.generateBtn.addEventListener('click', () => this.generate());
        this.bulkGenerateBtn.addEventListener('click', () => this.showBulkModal());
        this.copyBtn.addEventListener('click', () => this.copyPassword());
        this.visibilityToggle.addEventListener('click', () => this.toggleVisibility());
        
        this.updateEntropy();
        
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'g') {
                e.preventDefault();
                this.generate();
            }
        });
        
        console.log('Password Generator initialized');
    }
    
    updateLength() {
        this.lengthValue.textContent = this.lengthSlider.value;
        this.updateEntropy();
    }
    
    getOptions() {
        return {
            uppercase: this.optUppercase.checked,
            lowercase: this.optLowercase.checked,
            numbers: this.optNumbers.checked,
            symbols: this.optSymbols.checked
        };
    }
    
    async updateEntropy() {
        const options = this.getOptions();
        const length = parseInt(this.lengthSlider.value);
        
        if (!Object.values(options).some(v => v)) {
            this.entropyValue.textContent = '0.0 bits';
            this.entropyRating.textContent = '(Select at least one option)';
            return;
        }
        
        try {
            const result = await apiCall('/entropy/calculate', 'POST', { length, options });
            this.entropyValue.textContent = `${result.entropy} bits`;
            this.entropyRating.textContent = `(${result.rating})`;
        } catch (error) {
            console.error('Entropy calculation error:', error);
        }
    }
    
    async generate() {
        const options = this.getOptions();
        const length = parseInt(this.lengthSlider.value);
        
        if (!Object.values(options).some(v => v)) {
            alert('Please select at least one character set');
            return;
        }
        
        this.generateBtn.disabled = true;
        this.generateBtn.innerHTML = '<span class="loading"></span> Generating...';
        
        try {
            const result = await apiCall('/generate', 'POST', { length, options });
            this.passwordInput.value = result.password;
            this.copyBtn.disabled = false;
            this.visibilityToggle.disabled = false;
            this.entropyValue.textContent = `${result.entropy} bits`;
            this.entropyRating.textContent = `(${result.strength_estimate})`;
            this.passwordInput.classList.add('pulse');
            setTimeout(() => this.passwordInput.classList.remove('pulse'), 500);
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            this.generateBtn.disabled = false;
            this.generateBtn.textContent = 'Generate Password';
        }
    }
    
    async copyPassword() {
        const password = this.passwordInput.value;
        if (!password) return;
        const success = await copyToClipboard(password);
        if (success) {
            showFeedback(this.copyFeedback, '✓ Copied to clipboard!');
            this.copyBtn.classList.add('pulse');
            setTimeout(() => this.copyBtn.classList.remove('pulse'), 500);
        }
    }
    
    toggleVisibility() {
        const type = this.passwordInput.type === 'password' ? 'text' : 'password';
        this.passwordInput.type = type;
        this.visibilityToggle.textContent = type === 'password' ? '👁️' : '🙈';
    }
    
    async showBulkModal() {
        // Ensure modal content is loaded
        const bulkModal = document.getElementById('bulk-modal');
        if (!bulkModal) {
            console.error('Modal not found');
            return;
        }
    
        // Show modal first (in case elements are inside)
        bulkModal.classList.remove('hidden');
    
        // Wait a tick for DOM to update
        await new Promise(resolve => setTimeout(resolve, 0));
    
        // Now populate the values
        const currentLength = this.lengthSlider.value;
        const bulkLengthSlider = document.getElementById('bulk-length');
        const bulkLengthValue = document.getElementById('bulk-length-value');

        console.log('Setting bulk modal length to', currentLength); 
        console.log('bulkLengthSlider:', bulkLengthSlider); 
        console.log('bulkLengthValue:', bulkLengthValue);
    
        if (bulkLengthSlider) {
            bulkLengthSlider.value = currentLength;

            // Trigger any UI updates
            bulkLengthSlider.dispatchEvent(new Event('input'));
        }
    
        if (bulkLengthValue) {
            bulkLengthValue.textContent = currentLength;
        }
}
}