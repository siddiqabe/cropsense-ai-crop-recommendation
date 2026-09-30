// ════════════════════════════════════════
//  CROPSENSE — Shared Data & State
// ════════════════════════════════════════

// ============================================
// MULTI-LANGUAGE SUPPORT
// ============================================

let currentLanguage = localStorage.getItem('cropsense_lang') || 'en';
let translations = {};

const languageList = {
    'en': { name: 'English', flag: '🇬🇧', native: 'English' },
    'hi': { name: 'Hindi', flag: '🇮🇳', native: 'हिंदी' },
    'mr': { name: 'Marathi', flag: '🇮🇳', native: 'मराठी' },
    'kn': { name: 'Kannada', flag: '🇮🇳', native: 'ಕನ್ನಡ' },
    'ta': { name: 'Tamil', flag: '🇮🇳', native: 'தமிழ்' },
    'te': { name: 'Telugu', flag: '🇮🇳', native: 'తెలుగు' }
};

async function loadLanguage(lang) {
    const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

    try {
        // English is always direct from en.json
        if (lang === 'en') {
            const resp = await fetch('/languages/en.json');
            translations = await resp.json();
            currentLanguage = lang;
            localStorage.setItem('cropsense_lang', lang);
            translatePage();
            updateLanguageButton();
            return;
        }

        // Check localStorage cache
        const cacheKey = 'cropsense_translations_' + lang;
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            try {
                const parsed = JSON.parse(cached);
                if (parsed && typeof parsed.data === 'object' && Date.now() - parsed.timestamp < CACHE_DURATION) {
                    translations = parsed.data;
                    currentLanguage = lang;
                    localStorage.setItem('cropsense_lang', lang);
                    translatePage();
                    updateLanguageButton();
                    console.log('✅ Loaded', languageList[lang].name, 'from cache');
                    return;
                }
            } catch (e) {
                localStorage.removeItem(cacheKey);
            }
        }

        // Load static JSON file directly (instant — no slow API calls)
        const fallbackResp = await fetch('/languages/' + lang + '.json');
        if (fallbackResp.ok) {
            translations = await fallbackResp.json();
            // Cache for next load
            localStorage.setItem(cacheKey, JSON.stringify({
                timestamp: Date.now(),
                data: translations
            }));
        } else {
            // If static file missing, try API with fast timeout
            const enResp = await fetch('/languages/en.json');
            const enData = await enResp.json();
            const keys = Object.keys(enData);
            const texts = keys.map(k => enData[k]);

            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 5000);

            try {
                const translateResp = await fetch('/api/translate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ texts, to: lang }),
                    signal: controller.signal
                });
                clearTimeout(timeout);

                if (translateResp.ok) {
                    const result = await translateResp.json();
                    const translated = {};
                    keys.forEach((key, i) => { translated[key] = result.translations[i]; });
                    translations = translated;

                    localStorage.setItem(cacheKey, JSON.stringify({
                        timestamp: Date.now(),
                        data: translated
                    }));
                } else {
                    throw new Error('API failed');
                }
            } catch {
                clearTimeout(timeout);
                throw new Error('Translation unavailable');
            }
        }

        currentLanguage = lang;
        localStorage.setItem('cropsense_lang', lang);
        translatePage();
        updateLanguageButton();
        console.log('✅ Language changed to:', languageList[lang].name);

    } catch (error) {
        console.error('Failed to load language:', error);
        if (lang !== 'en') {
            await loadLanguage('en');
        }
    }
}

function translatePage() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                if (el.placeholder !== undefined) el.placeholder = translations[key];
            } else if (el.tagName === 'BUTTON') {
                const iconMatch = el.textContent.trim().match(/^(\p{Emoji})/u);
                if (iconMatch) {
                    el.innerHTML = iconMatch[1] + ' ' + translations[key];
                } else {
                    el.innerHTML = translations[key];
                }
            } else {
                el.innerHTML = translations[key];
            }
        }
    });
    
    if (translations['app_name']) {
        document.title = translations['app_name'];
    }
}

function updateLanguageButton() {
    const btn = document.querySelector('.lang-btn');
    if (btn) {
        btn.innerHTML = `${languageList[currentLanguage].flag} ${languageList[currentLanguage].native} ▼`;
    }
}

window.toggleLanguageDropdown = function() {
    const dropdown = document.getElementById('langDropdown');
    if (dropdown) dropdown.classList.toggle('show');
};

window.changeLanguage = async function(lang) {
    await loadLanguage(lang);
    const dropdown = document.getElementById('langDropdown');
    if (dropdown) dropdown.classList.remove('show');
    if (window.updateChatbotLanguage) {
        window.updateChatbotLanguage();
    }
};

document.addEventListener('click', function(e) {
    const dropdown = document.getElementById('langDropdown');
    const btn = document.querySelector('.lang-btn');
    if (dropdown && btn && !btn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    loadLanguage(currentLanguage);
});

// ============================================
// API BASE URL CONFIGURATION
// ============================================

const API_BASE = '';

// ============================================
// CROP DATABASE
// ============================================

const CROPS = {
  'rice': {min_temp:21, max_temp:37, min_rain:100, max_rain:300, soil:'alluvial', season:'Kharif', npk:{N:100,P:50,K:50}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:4024, icon:'🌾'},
  'wheat': {min_temp:16, max_temp:25, min_rain:50, max_rain:150, soil:'Loamy', season:'Rabi', npk:{N:120,P:60,K:40}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:2164, icon:'🌿'},
  'maize': {min_temp:18, max_temp:23, min_rain:50, max_rain:120, soil:'Sandy', season:'Kharif', npk:{N:120,P:60,K:40}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:1700, icon:'🌽'},
  'potato': {min_temp:20, max_temp:25, min_rain:50, max_rain:120, soil:'Loamy', season:'Rabi', npk:{N:120,P:80,K:75}, fert:'Urea 120kg/ha, DAP 80kg/ha', price:1240, icon:'🥔'},
  'tomato': {min_temp:18, max_temp:27, min_rain:50, max_rain:100, soil:'Loamy', season:'Zaid', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 80kg/ha', price:1848, icon:'🍅'},
  'onion': {min_temp:18, max_temp:24, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:100,P:50,K:80}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:1728, icon:'🧅'},
  'cotton': {min_temp:18, max_temp:29, min_rain:50, max_rain:100, soil:'Black cotton', season:'Kharif', npk:{N:100,P:50,K:50}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:7767, icon:'🌸'},
  'sugarcane': {min_temp:22, max_temp:32, min_rain:150, max_rain:250, soil:'Loamy', season:'Zaid', npk:{N:250,P:100,K:80}, fert:'Urea 250kg/ha, DAP 100kg/ha', price:205, icon:'🎋'},
  'tea': {min_temp:13, max_temp:32, min_rain:150, max_rain:300, soil:'Sandy', season:'Zaid', npk:{N:60,P:30,K:30}, fert:'Urea 60kg/ha, DAP 30kg/ha', price:27000, icon:'🍵'},
  'coffee': {min_temp:23, max_temp:28, min_rain:150, max_rain:250, soil:'Volcanic', season:'Zaid', npk:{N:80,P:40,K:40}, fert:'Urea 80kg/ha, DAP 40kg/ha', price:20200, icon:'☕'},
  'groundnut': {min_temp:25, max_temp:35, min_rain:50, max_rain:100, soil:'Sandy', season:'Kharif', npk:{N:20,P:60,K:40}, fert:'Urea 20kg/ha, DAP 60kg/ha', price:6619, icon:'🥜'},
  'soybean': {min_temp:20, max_temp:30, min_rain:50, max_rain:100, soil:'Loamy', season:'Kharif', npk:{N:30,P:60,K:20}, fert:'Urea 30kg/ha, DAP 60kg/ha', price:5423, icon:'🫘'},
  'pulse': {min_temp:21, max_temp:30, min_rain:40, max_rain:80, soil:'Clay', season:'Rabi', npk:{N:25,P:50,K:20}, fert:'Urea 25kg/ha, DAP 50kg/ha', price:6000, icon:'🫛'},
  'millets': {min_temp:25, max_temp:35, min_rain:30, max_rain:70, soil:'Loamy', season:'Kharif', npk:{N:40,P:40,K:20}, fert:'Urea 40kg/ha, DAP 40kg/ha', price:3100, icon:'🌾'},
  'jute': {min_temp:24, max_temp:37, min_rain:100, max_rain:200, soil:'Loamy', season:'Kharif', npk:{N:60,P:30,K:30}, fert:'Urea 60kg/ha, DAP 30kg/ha', price:11300, icon:'🌿'},
  'mustard': {min_temp:10, max_temp:25, min_rain:40, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:20}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:6076, icon:'🌼'},
  'banana': {min_temp:10, max_temp:40, min_rain:90, max_rain:120, soil:'Acidic', season:'Zaid', npk:{N:100,P:90,K:50}, fert:'Urea 200kg/ha, DAP 100kg/ha', price:3639, icon:'🍌'},
  'turmeric': {min_temp:20, max_temp:35, min_rain:150, max_rain:250, soil:'Loamy', season:'Kharif', npk:{N:80,P:50,K:60}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:10424, icon:'🟡'},
  'sunflower': {min_temp:24, max_temp:35, min_rain:50, max_rain:100, soil:'Clay', season:'Rabi', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:7500, icon:'🌻'},
  'sesame': {min_temp:25, max_temp:30, min_rain:50, max_rain:80, soil:'Sandy loam', season:'Kharif', npk:{N:40,P:40,K:50}, fert:'Urea 40kg/ha, DAP 40kg/ha', price:9316, icon:'🌱'},
  'apple': {min_temp:15, max_temp:25, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:30,P:140,K:100}, fert:'Urea 120kg/ha, DAP 80kg/ha', price:12871, icon:'🍎'},
  'papaya': {min_temp:23, max_temp:43, min_rain:40, max_rain:250, soil:'Loamy', season:'Zaid', npk:{N:50,P:60,K:50}, fert:'Urea 150kg/ha, DAP 80kg/ha', price:3087, icon:'🍈'},
  'guava': {min_temp:18, max_temp:32, min_rain:100, max_rain:150, soil:'Sandy', season:'Zaid', npk:{N:100,P:50,K:70}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:5290, icon:'🍐'},
  'watermelon': {min_temp:21, max_temp:29, min_rain:40, max_rain:60, soil:'Loamy', season:'Zaid', npk:{N:100,P:20,K:50}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:1526, icon:'🍉'},
  'cucumber': {min_temp:21, max_temp:28, min_rain:50, max_rain:100, soil:'Loamy', season:'Zaid', npk:{N:100,P:50,K:60}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:2250, icon:'🥒'},
  'pumpkin': {min_temp:18, max_temp:29, min_rain:80, max_rain:120, soil:'Loamy', season:'Kharif', npk:{N:100,P:60,K:80}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:1580, icon:'🎃'},
  'brinjal': {min_temp:21, max_temp:27, min_rain:60, max_rain:100, soil:'Sandy', season:'Zaid', npk:{N:100,P:60,K:80}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:2660, icon:'🍆'},
  'cabbage': {min_temp:15, max_temp:21, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:1631, icon:'🥬'},
  'cauliflower': {min_temp:15, max_temp:21, min_rain:50, max_rain:100, soil:'Sandy', season:'Rabi', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:2572, icon:'🥦'},
  'spinach': {min_temp:10, max_temp:21, min_rain:40, max_rain:80, soil:'Loamy', season:'Rabi', npk:{N:80,P:50,K:60}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:1280, icon:'🌿'},
  'carrot': {min_temp:14, max_temp:26, min_rain:50, max_rain:100, soil:'Sandy', season:'Rabi', npk:{N:100,P:60,K:70}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:3294, icon:'🥕'},
  'beetroot': {min_temp:12, max_temp:23, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:100,P:60,K:70}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:3584, icon:'🟣'},
  'radish': {min_temp:18, max_temp:24, min_rain:40, max_rain:80, soil:'Sandy', season:'Rabi', npk:{N:100,P:50,K:60}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:2321, icon:'⚪'},
  'peas': {min_temp:10, max_temp:18, min_rain:40, max_rain:80, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:5168, icon:'🟢'},
  'lentil': {min_temp:15, max_temp:21, min_rain:35, max_rain:55, soil:'Loamy', season:'Rabi', npk:{N:40,P:30,K:20}, fert:'Urea 40kg/ha, DAP 30kg/ha', price:6505, icon:'🫘'},
  'blackgram': {min_temp:25, max_temp:35, min_rain:60, max_rain:75, soil:'Sandy loam', season:'Kharif', npk:{N:30,P:20,K:20}, fert:'Urea 30kg/ha, DAP 20kg/ha', price:7132, icon:'⚫'},
  'greengram': {min_temp:25, max_temp:35, min_rain:60, max_rain:75, soil:'Sandy loam', season:'Kharif', npk:{N:25,P:20,K:20}, fert:'Urea 25kg/ha, DAP 20kg/ha', price:2828, icon:'🟢'},
  'ragi': {min_temp:20, max_temp:35, min_rain:50, max_rain:100, soil:'Red', season:'Kharif', npk:{N:40,P:40,K:20}, fert:'Urea 40kg/ha, DAP 40kg/ha', price:3934, icon:'🌾'},
  'coriander': {min_temp:10, max_temp:25, min_rain:40, max_rain:80, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:30}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:9569, icon:'🌿'},
  'cumin': {min_temp:15, max_temp:25, min_rain:40, max_rain:80, soil:'Sandy Loam', season:'Rabi', npk:{N:60,P:40,K:30}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:7639, icon:'🌱'},
  'strawberry': {min_temp:15, max_temp:26, min_rain:50, max_rain:100, soil:'Acidic', season:'Rabi', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:19000, icon:'🍓'},
  'custardapple': {min_temp:25, max_temp:35, min_rain:100, max_rain:150, soil:'Loamy', season:'Zaid', npk:{N:100,P:50,K:60}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:5200, icon:'🍏'},
  'lemon': {min_temp:20, max_temp:38, min_rain:80, max_rain:120, soil:'Loamy', season:'Zaid', npk:{N:80,P:50,K:60}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:12845, icon:'🍋'},
  'bottlegourd': {min_temp:21, max_temp:35, min_rain:80, max_rain:120, soil:'Loamy', season:'Zaid', npk:{N:100,P:60,K:60}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:1722, icon:'🎃'},
  'bittergourd': {min_temp:25, max_temp:35, min_rain:80, max_rain:120, soil:'Sandy', season:'Zaid', npk:{N:100,P:60,K:60}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:3802, icon:'🥒'},
  'ridgegourd': {min_temp:24, max_temp:35, min_rain:80, max_rain:120, soil:'Clay', season:'Zaid', npk:{N:100,P:60,K:60}, fert:'Urea 100kg/ha, DAP 60kg/ha', price:3000, icon:'🥒'},
  'okra': {min_temp:24, max_temp:32, min_rain:60, max_rain:100, soil:'Loamy', season:'Kharif', npk:{N:120,P:60,K:60}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:2500, icon:'🌿'},
  'fenugreek': {min_temp:10, max_temp:30, min_rain:40, max_rain:80, soil:'Sandy', season:'Rabi', npk:{N:60,P:40,K:30}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:5638, icon:'🌿'},
  'mint': {min_temp:18, max_temp:21, min_rain:60, max_rain:100, soil:'Loamy', season:'Zaid', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:2000, icon:'🌿'},
  'aloe_vera': {min_temp:13, max_temp:29, min_rain:30, max_rain:70, soil:'Sandy', season:'Zaid', npk:{N:40,P:30,K:40}, fert:'Urea 40kg/ha, DAP 30kg/ha', price:1000, icon:'🌵'},
  'rubber': {min_temp:25, max_temp:34, min_rain:200, max_rain:300, soil:'Loamy', season:'Zaid', npk:{N:80,P:40,K:60}, fert:'Urea 80kg/ha, DAP 40kg/ha', price:20700, icon:'🌳'},
  'avocado': {min_temp:15, max_temp:29, min_rain:100, max_rain:150, soil:'Sandy', season:'Zaid', npk:{N:100,P:50,K:80}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:17500, icon:'🥑'},
  'cherry': {min_temp:20, max_temp:25, min_rain:60, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:75000, icon:'🍒'},
  'jackfruit': {min_temp:25, max_temp:35, min_rain:150, max_rain:250, soil:'Loamy', season:'Zaid', npk:{N:100,P:50,K:70}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:3052, icon:'🍈'},
  'pear': {min_temp:18, max_temp:23, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:10603, icon:'🍐'},
  'apricot': {min_temp:20, max_temp:25, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:10000, icon:'🍑'},
  'oatpea': {min_temp:7, max_temp:24, min_rain:40, max_rain:80, soil:'Loamy', season:'Rabi', npk:{N:80,P:40,K:30}, fert:'Urea 80kg/ha, DAP 40kg/ha', price:3000, icon:'🌾'},
  'pigeonpea': {min_temp:29, max_temp:36, min_rain:60, max_rain:100, soil:'Sandy loam', season:'Kharif', npk:{N:30,P:20,K:20}, fert:'Urea 30kg/ha, DAP 20kg/ha', price:3198, icon:'🫘'},
  'horsegram': {min_temp:25, max_temp:30, min_rain:50, max_rain:80, soil:'Sandy loam', season:'Kharif', npk:{N:30,P:20,K:20}, fert:'Urea 30kg/ha, DAP 20kg/ha', price:3702, icon:'🫘'},
  'chickoo': {min_temp:10, max_temp:38, min_rain:80, max_rain:120, soil:'Loamy', season:'Zaid', npk:{N:80,P:50,K:60}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:3000, icon:'🟤'},
  'grapes': {min_temp:25, max_temp:32, min_rain:65, max_rain:90, soil:'Loamy', season:'Zaid', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:8942, icon:'🍇'},
  'litchi': {min_temp:25, max_temp:35, min_rain:100, max_rain:150, soil:'Loamy', season:'Zaid', npk:{N:80,P:50,K:60}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:17500, icon:'🍒'},
  'muskmelon': {min_temp:20, max_temp:25, min_rain:20, max_rain:30, soil:'Sandy', season:'Zaid', npk:{N:80,P:50,K:50}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:2500, icon:'🍈'},
  'capsicum': {min_temp:18, max_temp:25, min_rain:50, max_rain:80, soil:'Loamy', season:'Zaid', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:3189, icon:'🫑'},
  'cardamom': {min_temp:20, max_temp:35, min_rain:150, max_rain:250, soil:'Loamy', season:'Zaid', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:217800, icon:'🟢'},
  'fennel': {min_temp:15, max_temp:25, min_rain:50, max_rain:80, soil:'Loamy', season:'Rabi', npk:{N:60,P:40,K:30}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:7810, icon:'🌿'},
  'clove': {min_temp:20, max_temp:30, min_rain:150, max_rain:250, soil:'Loamy', season:'Zaid', npk:{N:50,P:40,K:50}, fert:'Urea 50kg/ha, DAP 40kg/ha', price:85500, icon:'🟤'},
  'saffron': {min_temp:23, max_temp:27, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:40,P:30,K:30}, fert:'Urea 40kg/ha, DAP 30kg/ha', price:200000, icon:'🟣'},
  'tamarind': {min_temp:20, max_temp:35, min_rain:80, max_rain:120, soil:'Loamy', season:'Zaid', npk:{N:60,P:40,K:50}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:7690, icon:'🟤'},
  'fig': {min_temp:18, max_temp:27, min_rain:50, max_rain:100, soil:'Loamy', season:'Zaid', npk:{N:80,P:60,K:70}, fert:'Urea 80kg/ha, DAP 60kg/ha', price:14000, icon:'🪴'},
  'flaxseed': {min_temp:13, max_temp:20, min_rain:40, max_rain:80, soil:'Sandy', season:'Rabi', npk:{N:60,P:40,K:30}, fert:'Urea 60kg/ha, DAP 40kg/ha', price:5540, icon:'🌾'},
  'sweetpotato': {min_temp:21, max_temp:26, min_rain:75, max_rain:150, soil:'Loamy', season:'Kharif', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:3071, icon:'🍠'},
  'yam': {min_temp:20, max_temp:30, min_rain:100, max_rain:150, soil:'Loamy', season:'Kharif', npk:{N:100,P:50,K:70}, fert:'Urea 100kg/ha, DAP 50kg/ha', price:3000, icon:'🌽'},
  'broccoli': {min_temp:15, max_temp:21, min_rain:50, max_rain:100, soil:'Loamy', season:'Rabi', npk:{N:120,P:60,K:80}, fert:'Urea 120kg/ha, DAP 60kg/ha', price:750, icon:'🥦'},
  'rosemary': {min_temp:15, max_temp:21, min_rain:40, max_rain:80, soil:'Well drained', season:'Zaid', npk:{N:50,P:30,K:40}, fert:'Urea 50kg/ha, DAP 30kg/ha', price:8000, icon:'🌿'},
  'cocoa': {min_temp:19, max_temp:39, min_rain:150, max_rain:250, soil:'Loamy', season:'Zaid', npk:{N:80,P:50,K:70}, fert:'Urea 80kg/ha, DAP 50kg/ha', price:12000, icon:'🟤'},
  'beans': {min_temp:21, max_temp:29, min_rain:60, max_rain:100, soil:'Sandy loam', season:'Kharif', npk:{N:25,P:60,K:40}, fert:'Urea 25kg/ha, DAP 60kg/ha', price:6951, icon:'🫘'},
  'coconut': {min_temp:20, max_temp:32, min_rain:130, max_rain:230, soil:'Sandy', season:'Zaid', npk:{N:200,P:100,K:150}, fert:'Urea 200kg/ha, DAP 100kg/ha', price:6135, icon:'🥥'}
};

// ============================================
// SOIL INFO
// ============================================

const SOIL_INFO = {
  'Clay': {N:'High', P:'Medium', K:'High', desc:'Rich in nutrients, excellent water retention. Ideal for rice.'},
  'Loamy': {N:'Medium', P:'High', K:'Medium', desc:'Best soil for most crops. Balanced drainage and water retention.'},
  'Sandy': {N:'Low', P:'Low', K:'Low', desc:'Drains quickly, needs frequent watering. Great for groundnut, watermelon.'},
  'Sandy loam': {N:'Low', P:'Medium', K:'Low', desc:'Well-draining with some organic matter. Good for pulses.'},
  'Black cotton': {N:'Medium', P:'High', K:'Medium', desc:'Excellent water retention. Perfect for cotton cultivation.'},
  'Acidic': {N:'Low', P:'Medium', K:'Low', desc:'Acidic soil. Needs lime treatment. Best for tea, coffee, strawberry.'},
  'Red': {N:'Low', P:'Low', K:'Medium', desc:'Iron-rich, well-draining. Good for ragi and millets.'},
  'Volcanic': {N:'High', P:'High', K:'High', desc:'Very fertile volcanic soil. Excellent for avocado.'},
  'Well drained': {N:'Medium', P:'Medium', K:'Medium', desc:'Well-draining soil. Good for herbs like rosemary.'},
};

// ============================================
// SEASON INFO
// ============================================

const SEASON_INFO = {
  kharif:{label:'Kharif (June–October)', info:'Sown at start of monsoon. Major crops: Rice, Maize, Cotton, Groundnut, Millets, Jute.'},
  rabi:  {label:'Rabi (November–April)', info:'Winter crops sown after monsoon. Major crops: Wheat, Barley, Mustard, Pulses, Potato.'},
  zaid:  {label:'Zaid (April–June)',     info:'Off-season summer crops. Major crops: Sugarcane, Tea, Coffee.'},
};

// ============================================
// SESSION MANAGEMENT (UPDATED WITH user_id)
// ============================================

const SS = {
  get user()    { return sessionStorage.getItem('cs_user'); },
  set user(v)   { v ? sessionStorage.setItem('cs_user',v) : sessionStorage.removeItem('cs_user'); },
  get user_id() { return sessionStorage.getItem('cs_user_id'); },
  set user_id(v){ v ? sessionStorage.setItem('cs_user_id',v) : sessionStorage.removeItem('cs_user_id'); },
  get history() { try{ return JSON.parse(sessionStorage.getItem('cs_hist')||'[]'); }catch{ return []; } },
  set history(v){ sessionStorage.setItem('cs_hist', JSON.stringify(v)); },
  get users()   { try{ return JSON.parse(sessionStorage.getItem('cs_users')||'{}'); }catch{ return {}; } },
  set users(v)  { sessionStorage.setItem('cs_users', JSON.stringify(v)); },
  addHistory(entry) {
    const h = this.history;
    h.unshift(entry);
    if(h.length > 10) h.pop();
    this.history = h;
    const users = this.users;
    if(this.user && users[this.user]) { users[this.user].history = h; this.users = users; }
  },
  logout() {
    const users = this.users;
    if(this.user && users[this.user]) { users[this.user].history = this.history; this.users = users; }
    sessionStorage.removeItem('cs_user');
    sessionStorage.removeItem('cs_user_id');
    sessionStorage.removeItem('cs_hist');
  }
};

/// ============================================
// AUTHENTICATION
// ============================================

function requireAuth() {
  if (!SS.user) { window.location.href = 'auth.html'; return false; }
  return true;
}

// LOGIN FUNCTION
window.handleLogin = async function(username, password) {
    try {
        const response = await fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            SS.user = username;
            SS.user_id = data.user_id;
            window.location.href = '/dashboard.html';
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Cannot connect to server. Please make sure Flask is running on port 5000');
    }
};

// REGISTER FUNCTION
window.handleRegister = async function(fullName, username, email, password) {
    try {
        const response = await fetch(`${API_BASE}/api/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                full_name: fullName || '',
                username: username, 
                email: email,
                password: password 
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Registration successful! Please login.');
            window.location.href = '/auth.html?mode=login';
        } else {
            alert('❌ ' + (data.error || 'Registration failed'));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Cannot connect to server. Please make sure Flask is running on port 5000');
    }
};

// ============================================
// NAVIGATION BUILDERS (ADD THIS SECTION)
// ============================================

// For NON-LOGGED IN users (Shows language + Sign In + Get Started)
window.buildAuthNav = function() {
    return `
        <div class="lang-switcher">
            <button class="lang-btn" onclick="toggleLanguageDropdown()">
                ${languageList[currentLanguage].flag} ${languageList[currentLanguage].native} ▼
            </button>
            <div class="lang-dropdown" id="langDropdown">
                ${Object.entries(languageList).map(([code, data]) => `
                    <a href="#" onclick="changeLanguage('${code}'); return false;">
                        ${data.flag} ${data.native} (${data.name})
                    </a>
                `).join('')}
            </div>
        </div>
        <a class="btn-nav btn-nav-ghost" href="auth.html?mode=login" data-i18n="nav_signin">Sign In</a>
        <a class="btn-nav btn-nav-solid" href="auth.html?mode=register" data-i18n="nav_get_started">Get Started</a>
    `;
};

// For LOGGED IN users (Shows language + Avatar + Username + Sign Out)
window.buildUserNav = function() {
    const u = SS.user || '';
    return `
        <div class="lang-switcher">
            <button class="lang-btn" onclick="toggleLanguageDropdown()">
                ${languageList[currentLanguage].flag} ${languageList[currentLanguage].native} ▼
            </button>
            <div class="lang-dropdown" id="langDropdown">
                ${Object.entries(languageList).map(([code, data]) => `
                    <a href="#" onclick="changeLanguage('${code}'); return false;">
                        ${data.flag} ${data.native} (${data.name})
                    </a>
                `).join('')}
            </div>
        </div>
        <div class="nav-user">
            <div class="nav-avatar">${u[0]?.toUpperCase()||'F'}</div>
            <span style="color:rgba(255,255,255,.65);font-size:13px;">${u}</span>
        </div>
        <button class="btn-nav btn-nav-logout" onclick="doLogout()" data-i18n="nav_signout">Sign Out</button>
    `;
};

function doLogout() {
  SS.logout();
  window.location.href = 'index.html';
}

// ============================================
// FOOTER
// ============================================

function footerHTML() {
  return `<footer>
    <div class="footer-inner">
      <div class="footer-top">
        <div>
          <div class="footer-brand">Crop<span>Sense</span></div>
          <div class="footer-desc" data-i18n="footer_desc">India's trusted crop recommendation platform. Free, data-driven, built for every farmer.</div>
        </div>
        <div class="footer-col"><h4 data-i18n="platform">Platform</h4><ul>
          <li><a href="index.html" data-i18n="nav_home">Home</a></li>
          <li><a href="auth.html?mode=register" data-i18n="nav_get_started">Get Started</a></li>
          <li><a href="auth.html?mode=login" data-i18n="nav_signin">Sign In</a></li>
          <li><a href="how-it-works.html" data-i18n="nav_how_it_works">How It Works</a></li>
          <li><a href="testimonials.html" data-i18n="nav_testimonials">Testimonials</a></li>
          <li><a href="contact.html" data-i18n="nav_contact">Contact</a></li>
        </ul></div>
        <div class="footer-col"><h4 data-i18n="resources">Resources</h4><ul>
          <li><a href="dashboard.html" data-i18n="crop_recommender">Crop Recommender</a></li>
          <li><a href="history.html" data-i18n="history">History</a></li>
          <li><a data-i18n="fertilizer_guide">Fertilizer Guide</a></li>
          <li><a data-i18n="season_calendar">Season Calendar</a></li>
        </ul></div>
        <div class="footer-col"><h4 data-i18n="support">Support</h4><ul>
          <li><a data-i18n="help_center">Help Center</a></li><li><a data-i18n="faq">FAQ</a></li>
          <li><a data-i18n="privacy_policy">Privacy Policy</a></li><li><a data-i18n="terms">Terms</a></li>
        </ul></div>
      </div>
      <div class="footer-bottom">
        <div class="footer-copy" data-i18n="footer_copyright">© 2024 CropSense. All rights reserved. Made with ❤️ for Indian farmers.</div>
        <div class="footer-social">
          <div class="social-btn">𝕏</div><div class="social-btn">f</div>
          <div class="social-btn">in</div><div class="social-btn">▶</div>
        </div>
      </div>
    </div>
  </footer>`;
}

// ============================================
// ML PREDICTIONS - UPDATED WITH USER_ID
// ============================================

async function getMLRecommendations() {
    const btn = document.getElementById('rec-btn');
    if (!btn) return;
    btn.classList.add('loading');
    
    const soilType = document.getElementById('soil-select')?.value || 'Loamy';
    const userId = SS.user_id;
    
    const inputData = {
        N: parseFloat(document.getElementById('nitrogen')?.value) || 50,
        P: parseFloat(document.getElementById('phosphorus')?.value) || 50,
        K: parseFloat(document.getElementById('potassium')?.value) || 50,
        ph: parseFloat(document.getElementById('ph')?.value) || 7.0,
        temperature: parseFloat(document.getElementById('temp-num')?.value) || 25,
        humidity: parseFloat(document.getElementById('humidity')?.value) || 70,
        rainfall: parseFloat(document.getElementById('rain-num')?.value) || 100,
        soil_type: soilType,
        user_id: userId
    };
    
    // Validation
    if (inputData.N < 20 || inputData.N > 200) {
        alert('❌ Nitrogen must be between 20-200 mg/kg');
        btn.classList.remove('loading');
        return;
    }
    if (inputData.P < 0 || inputData.P > 80) {
        alert('❌ Phosphorus must be between 0-80 mg/kg');
        btn.classList.remove('loading');
        return;
    }
    if (inputData.K < 0 || inputData.K > 200) {
        alert('❌ Potassium must be between 0-200 mg/kg');
        btn.classList.remove('loading');
        return;
    }
    if (inputData.ph < 3.0 || inputData.ph > 8.5) {
        alert('❌ pH must be between 3.0-8.5');
        btn.classList.remove('loading');
        return;
    }

    console.log("📤 Sending data:", inputData);

    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(inputData)
        });

        const result = await response.json();
        console.log("📥 Received result:", result);

        if (result.success) {
            renderResults(result.recommendations, inputData);
            
            SS.addHistory({ 
                id: Date.now(),
                date: new Date().toLocaleString('en-IN', {
                    day:'numeric', month:'short', year:'numeric',
                    hour:'2-digit', minute:'2-digit'
                }),
                soil: soilType,
                temp: inputData.temperature,
                rain: inputData.rainfall,
                N: inputData.N,
                P: inputData.P,
                K: inputData.K,
                ph: inputData.ph,
                crops: result.recommendations.map(r => r.name)
            });
        } else {
            alert('Error: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('❌ Error:', error);
        alert('Failed to connect to ML server. Make sure Flask is running on port 5000');
    } finally {
        btn.classList.remove('loading');
    }
}

// ============================================
// SIMPLIFIED RESULTS RENDERER
// ============================================

function renderResults(recommendations, inputData) {
    const rankClass = ['r1', 'r2', 'r3'];
    
    const cardsHtml = recommendations.map((r, i) => `
        <div class="rec-card ${rankClass[i]||''}" style="animation-delay:${i*.1}s">
            <div class="rec-badge">${i+1}</div>
            <div>
                <div class="rec-crop-name">${r.icon} ${r.name}</div>
                <div class="rec-tags">
                    <span class="rec-tag">📅 ${r.season}</span>
                    <span class="rec-tag">🌡 ${r.min_temp}–${r.max_temp}°C</span>
                    <span class="rec-tag">🌧 ${r.min_rain}–${r.max_rain}mm</span>
                    <span class="rec-tag">📊 ${r.confidence}% match</span>
                </div>
                <div class="rec-fert">💊 ${r.fert}</div>
            </div>
            <div class="rec-right">
                <div class="rec-price">₹${r.price.toLocaleString('en-IN')}</div>
                <div class="rec-price-label">per quintal</div>
            </div>
        </div>
    `).join('');

    const dashRight = document.getElementById('dash-right');
    if (dashRight) {
        dashRight.innerHTML = `
            <div style="font-family:'Playfair Display',serif;font-size:22px;color:var(--forest);margin-bottom:16px;">
                🏆 Top ${recommendations.length} Recommendations
            </div>
            <div class="soil-banner" style="background:linear-gradient(135deg,var(--forest),var(--moss))">
                <div>
                    <h3 style="color:white;margin-bottom:8px;">📊 Your Soil Analysis</h3>
                    <div style="display:flex;gap:15px;flex-wrap:wrap;">
                        <span style="color:var(--mint);">N: ${inputData.N}</span>
                        <span style="color:var(--mint);">P: ${inputData.P}</span>
                        <span style="color:var(--mint);">K: ${inputData.K}</span>
                        <span style="color:var(--mint);">pH: ${inputData.ph}</span>
                        <span style="color:var(--mint);">Humidity: ${inputData.humidity}%</span>
                        <span style="color:var(--mint);">Temp: ${inputData.temperature}°C</span>
                        <span style="color:var(--mint);">Rain: ${inputData.rainfall}mm</span>
                    </div>
                </div>
            </div>
            <div class="rec-list">${cardsHtml}</div>
        `;
    }
}