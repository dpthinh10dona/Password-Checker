// =====================================================================
// 1. PASSWORD CHECKER LOGIC (KHU VỰC TRÊN)
// =====================================================================
const checkerInput = document.getElementById('pwdInput'); // Chỉ dùng cho phần Checker ở trên
const strengthSection = document.getElementById('strengthSection');
const strengthBar = document.getElementById('strengthBar');
const clearBtn = document.getElementById('clearBtn');
const toggleVisBtn = document.getElementById('toggleVisBtn');
const reqUpper = document.getElementById('req-upper');
const reqDigit = document.getElementById('req-digit');
const reqSymbol = document.getElementById('req-symbol');
const time = document.getElementById('time');
const crackInfo = document.getElementById('crackInfo');

const regexUpper = /[A-Z]/;
const regexDigit = /[0-9]/;
const regexSymbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
const strengthColors = ['#ff4d4d', '#ff944d', '#ffd24d', '#a3ff4d', '#00c49a'];

if (checkerInput) {
    checkerInput.addEventListener('focus', () => strengthSection && strengthSection.classList.add('show'));
    checkerInput.addEventListener('blur', () => {
        setTimeout(() => { 
            if (document.activeElement !== checkerInput && strengthSection) {
                strengthSection.classList.remove('show'); 
            }
        }, 100);
    });

    checkerInput.addEventListener('input', () => {
        const val = checkerInput.value;
        if (reqUpper) reqUpper.classList.toggle('valid', regexUpper.test(val));
        if (reqDigit) reqDigit.classList.toggle('valid', regexDigit.test(val));
        if (reqSymbol) reqSymbol.classList.toggle('valid', regexSymbol.test(val));

        if (val === '') {
            if (strengthBar) {
                strengthBar.style.width = '0%';
                strengthBar.style.backgroundColor = 'transparent';
            }
            if (time) time.style.display = 'none';
            if (crackInfo) crackInfo.style.display = 'none';
            checkPasswordLeak('');
            return;
        }

        if (typeof zxcvbn === 'function') {
            const result = zxcvbn(val);
            if (strengthBar) {
                strengthBar.style.width = `${(result.score === 0 ? 20 : (result.score + 1) * 20)}%`;
                strengthBar.style.backgroundColor = strengthColors[result.score];
            }
            if (time) {
                time.style.display = 'block';
                time.textContent = result.crack_times_display.offline_slow_hashing_1e4_per_second;
            }
            if (crackInfo) crackInfo.style.display = 'block';
        }

        clearTimeout(leakCheckTimeout);
        leakCheckTimeout = setTimeout(() => checkPasswordLeak(val), 500);
    });
}

if (clearBtn) {
    clearBtn.addEventListener('click', () => {
        if (checkerInput) {
            checkerInput.value = '';
            checkerInput.dispatchEvent(new Event('input'));
            checkerInput.focus();
        }
    });
}

if (toggleVisBtn) {
    toggleVisBtn.addEventListener('click', () => {
        if (checkerInput) {
            checkerInput.type = checkerInput.type === 'password' ? 'text' : 'password';
            toggleVisBtn.textContent = checkerInput.type === 'password' ? '🙈' : '🙉';
            checkerInput.focus();
        }
    });
}

let leakCheckTimeout = null;

async function checkPasswordLeak(password) {
    const reqLeak = document.getElementById('req-leak');
    if (!reqLeak) return;

    if (!password) {
        reqLeak.classList.add('valid');
        reqLeak.innerHTML = '<div class="checkbox">✓</div> No leaks found';
        reqLeak.style.color = '';
        return;
    }

    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-1', data);
    const hashHex = Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();

    const prefix = hashHex.substring(0, 5);
    const suffix = hashHex.substring(5);

    try {
        const response = await fetch(`https://api.pwnedpasswords.com/range/${prefix}`);
        const text = await response.text();
        const match = text.split('\n').find(line => line.startsWith(suffix));

        if (match) {
            const leakCount = match.split(':')[1].trim();
            reqLeak.classList.remove('valid');
            reqLeak.innerHTML = `<div class="checkbox" style="color: #ff4d4d; border-color: #ff4d4d;">✕</div> Leaked ${Number(leakCount).toLocaleString()} times!`;
            reqLeak.style.color = '#ff4d4d';
        } else {
            reqLeak.classList.add('valid');
            reqLeak.innerHTML = '<div class="checkbox">✓</div> No leaks found';
            reqLeak.style.color = '';
        }
    } catch (error) {
        console.error("Leak check error:", error);
    }
}

// =====================================================================
// 2. GENERATOR / ENHANCER TAB UI LOGIC (KHU VỰC DƯỚI)
// =====================================================================
const btnGenerate = document.getElementById('btn-generate'); 
const tabScratch = document.getElementById('tab-scratch');
const tabInput = document.getElementById('tab-input');
const modeScratch = document.getElementById('mode-scratch');
const modeInput = document.getElementById('mode-input');

const aiLengthSlider = document.getElementById('ai-gen-length');
const aiLengthVal = document.getElementById('ai-length-val');

if (aiLengthSlider && aiLengthVal) {
    aiLengthSlider.addEventListener('input', () => {
        aiLengthVal.textContent = aiLengthSlider.value;
    });
}

if (tabScratch && tabInput && modeScratch && modeInput) {
    tabScratch.addEventListener('click', () => {
        tabScratch.classList.add('active');
        tabInput.classList.remove('active');
        modeScratch.classList.add('active');
        modeInput.classList.remove('active');
    });

    tabInput.addEventListener('click', () => {
        tabInput.classList.add('active');
        tabScratch.classList.remove('active');
        modeInput.classList.add('active');
        modeScratch.classList.remove('active');
    });
}

const lengthSlider = document.getElementById('gen-length');
const lengthValDisplay = document.getElementById('length-val');
if (lengthSlider && lengthValDisplay) {
    lengthSlider.addEventListener('input', () => lengthValDisplay.textContent = lengthSlider.value);
}

const copyBtn = document.getElementById('copy-btn');
const genResult = document.getElementById('gen-result');

if (copyBtn && genResult) {
    copyBtn.addEventListener('click', () => {
        if (genResult.value && genResult.value !== "AI is thinking..." && !genResult.value.includes("Error")) {
            genResult.select();
            document.execCommand('copy');
            const originalIcon = copyBtn.textContent;
            copyBtn.textContent = '✅';
            setTimeout(() => copyBtn.textContent = originalIcon, 1500);
        }
    });
}

// =====================================================================
// 3. API CALL LOGIC (GENERATE & ENHANCE)
// =====================================================================
if (btnGenerate) {
    btnGenerate.addEventListener('click', async () => {
        const isScratchMode = modeScratch && modeScratch.classList.contains('active');

        if (isScratchMode) {
            // --- MODE 1: FROM SCRATCH ---
            const targetLength = parseInt(lengthSlider ? lengthSlider.value : 16) || 16;
            const requestData = {
                uppercase: document.getElementById('inc-upper')?.checked ?? true,
                number: document.getElementById('inc-num')?.checked ?? true,
                special_character: document.getElementById('inc-sym')?.checked ?? true,
                length: targetLength,
                avoid_ambiguous: document.getElementById('inc-ambig')?.checked ?? false
            };

            try {
                const response = await fetch("http://127.0.0.1:8000/generate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(errorData.detail || "Đã xảy ra lỗi!");
                    return;
                }

                const result = await response.json();
                if (genResult) genResult.value = result.password;

            } catch (error) {
                console.error("Lỗi kết nối Generator:", error);
                alert("Không thể kết nối tới server Backend Python!");
            }
        } else {
            // --- MODE 2: FROM INPUT (STRONG PASSWORD ENHANCER) ---
            const targetLength = parseInt(aiLengthSlider ? aiLengthSlider.value : 8) || 8;
            
            // CHỈ LẤY Ô INPUT Ở KHU VỰC DƯỚI (Không lấy 'pwdInput' của Checker ở trên)
            const baseWordInput = document.getElementById('gen-base-word');
            const baseWordValue = baseWordInput ? baseWordInput.value.trim() : "";

            const requestData = {
                input_password: baseWordValue, 
                uppercase: document.getElementById('ai-inc-upper')?.checked ?? true, 
                number: document.getElementById('ai-inc-num')?.checked ?? true,
                special_character: document.getElementById('ai-inc-sym')?.checked ?? true,
                length: targetLength,
                avoid_ambiguous: document.getElementById('ai-inc-ambig')?.checked ?? false 
            };

            if (genResult) genResult.value = "AI is thinking..."; 

            try {
                const response = await fetch("http://127.0.0.1:8000/enhance", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(errorData.detail || "Đã xảy ra lỗi khi tối ưu mật khẩu!");
                    if (genResult) genResult.value = "";
                    return;
                }

                const result = await response.json();
                if (genResult) genResult.value = result.password; 

            } catch (error) {
                console.error("Lỗi kết nối Enhancer:", error);
                alert("Không thể kết nối tới server xử lý nâng cấp mật khẩu!");
                if (genResult) genResult.value = "Error";
            }
        }
    });
}

// =====================================================================
// 4. THEME SWITCHER LOGIC
// =====================================================================
const themeSelect = document.getElementById('themeSelect');

if (themeSelect) {
    // Load saved theme
    const savedTheme = localStorage.getItem('trustmii_theme') || 'dark';
    themeSelect.value = savedTheme;
    applyTheme(savedTheme);

    themeSelect.addEventListener('change', (e) => {
        const theme = e.target.value;
        applyTheme(theme);
        localStorage.setItem('trustmii_theme', theme);
    });
}

function applyTheme(theme) {
    // Remove all existing theme classes
    document.body.classList.remove('theme-light', 'theme-lofi', 'theme-chill', 'theme-eco');
    
    // Add the new theme class if it's not the default 'dark'
    if (theme !== 'dark') {
        document.body.classList.add(`theme-${theme}`);
    }
}
