class PasswordAnalyzer {
    constructor() {
        this.analyzeInput = document.getElementById('analyze-input');
        this.analyzeBtn = document.getElementById('analyze-btn');
        this.analyzeVisibilityToggle = document.getElementById('analyze-visibility-toggle');
        this.clearAnalyzeBtn = document.getElementById('clear-analyze-btn');
        this.strengthMeter = document.getElementById('strength-meter');
        this.strengthBar = document.getElementById('strength-bar');
        this.strengthText = document.getElementById('strength-text');
        this.strengthScore = document.getElementById('strength-score');
        this.analysisResults = document.getElementById('analysis-results');
        this.init();
    }
    
    init() {
        console.log('Initializing Password Analyzer...');
        this.analyzeBtn.addEventListener('click', () => this.analyze());
        this.analyzeVisibilityToggle.addEventListener('click', () => this.toggleVisibility());
        this.clearAnalyzeBtn.addEventListener('click', () => this.clearInput());
        this.analyzeInput.addEventListener('input', debounce(() => this.updateStrengthMeter(), 500));
        this.analyzeInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.analyze();
            }
        });
        console.log('Password Analyzer initialized');
    }
    
    toggleVisibility() {
        const type = this.analyzeInput.type === 'password' ? 'text' : 'password';
        this.analyzeInput.type = type;
        this.analyzeVisibilityToggle.textContent = type === 'password' ? '👁️' : '🙈';
    }
    
    clearInput() {
        this.analyzeInput.value = '';
        this.strengthMeter.classList.add('hidden');
        this.analysisResults.classList.add('hidden');
        this.analysisResults.innerHTML = '';
    }
    
    async updateStrengthMeter() {
        const password = this.analyzeInput.value;
        if (!password) {
            this.strengthMeter.classList.add('hidden');
            return;
        }
        
        try {
            const result = await apiCall('/analyze', 'POST', { password });
            const analysis = result.analysis;
            
            this.strengthMeter.classList.remove('hidden');
            this.strengthBar.style.width = `${analysis.score}%`;
            this.strengthBar.className = `strength-bar ${analysis.strength.toLowerCase().replace(' ', '-')}`;
            this.strengthText.textContent = analysis.strength;
            this.strengthText.className = `strength-text ${analysis.strength.toLowerCase().replace(' ', '-')}`;
            this.strengthScore.textContent = analysis.score;
        } catch (error) {
            console.error('Strength meter error:', error);
        }
    }
    
    async analyze() {
        const password = this.analyzeInput.value;
        if (!password) {
            alert('Please enter a password to analyze');
            return;
        }
        
        this.analyzeBtn.disabled = true;
        this.analyzeBtn.innerHTML = '<span class="loading"></span> Analyzing...';
        
        try {
            const result = await apiCall('/analyze', 'POST', { password });
            const analysis = result.analysis;
            this.displayResults(analysis);
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            this.analyzeBtn.disabled = false;
            this.analyzeBtn.textContent = 'Analyze Password';
        }
    }
    
    displayResults(analysis) {
        this.analysisResults.innerHTML = '';
        this.analysisResults.classList.remove('hidden');
        
        const html = `
            <div class="result-section fade-in">
                <h3>📊 Metrics</h3>
                <div class="result-grid">
                    <div class="result-item">
                        <span class="result-icon">📏</span>
                        <div>
                            <div class="result-label">Length</div>
                            <div class="result-value">${analysis.length} characters</div>
                        </div>
                    </div>
                    <div class="result-item">
                        <span class="result-icon">🔢</span>
                        <div>
                            <div class="result-label">Entropy</div>
                            <div class="result-value">${analysis.entropy} bits</div>
                        </div>
                    </div>
                    <div class="result-item">
                        <span class="result-icon">🎨</span>
                        <div>
                            <div class="result-label">Diversity</div>
                            <div class="result-value">${Math.round(analysis.diversity_score * 100)}%</div>
                        </div>
                    </div>
                    <div class="result-item">
                        <span class="result-icon">⏱️</span>
                        <div>
                            <div class="result-label">Crack Time</div>
                            <div class="result-value">${analysis.crack_time}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="result-section fade-in">
                <h3>🔤 Character Types</h3>
                <div class="result-grid">
                    <div class="result-item">${analysis.has_uppercase ? '✅' : '❌'} Uppercase</div>
                    <div class="result-item">${analysis.has_lowercase ? '✅' : '❌'} Lowercase</div>
                    <div class="result-item">${analysis.has_numbers ? '✅' : '❌'} Numbers</div>
                    <div class="result-item">${analysis.has_symbols ? '✅' : '❌'} Symbols</div>
                </div>
            </div>
            
            ${analysis.detected_patterns && analysis.detected_patterns.length > 0 ? `
            <div class="result-section fade-in">
                <h3>⚠️ Detected Issues</h3>
                <ul class="warning-list">
                    ${analysis.detected_patterns.map(p => `<li>${p}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
            
            ${analysis.recommendations && analysis.recommendations.length > 0 ? `
            <div class="result-section fade-in">
                <h3>💡 Recommendations</h3>
                <ul class="recommendation-list">
                    ${analysis.recommendations.map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
        `;
        
        this.analysisResults.innerHTML = html;
    }
}