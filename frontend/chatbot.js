// ============================================
// COMPLETE CHATBOT.JS - FIXED VERSION
// For CropSense AI-Powered Crop Recommendation System
// ============================================

// ============================================
// CROP DATABASE (ALL 80+ CROPS FROM YOUR DATASET)
// ============================================

// Get current language from localStorage
let currentChatLanguage = localStorage.getItem('cropsense_lang') || 'en';
let chatbotTranslations = {};

// Load chatbot language data from JSON file
async function loadChatbotLanguage(lang) {
    try {
        const resp = await fetch(`/languages/chatbot/${lang}.json`);
        if (resp.ok) {
            chatbotTranslations = await resp.json();
        }
    } catch (e) {
        console.warn('Chatbot translations not available for:', lang);
    }
}

const CROP_DATABASE = {
    // CEREALS & GRAINS
    'rice': { name: 'Rice', icon: '🌾', season: 'Kharif', temp: { min: 21, max: 37, optimal: 29 }, rainfall: { min: 100, max: 300, optimal: 200 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 5.0, max: 7.0, optimal: 6.0 }, soil: ['Clay', 'Alluvial'], price: 4024, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '90-120', P: '40-60', K: '40-60' }, varieties: ['Basmati', 'Sona Masoori', 'IR64', 'Swarna', 'Pusa 1121'], diseases: ['Blast', 'Bacterial Leaf Blight', 'Brown Spot', 'Sheath Blight'], pests: ['Stem Borer', 'Leaf Folder', 'Brown Planthopper', 'Gall Midge'], growingPeriod: '110-150 days', seedRate: '20-25 kg/ha' },
    'wheat': { name: 'Wheat', icon: '🌿', season: 'Rabi', temp: { min: 16, max: 25, optimal: 21 }, rainfall: { min: 50, max: 150, optimal: 100 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 2164, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '80-120', P: '40-60', K: '30-50' }, varieties: ['HD 2967', 'PBW 343', 'WH 1105', 'Lok-1', 'GW 366'], diseases: ['Rust', 'Powdery Mildew', 'Loose Smut', 'Karnal Bunt'], pests: ['Aphids', 'Termites', 'Armyworm', 'Shoot Fly'], growingPeriod: '110-150 days', seedRate: '100-125 kg/ha' },
    'maize': { name: 'Maize', icon: '🌽', season: 'Kharif', temp: { min: 18, max: 23, optimal: 21 }, rainfall: { min: 50, max: 120, optimal: 85 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 5.5, max: 7.0, optimal: 6.5 }, soil: ['Loamy', 'Sandy'], price: 1700, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '90-150', P: '50-70', K: '40-60' }, varieties: ['Pioneer 30V92', 'NK 6240', 'Dekalb 9108', 'PMH 1', 'Vivek 9'], diseases: ['Turcicum Leaf Blight', 'Downy Mildew', 'Stalk Rot'], pests: ['Stem Borer', 'Fall Armyworm', 'Shoot Fly', 'Cutworm'], growingPeriod: '90-110 days', seedRate: '18-20 kg/ha' },
    'ragi': { name: 'Ragi (Finger Millet)', icon: '🌾', season: 'Kharif', temp: { min: 20, max: 35, optimal: 27 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 5.5, max: 7.5, optimal: 6.5 }, soil: ['Red', 'Loamy'], price: 3934, fertilizer: 'Urea 40kg/ha, DAP 40kg/ha', npk: { N: '40-60', P: '40-60', K: '20-40' }, varieties: ['GPU 28', 'MR 1', 'HR 911', 'GPU 45', 'VL 149', 'Indaf 5'], diseases: ['Blast', 'Downy Mildew', 'Smut', 'Foot Rot'], pests: ['Stem Borer', 'Aphids', 'Armyworm', 'Root Aphid'], growingPeriod: '110-120 days', seedRate: '8-10 kg/ha' },
    'millets': { name: 'Millets', icon: '🌾', season: 'Kharif', temp: { min: 25, max: 35, optimal: 30 }, rainfall: { min: 30, max: 70, optimal: 50 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 5.5, max: 7.5, optimal: 6.5 }, soil: ['Loamy', 'Sandy'], price: 3100, fertilizer: 'Urea 40kg/ha, DAP 40kg/ha', npk: { N: '40-60', P: '30-50', K: '20-40' }, varieties: ['GHB 558', 'HHB 67', 'ICTP 8203', 'Pusa Composite 443'], diseases: ['Downy Mildew', 'Ergot', 'Smut', 'Rust'], pests: ['Shoot Fly', 'Stem Borer', 'Blister Beetle', 'Earhead Bug'], growingPeriod: '80-90 days', seedRate: '4-5 kg/ha' },

    // VEGETABLES
    'potato': { name: 'Potato', icon: '🥔', season: 'Rabi', temp: { min: 20, max: 25, optimal: 22 }, rainfall: { min: 50, max: 120, optimal: 85 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 5.0, max: 6.5, optimal: 5.5 }, soil: ['Loamy'], price: 1240, fertilizer: 'Urea 120kg/ha, DAP 80kg/ha', npk: { N: '100-150', P: '60-80', K: '100-150' }, varieties: ['Kufri Jyoti', 'Kufri Chandramukhi', 'Kufri Bahar', 'Kufri Pukhraj'], diseases: ['Late Blight', 'Early Blight', 'Black Scurf', 'Common Scab'], pests: ['Aphids', 'Cutworms', 'White Grubs', 'Potato Tuber Moth'], growingPeriod: '90-100 days', seedRate: '20-25 quintals/ha' },
    'tomato': { name: 'Tomato', icon: '🍅', season: 'Zaid', temp: { min: 18, max: 27, optimal: 22 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 1848, fertilizer: 'Urea 120kg/ha, DAP 80kg/ha', npk: { N: '100-150', P: '60-80', K: '60-80' }, varieties: ['Arka Vikas', 'Arka Rakshak', 'Pusa Ruby', 'Pusa Early Dwarf'], diseases: ['Early Blight', 'Late Blight', 'Leaf Curl Virus', 'Bacterial Wilt'], pests: ['Fruit Borer', 'Leaf Miner', 'Whitefly', 'Aphids'], growingPeriod: '100-120 days', seedRate: '400-500 g/ha' },
    'onion': { name: 'Onion', icon: '🧅', season: 'Rabi', temp: { min: 18, max: 24, optimal: 21 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.5, optimal: 6.5 }, soil: ['Loamy'], price: 1728, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '80-120', P: '40-60', K: '60-80' }, varieties: ['NHRDF Red', 'Agrifound Dark Red', 'Arka Kalyan', 'Pusa Red'], diseases: ['Purple Blotch', 'Downy Mildew', 'Basal Rot'], pests: ['Thrips', 'Onion Fly', 'Cutworms'], growingPeriod: '120-150 days', seedRate: '8-10 kg/ha' },
    'brinjal': { name: 'Brinjal', icon: '🍆', season: 'Zaid', temp: { min: 21, max: 27, optimal: 24 }, rainfall: { min: 60, max: 100, optimal: 80 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 5.5, max: 7.0, optimal: 6.5 }, soil: ['Sandy', 'Loamy'], price: 2660, fertilizer: 'Urea 100kg/ha, DAP 60kg/ha', npk: { N: '80-120', P: '40-60', K: '60-80' }, varieties: ['Pusa Purple Long', 'Pusa Kranti', 'Arka Navneet', 'Arka Shirish'], diseases: ['Little Leaf', 'Phomopsis Blight', 'Bacterial Wilt', 'Cercospora Leaf Spot'], pests: ['Shoot and Fruit Borer', 'Jassids', 'Whitefly', 'Mite'], growingPeriod: '120-150 days', seedRate: '400-500 g/ha' },
    'cabbage': { name: 'Cabbage', icon: '🥬', season: 'Rabi', temp: { min: 15, max: 21, optimal: 18 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 1631, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '100-150', P: '40-60', K: '60-80' }, varieties: ['Golden Acre', 'Pusa Drumhead', 'Pusa Mukta', 'Pride of India'], diseases: ['Black Rot', 'Club Root', 'Downy Mildew'], pests: ['Diamondback Moth', 'Cabbage Butterfly', 'Aphids'], growingPeriod: '70-90 days', seedRate: '400-500 g/ha' },
    'cauliflower': { name: 'Cauliflower', icon: '🥦', season: 'Rabi', temp: { min: 15, max: 21, optimal: 18 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Sandy', 'Loamy'], price: 2572, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '100-150', P: '40-60', K: '60-80' }, varieties: ['Pusa Deepali', 'Pusa Himjyoti', 'Pusa Snowball-1', 'Pusa Shubhra'], diseases: ['Black Rot', 'Club Root', 'Downy Mildew', 'Stalk Rot'], pests: ['Diamondback Moth', 'Aphids', 'Tobacco Caterpillar'], growingPeriod: '70-100 days', seedRate: '400-500 g/ha' },
    'spinach': { name: 'Spinach', icon: '🌿', season: 'Rabi', temp: { min: 10, max: 21, optimal: 16 }, rainfall: { min: 40, max: 80, optimal: 60 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.5, optimal: 6.5 }, soil: ['Loamy'], price: 1280, fertilizer: 'Urea 80kg/ha, DAP 50kg/ha', npk: { N: '60-80', P: '40-50', K: '40-60' }, varieties: ['Pusa Jyoti', 'Pusa Harit', 'All Green', 'Virginia Savoy'], diseases: ['Damping Off', 'Leaf Spot', 'Downy Mildew', 'White Rust'], pests: ['Leaf Miner', 'Aphids', 'Cutworms'], growingPeriod: '25-30 days', seedRate: '30-40 kg/ha' },
    'carrot': { name: 'Carrot', icon: '🥕', season: 'Rabi', temp: { min: 14, max: 26, optimal: 18 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Sandy', 'Loamy'], price: 3294, fertilizer: 'Urea 100kg/ha, DAP 60kg/ha', npk: { N: '80-120', P: '40-60', K: '60-80' }, varieties: ['Pusa Kesar', 'Pusa Meghali', 'Pusa Rudhira', 'Nantes', 'Chantenay'], diseases: ['Leaf Blight', 'Powdery Mildew', 'Root Rot'], pests: ['Carrot Rust Fly', 'Aphids', 'Nematodes'], growingPeriod: '80-100 days', seedRate: '5-6 kg/ha' },
    'beetroot': { name: 'Beetroot', icon: '🟣', season: 'Rabi', temp: { min: 12, max: 23, optimal: 18 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.5, optimal: 6.5 }, soil: ['Loamy'], price: 3584, fertilizer: 'Urea 100kg/ha, DAP 60kg/ha', npk: { N: '80-120', P: '40-60', K: '60-80' }, varieties: ['Detroit Dark Red', 'Crimson Globe', 'Crosby Egyptian', 'Early Wonder'], diseases: ['Cercospora Leaf Spot', 'Downy Mildew', 'Root Rot'], pests: ['Leaf Miner', 'Aphids', 'Webworm'], growingPeriod: '60-80 days', seedRate: '8-10 kg/ha' },
    'radish': { name: 'Radish', icon: '⚪', season: 'Rabi', temp: { min: 18, max: 24, optimal: 21 }, rainfall: { min: 40, max: 80, optimal: 60 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Sandy', 'Loamy'], price: 2321, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '60-80', P: '40-60', K: '40-60' }, varieties: ['Pusa Chetki', 'Pusa Desi', 'Pusa Himani', 'Japanese White'], diseases: ['White Rust', 'Alternaria Leaf Spot', 'Root Rot'], pests: ['Mustard Sawfly', 'Aphids', 'Painted Bug'], growingPeriod: '40-50 days', seedRate: '10-12 kg/ha' },
    'peas': { name: 'Peas', icon: '🟢', season: 'Rabi', temp: { min: 10, max: 18, optimal: 14 }, rainfall: { min: 40, max: 80, optimal: 60 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.5, optimal: 6.5 }, soil: ['Loamy'], price: 5168, fertilizer: 'Urea 60kg/ha, DAP 40kg/ha', npk: { N: '40-60', P: '40-60', K: '30-50' }, varieties: ['Arkel', 'Bonneville', 'Azad P-1', 'Pusa Pragati', 'Pant Matar-2'], diseases: ['Powdery Mildew', 'Rust', 'Wilt', 'Ascochyta Blight'], pests: ['Pea Leaf Miner', 'Pod Borer', 'Aphids'], growingPeriod: '60-70 days', seedRate: '60-75 kg/ha' },
    'okra': { name: 'Okra', icon: '🌿', season: 'Kharif', temp: { min: 24, max: 32, optimal: 28 }, rainfall: { min: 60, max: 100, optimal: 80 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 2500, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '80-120', P: '40-60', K: '40-60' }, varieties: ['Pusa Sawani', 'Pusa A-4', 'Arka Anamika', 'Arka Abhay', 'Parbhani Kranti'], diseases: ['Yellow Vein Mosaic', 'Powdery Mildew', 'Cercospora Leaf Spot'], pests: ['Shoot and Fruit Borer', 'Jassids', 'Whitefly', 'Mite'], growingPeriod: '90-100 days', seedRate: '20-25 kg/ha' },
    'capsicum': { name: 'Capsicum', icon: '🫑', season: 'Zaid', temp: { min: 18, max: 25, optimal: 22 }, rainfall: { min: 50, max: 80, optimal: 65 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 3189, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '100-150', P: '40-60', K: '60-80' }, varieties: ['Indra', 'Bachata', 'Orobelle', 'California Wonder', 'Yolo Wonder'], diseases: ['Anthracnose', 'Powdery Mildew', 'Leaf Curl Virus'], pests: ['Fruit Borer', 'Aphids', 'Whitefly', 'Mite'], growingPeriod: '90-100 days', seedRate: '500-600 g/ha' },
    'cucumber': { name: 'Cucumber', icon: '🥒', season: 'Zaid', temp: { min: 21, max: 28, optimal: 24 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 2250, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '80-100', P: '40-50', K: '40-60' }, varieties: ['Pusa Sanyog', 'Japanese Long Green', 'Poinsette', 'Straight Eight', 'Himangi'], diseases: ['Powdery Mildew', 'Downy Mildew', 'Angular Leaf Spot', 'Mosaic Virus'], pests: ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'], growingPeriod: '50-70 days', seedRate: '2.5-3 kg/ha' },
    'watermelon': { name: 'Watermelon', icon: '🍉', season: 'Zaid', temp: { min: 21, max: 29, optimal: 25 }, rainfall: { min: 40, max: 60, optimal: 50 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy', 'Sandy'], price: 1526, fertilizer: 'Urea 80kg/ha, DAP 50kg/ha', npk: { N: '80-100', P: '40-50', K: '40-50' }, varieties: ['Sugar Baby', 'Arka Manik', 'Arka Jyoti', 'Pusa Bedana', 'Madhuri', 'Crimson Sweet'], diseases: ['Powdery Mildew', 'Downy Mildew', 'Fusarium Wilt', 'Anthracnose'], pests: ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'], growingPeriod: '80-100 days', seedRate: '3-4 kg/ha' },

    // FRUITS
    'banana': { name: 'Banana', icon: '🍌', season: 'Zaid', temp: { min: 10, max: 40, optimal: 25 }, rainfall: { min: 90, max: 120, optimal: 105 }, humidity: { min: 75, max: 85, optimal: 80 }, ph: { min: 6.0, max: 7.5, optimal: 6.5 }, soil: ['Acidic', 'Loamy'], price: 3639, fertilizer: 'Urea 200kg/ha, DAP 100kg/ha', npk: { N: '150-250', P: '60-100', K: '100-200' }, varieties: ['Grand Naine', 'Robusta', 'Dwarf Cavendish', 'Nendran', 'Poovan', 'Red Banana'], diseases: ['Panama Wilt', 'Sigatoka Leaf Spot', 'Bunchy Top', 'Anthracnose'], pests: ['Rhizome Weevil', 'Aphids', 'Nematodes', 'Thrips'], growingPeriod: '11-14 months', seedRate: '2500-3000 suckers/ha' },
    'apple': { name: 'Apple', icon: '🍎', season: 'Rabi', temp: { min: 15, max: 25, optimal: 20 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 5.5, max: 6.5, optimal: 6.0 }, soil: ['Loamy'], price: 12871, fertilizer: 'Urea 120kg/ha, DAP 80kg/ha', npk: { N: '100-150', P: '60-80', K: '80-120' }, varieties: ['Red Delicious', 'Golden Delicious', 'Royal Delicious', 'Gala', 'Fuji', 'Granny Smith'], diseases: ['Apple Scab', 'Powdery Mildew', 'Collar Rot', 'Sooty Blotch'], pests: ['San Jose Scale', 'Woolly Aphid', 'Codling Moth', 'Tent Caterpillar'], growingPeriod: 'Perennial (30-40 years)', seedRate: '400-500 plants/ha' },
    'mango': { name: 'Mango', icon: '🥭', season: 'Zaid', temp: { min: 18, max: 35, optimal: 27 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 60, max: 80, optimal: 70 }, ph: { min: 5.5, max: 7.5, optimal: 6.5 }, soil: ['Loamy', 'Sandy loam'], price: 35000, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '80-120', P: '40-60', K: '60-80' }, varieties: ['Alphonso', 'Dasheri', 'Langra', 'Totapuri', 'Kesar', 'Himsagar'], diseases: ['Powdery Mildew', 'Anthracnose', 'Die Back', 'Mango Malformation'], pests: ['Mango Hopper', 'Mealybug', 'Fruit Fly', 'Stem Borer'], growingPeriod: 'Perennial (30-40 years)', seedRate: '100-150 plants/ha' },
    'grapes': { name: 'Grapes', icon: '🍇', season: 'Zaid', temp: { min: 25, max: 32, optimal: 28 }, rainfall: { min: 65, max: 90, optimal: 78 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 8942, fertilizer: 'Urea 120kg/ha, DAP 60kg/ha', npk: { N: '100-150', P: '50-70', K: '60-80' }, varieties: ['Thompson Seedless', 'Bangalore Blue', 'Sharad Seedless', 'Sonaka', 'Manjari'], diseases: ['Downy Mildew', 'Powdery Mildew', 'Anthracnose', 'Black Rot'], pests: ['Thrips', 'Mealybug', 'Leaf Roller', 'Grape Vine Moth'], growingPeriod: 'Perennial', seedRate: '2000-2500 plants/ha' },
    'guava': { name: 'Guava', icon: '🍐', season: 'Zaid', temp: { min: 18, max: 32, optimal: 25 }, rainfall: { min: 100, max: 150, optimal: 125 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 5.5, max: 7.5, optimal: 6.5 }, soil: ['Sandy', 'Loamy'], price: 5290, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '80-100', P: '40-50', K: '60-80' }, varieties: ['Allahabad Safeda', 'Sardar (L-49)', 'Lalit', 'Shweta', 'Pant Prabhat'], diseases: ['Wilt', 'Fruit Rot', 'Anthracnose', 'Canker'], pests: ['Fruit Fly', 'Mealybug', 'Tea Mosquito Bug', 'Scale Insect'], growingPeriod: 'Perennial (30+ years)', seedRate: '275-300 plants/ha' },
    'papaya': { name: 'Papaya', icon: '🍈', season: 'Zaid', temp: { min: 23, max: 43, optimal: 33 }, rainfall: { min: 40, max: 250, optimal: 145 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 3087, fertilizer: 'Urea 150kg/ha, DAP 80kg/ha', npk: { N: '100-150', P: '50-80', K: '50-80' }, varieties: ['Pusa Delicious', 'Pusa Majesty', 'Pusa Giant', 'Pusa Dwarf', 'Coorg Honey Dew', 'Red Lady'], diseases: ['Papaya Ring Spot Virus', 'Powdery Mildew', 'Collar Rot', 'Anthracnose'], pests: ['Papaya Mealybug', 'Fruit Fly', 'Spider Mite', 'Whitefly'], growingPeriod: '2-3 years', seedRate: '1600-2000 plants/ha' },
    'lemon': { name: 'Lemon', icon: '🍋', season: 'Zaid', temp: { min: 20, max: 38, optimal: 29 }, rainfall: { min: 80, max: 120, optimal: 100 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 5.5, max: 7.0, optimal: 6.5 }, soil: ['Loamy'], price: 12845, fertilizer: 'Urea 80kg/ha, DAP 50kg/ha', npk: { N: '60-80', P: '40-50', K: '40-60' }, varieties: ['Pant Lemon-1', 'Assam Lemon', 'Kagzi Kalan', 'Eureka', 'Lisbon'], diseases: ['Citrus Canker', 'Gummosis', 'Tristeza', 'Scab'], pests: ['Citrus Psylla', 'Leaf Miner', 'Fruit Sucking Moth', 'Mealybug'], growingPeriod: 'Perennial (20+ years)', seedRate: '275-300 plants/ha' },

    // CASH CROPS
    'cotton': { name: 'Cotton', icon: '🌸', season: 'Kharif', temp: { min: 18, max: 29, optimal: 24 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Black cotton'], price: 7767, fertilizer: 'Urea 100kg/ha, DAP 50kg/ha', npk: { N: '80-120', P: '40-60', K: '40-60' }, varieties: ['BT Cotton', 'RCH 2', 'MRC 7351', 'Suraj', 'F 1861', 'Bikaneri Narma'], diseases: ['Leaf Curl Virus', 'Bacterial Blight', 'Fusarium Wilt', 'Alternaria Leaf Spot'], pests: ['Bollworm', 'Aphids', 'Jassids', 'Whitefly', 'Pink Bollworm'], growingPeriod: '160-180 days', seedRate: '2-3 kg/ha (BT), 8-10 kg/ha (varieties)' },
    'sugarcane': { name: 'Sugarcane', icon: '🎋', season: 'Zaid', temp: { min: 22, max: 32, optimal: 27 }, rainfall: { min: 150, max: 250, optimal: 200 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 3500, fertilizer: 'Urea 250kg/ha, DAP 100kg/ha', npk: { N: '150-250', P: '60-100', K: '80-150' }, varieties: ['Co 86032', 'Co 0238', 'Co 1148', 'CoJ 85', 'CoS 8436', 'Co 0118'], diseases: ['Red Rot', 'Smut', 'Wilt', 'Grassy Shoot'], pests: ['Early Shoot Borer', 'Top Borer', 'Stalk Borer', 'Pyrilla', 'Whitefly'], growingPeriod: '10-12 months', seedRate: '35000-40000 setts/ha' },
    'tea': { name: 'Tea', icon: '🍵', season: 'Zaid', temp: { min: 13, max: 32, optimal: 22 }, rainfall: { min: 150, max: 300, optimal: 225 }, humidity: { min: 75, max: 85, optimal: 80 }, ph: { min: 4.5, max: 5.5, optimal: 5.0 }, soil: ['Sandy', 'Acidic'], price: 27000, fertilizer: 'Urea 60kg/ha, DAP 30kg/ha', npk: { N: '60-80', P: '30-40', K: '30-40' }, varieties: ['TV 1', 'TV 9', 'TV 20', 'TV 23', 'T3E3', 'AV2', 'P 126'], diseases: ['Blister Blight', 'Red Rust', 'Black Rot', 'Brown Root Rot'], pests: ['Tea Mosquito Bug', 'Red Spider Mite', 'Looper Caterpillar', 'Thrips'], growingPeriod: 'Perennial (50+ years)', seedRate: '15000-17000 plants/ha' },
    'coffee': { name: 'Coffee', icon: '☕', season: 'Zaid', temp: { min: 23, max: 28, optimal: 25 }, rainfall: { min: 150, max: 250, optimal: 200 }, humidity: { min: 70, max: 85, optimal: 78 }, ph: { min: 5.0, max: 6.5, optimal: 5.8 }, soil: ['Volcanic', 'Acidic'], price: 20200, fertilizer: 'Urea 80kg/ha, DAP 40kg/ha', npk: { N: '80-100', P: '40-50', K: '40-50' }, varieties: ['Arabica S.795', 'Robusta S.274', 'Cauvery', 'Chandragiri', 'Sln.9'], diseases: ['Coffee Rust', 'Berry Disease', 'Black Rot', 'Root Rot'], pests: ['Coffee Berry Borer', 'White Stem Borer', 'Green Scale', 'Mealybug'], growingPeriod: 'Perennial (40-50 years)', seedRate: '1100-1300 plants/ha (Arabica), 800-1000 plants/ha (Robusta)' },

    // OILSEEDS
    'groundnut': { name: 'Groundnut', icon: '🥜', season: 'Kharif', temp: { min: 25, max: 35, optimal: 30 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.0, optimal: 6.5 }, soil: ['Sandy'], price: 6619, fertilizer: 'Urea 20kg/ha, DAP 60kg/ha', npk: { N: '20-40', P: '40-60', K: '30-40' }, varieties: ['TG 37A', 'GG 20', 'Kadiri 6', 'JL 24', 'TMV 2', 'ICGS 44'], diseases: ['Tikka Leaf Spot', 'Rust', 'Stem Rot', 'Collar Rot'], pests: ['Leaf Miner', 'Aphids', 'Thrips', 'White Grub'], growingPeriod: '105-120 days', seedRate: '100-120 kg/ha' },
    'soybean': { name: 'Soybean', icon: '🫘', season: 'Kharif', temp: { min: 20, max: 30, optimal: 25 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 65, max: 80, optimal: 72 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 5423, fertilizer: 'Urea 30kg/ha, DAP 60kg/ha', npk: { N: '20-40', P: '40-60', K: '20-40' }, varieties: ['JS 335', 'JS 95-60', 'MACS 450', 'Pusa 9712', 'NRC 37', 'JS 20-34'], diseases: ['Rust', 'Anthracnose', 'Bacterial Pustule', 'Yellow Mosaic'], pests: ['Girdle Beetle', 'Tobacco Caterpillar', 'Green Semilooper', 'Stem Fly'], growingPeriod: '90-100 days', seedRate: '60-70 kg/ha' },
    'sunflower': { name: 'Sunflower', icon: '🌻', season: 'Rabi', temp: { min: 24, max: 35, optimal: 30 }, rainfall: { min: 50, max: 100, optimal: 75 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Clay', 'Sandy'], price: 7500, fertilizer: 'Urea 60kg/ha, DAP 40kg/ha', npk: { N: '60-80', P: '40-50', K: '40-50' }, varieties: ['KBSH 1', 'Morden', 'DSH 1', 'PKVSH 27', 'RSFH 130', 'Jwalamukhi'], diseases: ['Alternaria Blight', 'Downy Mildew', 'Rust', 'Head Rot'], pests: ['Head Borer', 'Jassids', 'Bihar Hairy Caterpillar'], growingPeriod: '90-100 days', seedRate: '5-6 kg/ha' },
    'mustard': { name: 'Mustard', icon: '🌼', season: 'Rabi', temp: { min: 10, max: 25, optimal: 18 }, rainfall: { min: 40, max: 100, optimal: 70 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 6076, fertilizer: 'Urea 60kg/ha, DAP 40kg/ha', npk: { N: '60-80', P: '40-60', K: '20-40' }, varieties: ['Pusa Bold', 'Varuna', 'RH 749', 'Pusa Jai Kisan', 'NRCHB 101', 'RGN 48'], diseases: ['White Rust', 'Alternaria Blight', 'Powdery Mildew', 'Sclerotinia Rot'], pests: ['Mustard Aphid', 'Painted Bug', 'Sawfly', 'Leaf Miner'], growingPeriod: '120-140 days', seedRate: '4-5 kg/ha' },

    // PULSES
    'lentil': { name: 'Lentil', icon: '🫘', season: 'Rabi', temp: { min: 15, max: 21, optimal: 18 }, rainfall: { min: 35, max: 55, optimal: 45 }, humidity: { min: 60, max: 75, optimal: 68 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 6505, fertilizer: 'Urea 40kg/ha, DAP 30kg/ha', npk: { N: '20-40', P: '30-40', K: '20-30' }, varieties: ['Pusa Masoor-5', 'Pant L-4', 'K-75', 'PL 639', 'DPL 62'], diseases: ['Rust', 'Wilt', 'Blight', 'Powdery Mildew'], pests: ['Pod Borer', 'Aphids', 'Cutworms'], growingPeriod: '100-120 days', seedRate: '30-35 kg/ha' },
    'chickpea': { name: 'Chickpea', icon: '🫘', season: 'Rabi', temp: { min: 18, max: 30, optimal: 24 }, rainfall: { min: 40, max: 80, optimal: 60 }, humidity: { min: 55, max: 70, optimal: 62 }, ph: { min: 6.0, max: 7.5, optimal: 6.8 }, soil: ['Loamy'], price: 5200, fertilizer: 'Urea 20kg/ha, DAP 40kg/ha', npk: { N: '20-30', P: '40-50', K: '20-30' }, varieties: ['Desi - JG 11', 'Kabuli - L 550', 'Pusa 1053', 'Pusa 1103', 'PBG 1'], diseases: ['Wilt', 'Blight', 'Rust', 'Ascochyta Blight'], pests: ['Pod Borer', 'Aphids', 'Cutworms', 'Termites'], growingPeriod: '90-110 days', seedRate: '60-80 kg/ha' }
};

// ============================================
// SAFE HELPER FUNCTIONS (WITH ERROR HANDLING)
// ============================================

// SAFE FUNCTION TO GET CROP DATA
function getCropData(cropName) {
    if (!cropName) return null;
    const crop = cropName.toLowerCase().trim();
    if (CROP_DATABASE && CROP_DATABASE[crop]) {
        return CROP_DATABASE[crop];
    }
    return null;
}

// FUNCTION TO GET FULL CROP INFO (FIXED - NO undefined.min ERROR)
function getFullCropInfoResponse(crop) {
    const data = getCropData(crop);
    
    // SAFETY CHECK - Prevent undefined error
    if (!data) {
        return null;
    }
    
    // SAFE ACCESS with fallbacks using optional chaining
    const minTemp = data.temp?.min ?? data.min_temp ?? "N/A";
    const maxTemp = data.temp?.max ?? data.max_temp ?? "N/A";
    const minRain = data.rainfall?.min ?? data.min_rain ?? "N/A";
    const maxRain = data.rainfall?.max ?? data.max_rain ?? "N/A";
    const price = data.price ?? 0;
    const soilTypes = Array.isArray(data.soil) ? data.soil.join(', ') : (data.soil || 'N/A');
    
    return `${data.icon || '🌾'} **${data.name || crop} - Complete Growing Guide**\n\n` +
           `**📅 Season:** ${data.season || 'N/A'}\n` +
           `**🌡 Temperature:** ${minTemp}-${maxTemp}°C\n` +
           `**🌧 Rainfall:** ${minRain}-${maxRain}mm\n` +
           `**🪴 Soil Type:** ${soilTypes}\n` +
           `**💰 Market Price:** ₹${price.toLocaleString('en-IN')}/quintal\n` +
           `**🧪 Fertilizer:** ${data.fertilizer || 'N/A'}\n\n` +
           `💡 Ask me: "${crop} price" for market rates!`;
}

// FUNCTION TO GET PRICE RESPONSE (FIXED - NO toLocaleString ERROR)
function getPriceResponse(crop) {
    const data = getCropData(crop);
    
    // SAFETY CHECK - Prevent .toLocaleString() on undefined
    if (!data) {
        return `❌ Sorry, I don't have price information for "${crop}". Please try another crop like rice, wheat, or maize.`;
    }
    
    const price = data.price;
    
    // Check if price exists and is a number
    if (!price || typeof price !== 'number') {
        return `📊 ${data.name || crop} is in our database, but price information is currently unavailable.`;
    }
    
    // SAFE to call toLocaleString now
    return `💰 **${data.name || crop} Market Price**\n\n` +
           `📊 Current Price: **₹${price.toLocaleString('en-IN')}/quintal**\n` +
           `📅 Season: ${data.season || 'N/A'}\n` +
           `💡 Prices vary by region and demand. Check local mandi for exact rates.`;
}

// FUNCTION TO GET SOIL FOR CROP
function getSoilForCropResponse(crop) {
    const data = getCropData(crop);
    if (!data) return null;
    
    const soilTypes = Array.isArray(data.soil) ? data.soil.join(', ') : (data.soil || 'N/A');
    const minPh = data.ph?.min ?? data.min_ph ?? "N/A";
    const maxPh = data.ph?.max ?? data.max_ph ?? "N/A";
    
    return `🪴 **Soil Requirements for ${data.name || crop}**\n\n` +
           `✅ **Suitable Soil Types:** ${soilTypes}\n` +
           `🧪 **Optimal pH Range:** ${minPh}-${maxPh}\n\n` +
           `💡 Ask me: "${crop} NPK" for fertilizer requirements!`;
}

// FUNCTION TO GET NPK FOR CROP
function getNPKForCropResponse(crop) {
    const data = getCropData(crop);
    if (!data) return null;
    
    const npkN = data.npk?.N ?? "N/A";
    const npkP = data.npk?.P ?? "N/A";
    const npkK = data.npk?.K ?? "N/A";
    
    return `🧪 **Fertilizer for ${data.name || crop}**\n\n` +
           `**📊 Recommended Fertilizer:**\n${data.fertilizer || 'N/A'}\n\n` +
           `**📈 NPK Requirement:**\n` +
           `• 🟢 Nitrogen (N): ${npkN} kg/ha\n` +
           `• 🔵 Phosphorus (P): ${npkP} kg/ha\n` +
           `• 🔴 Potassium (K): ${npkK} kg/ha\n\n` +
           `💡 Conduct soil test before application.`;
}

// EXTRACT CROP NAME FROM MESSAGE
function extractCropName(message) {
    if (!message) return null;
    const msg = message.toLowerCase();
    const crops = Object.keys(CROP_DATABASE || {});
    for (let crop of crops) {
        if (msg.includes(crop)) return crop;
    }
    return null;
}

// DETECT INTENT OF USER QUERY
function detectIntent(message) {
    if (!message) return { type: 'UNKNOWN' };
    const msg = message.toLowerCase();
    
    // Extract crop name
    const cropMatch = extractCropName(msg);
    
    // Check for price queries
    if (msg.match(/price|rate|cost|market|₹|rs/)) {
        if (cropMatch) return { type: 'PRICE', crop: cropMatch };
    }
    
    // Check for soil queries
    if (msg.match(/soil/)) {
        if (cropMatch) return { type: 'SOIL_FOR_CROP', crop: cropMatch };
    }
    
    // Check for NPK/Fertilizer queries
    if (msg.match(/npk|fertilizer|urea|dap/)) {
        if (cropMatch) return { type: 'NPK_FOR_CROP', crop: cropMatch };
    }
    
    // Check for general crop info
    if (cropMatch) {
        return { type: 'CROP_INFO', crop: cropMatch };
    }
    
    // Check for help
    if (msg.match(/help|what can you do/)) return { type: 'HELP' };
    
    // Check for greeting
    if (msg.match(/hi|hello|hey|namaste/)) return { type: 'GREETING' };
    
    return { type: 'UNKNOWN' };
}

// MAIN GENERATE RESPONSE FUNCTION
function generateResponse(intent) {
    if (!intent) return getDefaultResponse();
    
    try {
        switch (intent.type) {
            case 'CROP_INFO':
                return getFullCropInfoResponse(intent.crop) || getDefaultResponse();
            case 'PRICE':
                return getPriceResponse(intent.crop) || getDefaultResponse();
            case 'SOIL_FOR_CROP':
                return getSoilForCropResponse(intent.crop) || getDefaultResponse();
            case 'NPK_FOR_CROP':
                return getNPKForCropResponse(intent.crop) || getDefaultResponse();
            case 'GREETING':
                return getGreetingResponse();
            case 'HELP':
                return getHelpResponse();
            default:
                return getDefaultResponse();
        }
    } catch (error) {
        console.error("Chatbot error:", error);
        return "⚠️ Sorry, I encountered an error. Please try again.";
    }
}

// GREETING RESPONSE
function getGreetingResponse() {
    if (chatbotTranslations.greeting) {
        return chatbotTranslations.greeting;
    }
    const lang = currentChatLanguage;
    const greetings = {
        'en': '👋 **Namaste! I\'m CropSense Assistant.** 🌾\n\nI can help you with:\n\n🌾 **Crops:** "Rice details", "Wheat info"\n💰 **Prices:** "Price of wheat", "Rice rate"\n🪴 **Soil:** "Soil for rice", "Wheat soil type"\n🧪 **NPK:** "NPK for banana", "Fertilizer for wheat"\n\n💡 **Type "help" to see everything I can do!**',
        'hi': '👋 **नमस्ते! मैं क्रॉपसेंस सहायक हूं।** 🌾\n\nमैं आपकी मदद कर सकता हूं:\n\n🌾 **फसलें:** "चावल की जानकारी", "गेहूं की जानकारी"\n💰 **कीमतें:** "गेहूं का दाम", "चावल का रेट"\n🪴 **मिट्टी:** "चावल के लिए मिट्टी", "गेहूं के लिए मिट्टी"\n🧪 **एनपीके:** "केले के लिए एनपीके", "गेहूं के लिए उर्वरक"\n\n💡 **"सहायता" टाइप करें मेरी सभी क्षमताओं के लिए!**'
    };
    return greetings[lang] || greetings['en'];
}

// HELP RESPONSE
function getHelpResponse() {
    if (chatbotTranslations.help) {
        return chatbotTranslations.help;
    }
    const lang = currentChatLanguage;
    const helpTexts = {
        'en': '🌾 **CropSense Assistant - Help Guide**\n\n**💰 PRICE QUERIES**\n• "Price of rice" - Get market price\n• "Wheat rate" - Current wheat price\n\n**🌾 CROP DETAILS**\n• "Rice details" - Complete crop information\n• "Wheat growing guide" - Cultivation info\n\n**🪴 SOIL REQUIREMENTS**\n• "Soil for rice" - Best soil for rice\n• "Wheat soil type" - Soil requirements\n\n**🧪 FERTILIZER**\n• "NPK for rice" - Fertilizer recommendation\n• "Fertilizer for wheat" - NPK requirements\n\n💡 Just type your question naturally!',
        'hi': '🌾 **क्रॉपसेंस सहायक - सहायता गाइड**\n\n**💰 कीमत संबंधी प्रश्न**\n• "चावल का दाम" - बाजार मूल्य प्राप्त करें\n• "गेहूं का रेट" - वर्तमान गेहूं मूल्य\n\n**🌾 फसल विवरण**\n• "चावल की जानकारी" - संपूर्ण फसल जानकारी\n• "गेहूं की खेती" - उन्नत जानकारी\n\n**🪴 मिट्टी की आवश्यकताएं**\n• "चावल के लिए मिट्टी" - चावल के लिए उपयुक्त मिट्टी\n• "गेहूं के लिए मिट्टी" - मिट्टी की आवश्यकताएं\n\n**🧪 उर्वरक**\n• "चावल के लिए एनपीके" - उर्वरक सिफारिश\n• "गेहूं के लिए उर्वरक" - एनपीके आवश्यकताएं\n\n💡 बस अपना प्रश्न टाइप करें!'
    };
    return helpTexts[lang] || helpTexts['en'];
}

// DEFAULT RESPONSE
function getDefaultResponse() {
    if (chatbotTranslations.not_sure) {
        return chatbotTranslations.not_sure;
    }
    const lang = currentChatLanguage;
    const defaultTexts = {
        'en': '🌾 I\'m not sure about that.\n\n💡 **Try asking:**\n• "Price of rice" - Get market price\n• "Rice details" - Crop information\n• "Soil for wheat" - Soil requirements\n• "NPK for maize" - Fertilizer advice\n• "What can you do?" - See all features\n\nType "help" to see everything I can do! 🌾',
        'hi': '🌾 मुझे इसके बारे में निश्चितता नहीं है।\n\n💡 **पूछने का प्रयास करें:**\n• "चावल का दाम" - बाजार मूल्य प्राप्त करें\n• "चावल की जानकारी" - फसल की जानकारी\n• "गेहूं के लिए मिट्टी" - मिट्टी की आवश्यकताएं\n• "मक्का के लिए एनपीके" - उर्वरक सलाह\n• "आप क्या कर सकते हैं?" - सभी सुविधाएं देखें\n\n"सहायता" टाइप करें मेरी सभी क्षमताओं के लिए! 🌾'
    };
    return defaultTexts[lang] || defaultTexts['en'];
}

// ============================================
// CHAT UI FUNCTIONS
// ============================================

// ADD MESSAGE TO CHAT
function addMessage(text, sender) {
    const chatContainer = document.getElementById('chat-msgs');
    if (!chatContainer) {
        console.error("Chat container not found");
        return;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-msg ${sender}`;
    messageDiv.innerHTML = text.replace(/\n/g, '<br>');
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// SHOW TYPING INDICATOR
function showTypingIndicator() {
    const chatContainer = document.getElementById('chat-msgs');
    if (!chatContainer) return;
    
    // Remove existing typing indicator
    removeTypingIndicator();
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-typing';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// REMOVE TYPING INDICATOR
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// SEND MESSAGE FUNCTION
async function sendMessage() {
    const input = document.getElementById('chat-input');
    if (!input) return;
    
    const message = input.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Try backend first, fall back to local
    try {
        const lang = currentChatLanguage || 'en';
        const resp = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, language: lang })
        });
        const data = await resp.json();
        removeTypingIndicator();
        if (data.success && data.response) {
            addMessage(data.response, 'bot');
        } else {
            // Fall back to local
            const intent = detectIntent(message);
            const response = generateResponse(intent);
            addMessage(response, 'bot');
        }
    } catch (err) {
        console.warn('Backend chat unavailable, using local:', err);
        removeTypingIndicator();
        // Fall back to local processing
        const intent = detectIntent(message);
        const response = generateResponse(intent);
        addMessage(response, 'bot');
    }
}

// TOGGLE CHAT PANEL
function toggleChat() {
    const panel = document.getElementById('chatbot-panel');
    if (panel) {
        panel.classList.toggle('open');
        if (panel.classList.contains('open')) {
            const input = document.getElementById('chat-input');
            if (input) input.focus();
        }
    }
}

// VOICE INPUT FUNCTION
function toggleVoice() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Voice input is not supported in this browser. Please use Chrome or Edge.');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    const voiceLangMap = { 'hi': 'hi-IN', 'kn': 'kn-IN', 'mr': 'mr-IN', 'ta': 'ta-IN', 'te': 'te-IN' };
    recognition.lang = voiceLangMap[currentChatLanguage] || 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    
    recognition.start();
    
    const voiceBtn = document.getElementById('chat-voice-btn');
    if (voiceBtn) {
        voiceBtn.classList.add('recording');
        voiceBtn.textContent = '⏺';
    }
    
    recognition.onresult = function(event) {
        const speechResult = event.results[0][0].transcript;
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = speechResult;
            sendMessage();
        }
        if (voiceBtn) {
            voiceBtn.classList.remove('recording');
            voiceBtn.textContent = '🎤';
        }
    };
    
    recognition.onerror = function() {
        if (voiceBtn) {
            voiceBtn.classList.remove('recording');
            voiceBtn.textContent = '🎤';
        }
        alert('Could not hear that. Please try again.');
    };
    
    recognition.onend = function() {
        if (voiceBtn) {
            voiceBtn.classList.remove('recording');
            voiceBtn.textContent = '🎤';
        }
    };
}

// UPDATE CHATBOT LANGUAGE
window.updateChatbotLanguage = function() {
    currentChatLanguage = localStorage.getItem('cropsense_lang') || 'en';
    console.log('✅ Chatbot language updated to:', currentChatLanguage);
    
    // Load translations for this language
    loadChatbotLanguage(currentChatLanguage).then(() => {
        // Update welcome message after translations loaded
        const welcomeMsg = document.querySelector('.chat-msg.bot:first-child');
        if (welcomeMsg) {
            welcomeMsg.textContent = getGreetingResponse().replace(/\*\*/g, '');
        }
    });
};

// INITIALIZE CHATBOT
function initChatbot() {
    console.log("🤖 Chatbot initializing...");
    
    // Attach send button event
    const sendBtn = document.querySelector('.chat-send');
    if (sendBtn) {
        sendBtn.onclick = sendMessage;
    }
    
    // Attach voice button event
    const voiceBtn = document.getElementById('chat-voice-btn');
    if (voiceBtn) {
        voiceBtn.onclick = toggleVoice;
    }
    
    // Attach enter key to input
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.onkeypress = function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        };
    }
    
    // Attach fab button
    const fabBtn = document.getElementById('chatbot-fab');
    if (fabBtn) {
        fabBtn.onclick = toggleChat;
    }
    
    // Attach close button
    const closeBtn = document.querySelector('.chat-close');
    if (closeBtn) {
        closeBtn.onclick = toggleChat;
    }
    
    // Update welcome message with translated greeting (async)
    loadChatbotLanguage(currentChatLanguage).then(() => {
        const welcomeMsg = document.querySelector('.chat-msg.bot:first-child');
        if (welcomeMsg) {
            welcomeMsg.textContent = getGreetingResponse().replace(/\*\*/g, '');
        }
    });
    console.log("✅ Chatbot initialized successfully!");
}

// ============================================
// EXPORT FUNCTIONS TO WINDOW OBJECT
// ============================================

window.CROP_DATABASE = CROP_DATABASE;
window.getCropData = getCropData;
window.getFullCropInfoResponse = getFullCropInfoResponse;
window.getPriceResponse = getPriceResponse;
window.getSoilForCropResponse = getSoilForCropResponse;
window.getNPKForCropResponse = getNPKForCropResponse;
window.extractCropName = extractCropName;
window.detectIntent = detectIntent;
window.generateResponse = generateResponse;
window.sendMessage = sendMessage;
window.toggleChat = toggleChat;
window.toggleVoice = toggleVoice;
window.initChatbot = initChatbot;
window.updateChatbotLanguage = updateChatbotLanguage;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChatbot);
} else {
    initChatbot();
}

console.log("✅ Chatbot fully loaded with " + Object.keys(CROP_DATABASE).length + " crops!");