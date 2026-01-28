# Secure Password Utility — Project Report

## Project Title
Secure Password Utility (Web Application)

## Abstract / Overview
I built a web-based password utility that generates cryptographically secure passwords and analyzes password strength in real time. The application provides a single-page UI with generator and analyzer tabs, backed by a Flask API that performs all security-sensitive logic in memory, with no persistence or logging of password data. The system is designed for secure, fast, and user-friendly password creation and assessment.

## Problem Statement
Users often create weak or predictable passwords and lack immediate feedback on password strength. There is a need for a secure tool that generates strong passwords, evaluates existing ones, and does so without storing or leaking sensitive data.

## Objectives
- Provide a secure password generator using a cryptographically secure random number generator.
- Offer a detailed password analyzer with scoring, entropy calculation, and pattern detection.
- Maintain a zero-persistence model where passwords are never stored or logged.
- Deliver a responsive web UI with clear feedback and usability features.

## Scope of the Project
- Web UI for password generation and analysis.
- REST API for generation, bulk generation, entropy calculation, and analysis.
- Security-focused backend with rate limiting, input validation, and response headers.
- No user accounts, storage, or server-side password history.

## System Architecture (text-based explanation)
The system uses a client-server architecture. A single-page HTML interface serves the UI and loads JavaScript modules for generator, analyzer, and UI controls. These modules call the Flask API via JSON requests. The Flask app routes requests to stateless generator/analyzer/validator components. Security middleware adds headers and enforces JSON input. The backend returns structured results to the UI for display. All password handling remains in memory for the life of each request.

## Project Structure
```
password-utility/
├── app.py                     # Flask application entry point
├── requirements.txt           # Web dependencies
├── README.md                  # Documentation
├── Deployment_instructions    # Deployment guide
├── config/
│   ├── settings.py            # Core settings shared by modules
│   └── web_settings.py        # Web-specific config (CORS, rate limits)
├── src/
│   ├── api/                   # API routes, validators, middleware
│   ├── analyzer/              # Password analysis engine
│   ├── core/                  # Security utilities/constants
│   ├── generator/             # Password generation engine
│   ├── ui/                    # Optional desktop UI modules (not used in web app)
│   └── validator/             # Policy validation
├── static/
│   ├── css/                   # Styles and themes
│   └── js/                    # Frontend logic
└── templates/
    └── index.html             # Single-page UI
```

## Technologies and Tools Used
- **Backend:** Python, Flask, Flask-CORS, Flask-Limiter.
- **Frontend:** HTML, CSS, JavaScript (vanilla).
- **Security:** Python `secrets` module, entropy calculation, pattern detection.
- **Configuration:** Environment variables for runtime settings.

## Methodology / Working Flow
1. The user selects options in the UI (length and character sets) or enters a password to analyze.
2. The frontend makes a JSON request to the appropriate API endpoint.
3. The backend validates the request and invokes the generator/analyzer.
4. Results (passwords, entropy, scores, recommendations) are returned as JSON.
5. The UI updates the display, strength meter, and recommendations in real time.

## Key Features
- Secure password generation with guaranteed character diversity.
- Bulk password generation with copy and download support.
- Real-time entropy calculation and strength rating.
- Pattern detection for common, sequential, keyboard, and repeated patterns.
- Policy-based validation with errors and warnings.
- Dark/light theme toggle, keyboard shortcuts, and responsive UI.
- Security headers, rate limiting, and input validation on the API.

## How to Use
### Installation
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in a browser.

### Web UI Usage
- **Generator:** Choose length and character sets, then click **Generate Password**.
- **Analyzer:** Enter a password and click **Analyze Password** to get scores, entropy, and recommendations.
- **Bulk Generation:** Click **Generate Multiple** to create a list, then copy or download it.

### API Endpoints (JSON)
- `POST /api/v1/generate` — Generate a single password.
- `POST /api/v1/generate/bulk` — Generate multiple passwords.
- `POST /api/v1/analyze` — Analyze password strength.
- `POST /api/v1/entropy/calculate` — Calculate entropy for given parameters.
- `GET /api/v1/health` — Health check.

## Implementation Details (high-level)
- The generator uses a cryptographically secure RNG and shuffles output to prevent predictable patterns.
- The analyzer computes entropy, diversity, and a score-based strength level, then estimates crack time.
- Pattern detection checks for common weak strings, sequential runs, keyboard patterns, and repeated characters.
- API endpoints are protected with JSON-only enforcement and consistent error handling.
- Rate limits are applied to generation and analysis endpoints to prevent abuse.

## Challenges Faced and Solutions
- **Balancing security with usability:** I ensured strong defaults (entropy calculation, diversity checks) while keeping controls simple in the UI.
- **Preventing misuse and overuse of the API:** I added rate limiting and input validation to enforce safe request patterns.
- **Maintaining zero persistence:** I kept all password data in memory and avoided any logging or storage of sensitive inputs.

## Results / Outcomes
The project delivers a secure password utility with an easy-to-use web interface, strong cryptographic generation, and comprehensive analysis. The API and UI work together to provide fast feedback without persisting sensitive data.

## Future Enhancements
- Add optional client-side-only mode for offline use.
- Expand pattern detection with language-specific dictionaries.
- Provide configurable policy profiles (e.g., NIST, enterprise presets).
- Add accessibility improvements (ARIA labels and screen reader hints).

## Conclusion
This project provides a secure, user-friendly password utility with strong backend security practices and a responsive UI. It meets the core goal of generating and analyzing passwords without persisting sensitive data, while remaining extensible for future improvements.
