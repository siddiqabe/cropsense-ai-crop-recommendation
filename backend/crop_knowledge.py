# Comprehensive crop knowledge database for CropSense chatbot
# Merges detailed data (diseases, pests, varieties) with CROP_INFO

CROP_DETAILED = {
    'rice': {
        'diseases': ['Blast', 'Bacterial Leaf Blight', 'Brown Spot', 'Sheath Blight'],
        'pests': ['Stem Borer', 'Leaf Folder', 'Brown Planthopper', 'Gall Midge'],
        'varieties': ['Basmati', 'Sona Masoori', 'IR64', 'Swarna', 'Pusa 1121'],
        'growing_period': '110-150 days', 'seed_rate': '20-25 kg/ha',
        'npk': {'N': '90-120', 'P': '40-60', 'K': '40-60'}
    },
    'wheat': {
        'diseases': ['Rust', 'Powdery Mildew', 'Loose Smut', 'Karnal Bunt'],
        'pests': ['Aphids', 'Termites', 'Armyworm', 'Shoot Fly'],
        'varieties': ['HD 2967', 'PBW 343', 'WH 1105', 'Lok-1', 'GW 366'],
        'growing_period': '110-150 days', 'seed_rate': '100-125 kg/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '30-50'}
    },
    'maize': {
        'diseases': ['Turcicum Leaf Blight', 'Downy Mildew', 'Stalk Rot'],
        'pests': ['Stem Borer', 'Fall Armyworm', 'Shoot Fly', 'Cutworm'],
        'varieties': ['Pioneer 30V92', 'NK 6240', 'Dekalb 9108', 'PMH 1', 'Vivek 9'],
        'growing_period': '90-110 days', 'seed_rate': '18-20 kg/ha',
        'npk': {'N': '90-150', 'P': '50-70', 'K': '40-60'}
    },
    'ragi': {
        'diseases': ['Blast', 'Downy Mildew', 'Smut', 'Foot Rot'],
        'pests': ['Stem Borer', 'Aphids', 'Armyworm', 'Root Aphid'],
        'varieties': ['GPU 28', 'MR 1', 'HR 911', 'GPU 45', 'VL 149', 'Indaf 5'],
        'growing_period': '110-120 days', 'seed_rate': '8-10 kg/ha',
        'npk': {'N': '40-60', 'P': '40-60', 'K': '20-40'}
    },
    'millets': {
        'diseases': ['Downy Mildew', 'Ergot', 'Smut', 'Rust'],
        'pests': ['Shoot Fly', 'Stem Borer', 'Blister Beetle', 'Earhead Bug'],
        'varieties': ['GHB 558', 'HHB 67', 'ICTP 8203', 'Pusa Composite 443'],
        'growing_period': '80-90 days', 'seed_rate': '4-5 kg/ha',
        'npk': {'N': '40-60', 'P': '30-50', 'K': '20-40'}
    },
    'potato': {
        'diseases': ['Late Blight', 'Early Blight', 'Black Scurf', 'Common Scab'],
        'pests': ['Aphids', 'Cutworms', 'White Grubs', 'Potato Tuber Moth'],
        'varieties': ['Kufri Jyoti', 'Kufri Chandramukhi', 'Kufri Bahar', 'Kufri Pukhraj'],
        'growing_period': '90-100 days', 'seed_rate': '20-25 quintals/ha',
        'npk': {'N': '100-150', 'P': '60-80', 'K': '100-150'}
    },
    'tomato': {
        'diseases': ['Early Blight', 'Late Blight', 'Leaf Curl Virus', 'Bacterial Wilt'],
        'pests': ['Fruit Borer', 'Leaf Miner', 'Whitefly', 'Aphids'],
        'varieties': ['Arka Vikas', 'Arka Rakshak', 'Pusa Ruby', 'Pusa Early Dwarf'],
        'growing_period': '100-120 days', 'seed_rate': '400-500 g/ha',
        'npk': {'N': '100-150', 'P': '60-80', 'K': '60-80'}
    },
    'onion': {
        'diseases': ['Purple Blotch', 'Downy Mildew', 'Basal Rot'],
        'pests': ['Thrips', 'Onion Fly', 'Cutworms'],
        'varieties': ['NHRDF Red', 'Agrifound Dark Red', 'Arka Kalyan', 'Pusa Red'],
        'growing_period': '120-150 days', 'seed_rate': '8-10 kg/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'brinjal': {
        'diseases': ['Little Leaf', 'Phomopsis Blight', 'Bacterial Wilt', 'Cercospora Leaf Spot'],
        'pests': ['Shoot and Fruit Borer', 'Jassids', 'Whitefly', 'Mite'],
        'varieties': ['Pusa Purple Long', 'Pusa Kranti', 'Arka Navneet', 'Arka Shirish'],
        'growing_period': '120-150 days', 'seed_rate': '400-500 g/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'cabbage': {
        'diseases': ['Black Rot', 'Club Root', 'Downy Mildew'],
        'pests': ['Diamondback Moth', 'Cabbage Butterfly', 'Aphids'],
        'varieties': ['Golden Acre', 'Pusa Drumhead', 'Pusa Mukta', 'Pride of India'],
        'growing_period': '70-90 days', 'seed_rate': '400-500 g/ha',
        'npk': {'N': '100-150', 'P': '40-60', 'K': '60-80'}
    },
    'cauliflower': {
        'diseases': ['Black Rot', 'Club Root', 'Downy Mildew', 'Stalk Rot'],
        'pests': ['Diamondback Moth', 'Aphids', 'Tobacco Caterpillar'],
        'varieties': ['Pusa Deepali', 'Pusa Himjyoti', 'Pusa Snowball-1', 'Pusa Shubhra'],
        'growing_period': '70-100 days', 'seed_rate': '400-500 g/ha',
        'npk': {'N': '100-150', 'P': '40-60', 'K': '60-80'}
    },
    'spinach': {
        'diseases': ['Damping Off', 'Leaf Spot', 'Downy Mildew', 'White Rust'],
        'pests': ['Leaf Miner', 'Aphids', 'Cutworms'],
        'varieties': ['Pusa Jyoti', 'Pusa Harit', 'All Green', 'Virginia Savoy'],
        'growing_period': '25-30 days', 'seed_rate': '30-40 kg/ha',
        'npk': {'N': '60-80', 'P': '40-50', 'K': '40-60'}
    },
    'carrot': {
        'diseases': ['Leaf Blight', 'Powdery Mildew', 'Root Rot'],
        'pests': ['Carrot Rust Fly', 'Aphids', 'Nematodes'],
        'varieties': ['Pusa Kesar', 'Pusa Meghali', 'Pusa Rudhira', 'Nantes', 'Chantenay'],
        'growing_period': '80-100 days', 'seed_rate': '5-6 kg/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'beetroot': {
        'diseases': ['Cercospora Leaf Spot', 'Downy Mildew', 'Root Rot'],
        'pests': ['Leaf Miner', 'Aphids', 'Webworm'],
        'varieties': ['Detroit Dark Red', 'Crimson Globe', 'Crosby Egyptian', 'Early Wonder'],
        'growing_period': '60-80 days', 'seed_rate': '8-10 kg/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'radish': {
        'diseases': ['White Rust', 'Alternaria Leaf Spot', 'Root Rot'],
        'pests': ['Mustard Sawfly', 'Aphids', 'Painted Bug'],
        'varieties': ['Pusa Chetki', 'Pusa Desi', 'Pusa Himani', 'Japanese White'],
        'growing_period': '40-50 days', 'seed_rate': '10-12 kg/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'peas': {
        'diseases': ['Powdery Mildew', 'Rust', 'Wilt', 'Ascochyta Blight'],
        'pests': ['Pea Leaf Miner', 'Pod Borer', 'Aphids'],
        'varieties': ['Arkel', 'Bonneville', 'Azad P-1', 'Pusa Pragati', 'Pant Matar-2'],
        'growing_period': '60-70 days', 'seed_rate': '60-75 kg/ha',
        'npk': {'N': '40-60', 'P': '40-60', 'K': '30-50'}
    },
    'okra': {
        'diseases': ['Yellow Vein Mosaic', 'Powdery Mildew', 'Cercospora Leaf Spot'],
        'pests': ['Shoot and Fruit Borer', 'Jassids', 'Whitefly', 'Mite'],
        'varieties': ['Pusa Sawani', 'Pusa A-4', 'Arka Anamika', 'Arka Abhay', 'Parbhani Kranti'],
        'growing_period': '90-100 days', 'seed_rate': '20-25 kg/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '40-60'}
    },
    'capsicum': {
        'diseases': ['Anthracnose', 'Powdery Mildew', 'Leaf Curl Virus'],
        'pests': ['Fruit Borer', 'Aphids', 'Whitefly', 'Mite'],
        'varieties': ['Indra', 'Bachata', 'Orobelle', 'California Wonder', 'Yolo Wonder'],
        'growing_period': '90-100 days', 'seed_rate': '500-600 g/ha',
        'npk': {'N': '100-150', 'P': '40-60', 'K': '60-80'}
    },
    'cucumber': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Angular Leaf Spot', 'Mosaic Virus'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'],
        'varieties': ['Pusa Sanyog', 'Japanese Long Green', 'Poinsette', 'Straight Eight', 'Himangi'],
        'growing_period': '50-70 days', 'seed_rate': '2.5-3 kg/ha',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '40-60'}
    },
    'watermelon': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Fusarium Wilt', 'Anthracnose'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'],
        'varieties': ['Sugar Baby', 'Arka Manik', 'Arka Jyoti', 'Pusa Bedana', 'Madhuri', 'Crimson Sweet'],
        'growing_period': '80-100 days', 'seed_rate': '3-4 kg/ha',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '40-50'}
    },
    'banana': {
        'diseases': ['Panama Wilt', 'Sigatoka Leaf Spot', 'Bunchy Top', 'Anthracnose'],
        'pests': ['Rhizome Weevil', 'Aphids', 'Nematodes', 'Thrips'],
        'varieties': ['Grand Naine', 'Robusta', 'Dwarf Cavendish', 'Nendran', 'Poovan', 'Red Banana'],
        'growing_period': '11-14 months', 'seed_rate': '2500-3000 suckers/ha',
        'npk': {'N': '150-250', 'P': '60-100', 'K': '100-200'}
    },
    'apple': {
        'diseases': ['Apple Scab', 'Powdery Mildew', 'Collar Rot', 'Sooty Blotch'],
        'pests': ['San Jose Scale', 'Woolly Aphid', 'Codling Moth', 'Tent Caterpillar'],
        'varieties': ['Red Delicious', 'Golden Delicious', 'Royal Delicious', 'Gala', 'Fuji', 'Granny Smith'],
        'growing_period': 'Perennial (30-40 years)', 'seed_rate': '400-500 plants/ha',
        'npk': {'N': '100-150', 'P': '60-80', 'K': '80-120'}
    },
    'mango': {
        'diseases': ['Powdery Mildew', 'Anthracnose', 'Die Back', 'Mango Malformation'],
        'pests': ['Mango Hopper', 'Mealybug', 'Fruit Fly', 'Stem Borer'],
        'varieties': ['Alphonso', 'Dasheri', 'Langra', 'Totapuri', 'Kesar', 'Himsagar'],
        'growing_period': 'Perennial (30-40 years)', 'seed_rate': '100-150 plants/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'grapes': {
        'diseases': ['Downy Mildew', 'Powdery Mildew', 'Anthracnose', 'Black Rot'],
        'pests': ['Thrips', 'Mealybug', 'Leaf Roller', 'Grape Vine Moth'],
        'varieties': ['Thompson Seedless', 'Bangalore Blue', 'Sharad Seedless', 'Sonaka', 'Manjari'],
        'growing_period': 'Perennial', 'seed_rate': '2000-2500 plants/ha',
        'npk': {'N': '100-150', 'P': '50-70', 'K': '60-80'}
    },
    'guava': {
        'diseases': ['Wilt', 'Fruit Rot', 'Anthracnose', 'Canker'],
        'pests': ['Fruit Fly', 'Mealybug', 'Tea Mosquito Bug', 'Scale Insect'],
        'varieties': ['Allahabad Safeda', 'Sardar (L-49)', 'Lalit', 'Shweta', 'Pant Prabhat'],
        'growing_period': 'Perennial (30+ years)', 'seed_rate': '275-300 plants/ha',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '60-80'}
    },
    'papaya': {
        'diseases': ['Papaya Ring Spot Virus', 'Powdery Mildew', 'Collar Rot', 'Anthracnose'],
        'pests': ['Papaya Mealybug', 'Fruit Fly', 'Spider Mite', 'Whitefly'],
        'varieties': ['Pusa Delicious', 'Pusa Majesty', 'Pusa Giant', 'Pusa Dwarf', 'Coorg Honey Dew', 'Red Lady'],
        'growing_period': '2-3 years', 'seed_rate': '1600-2000 plants/ha',
        'npk': {'N': '100-150', 'P': '50-80', 'K': '50-80'}
    },
    'lemon': {
        'diseases': ['Citrus Canker', 'Gummosis', 'Tristeza', 'Scab'],
        'pests': ['Citrus Psylla', 'Leaf Miner', 'Fruit Sucking Moth', 'Mealybug'],
        'varieties': ['Pant Lemon-1', 'Assam Lemon', 'Kagzi Kalan', 'Eureka', 'Lisbon'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '275-300 plants/ha',
        'npk': {'N': '60-80', 'P': '40-50', 'K': '40-60'}
    },
    'cotton': {
        'diseases': ['Leaf Curl Virus', 'Bacterial Blight', 'Fusarium Wilt', 'Alternaria Leaf Spot'],
        'pests': ['Bollworm', 'Aphids', 'Jassids', 'Whitefly', 'Pink Bollworm'],
        'varieties': ['BT Cotton', 'RCH 2', 'MRC 7351', 'Suraj', 'F 1861', 'Bikaneri Narma'],
        'growing_period': '160-180 days', 'seed_rate': '2-3 kg/ha (BT), 8-10 kg/ha (varieties)',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '40-60'}
    },
    'sugarcane': {
        'diseases': ['Red Rot', 'Smut', 'Wilt', 'Grassy Shoot'],
        'pests': ['Early Shoot Borer', 'Top Borer', 'Stalk Borer', 'Pyrilla', 'Whitefly'],
        'varieties': ['Co 86032', 'Co 0238', 'Co 1148', 'CoJ 85', 'CoS 8436', 'Co 0118'],
        'growing_period': '10-12 months', 'seed_rate': '35000-40000 setts/ha',
        'npk': {'N': '150-250', 'P': '60-100', 'K': '80-150'}
    },
    'tea': {
        'diseases': ['Blister Blight', 'Red Rust', 'Black Rot', 'Brown Root Rot'],
        'pests': ['Tea Mosquito Bug', 'Red Spider Mite', 'Looper Caterpillar', 'Thrips'],
        'varieties': ['TV 1', 'TV 9', 'TV 20', 'TV 23', 'T3E3', 'AV2', 'P 126'],
        'growing_period': 'Perennial (50+ years)', 'seed_rate': '15000-17000 plants/ha',
        'npk': {'N': '60-80', 'P': '30-40', 'K': '30-40'}
    },
    'coffee': {
        'diseases': ['Coffee Rust', 'Berry Disease', 'Black Rot', 'Root Rot'],
        'pests': ['Coffee Berry Borer', 'White Stem Borer', 'Green Scale', 'Mealybug'],
        'varieties': ['Arabica S.795', 'Robusta S.274', 'Cauvery', 'Chandragiri', 'Sln.9'],
        'growing_period': 'Perennial (40-50 years)', 'seed_rate': '1100-1300 plants/ha (Arabica), 800-1000 plants/ha (Robusta)',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '40-50'}
    },
    'groundnut': {
        'diseases': ['Tikka Leaf Spot', 'Rust', 'Stem Rot', 'Collar Rot'],
        'pests': ['Leaf Miner', 'Aphids', 'Thrips', 'White Grub'],
        'varieties': ['TG 37A', 'GG 20', 'Kadiri 6', 'JL 24', 'TMV 2', 'ICGS 44'],
        'growing_period': '105-120 days', 'seed_rate': '100-120 kg/ha',
        'npk': {'N': '20-40', 'P': '40-60', 'K': '30-40'}
    },
    'soybean': {
        'diseases': ['Rust', 'Anthracnose', 'Bacterial Pustule', 'Yellow Mosaic'],
        'pests': ['Girdle Beetle', 'Tobacco Caterpillar', 'Green Semilooper', 'Stem Fly'],
        'varieties': ['JS 335', 'JS 95-60', 'MACS 450', 'Pusa 9712', 'NRC 37', 'JS 20-34'],
        'growing_period': '90-100 days', 'seed_rate': '60-70 kg/ha',
        'npk': {'N': '20-40', 'P': '40-60', 'K': '20-40'}
    },
    'sunflower': {
        'diseases': ['Alternaria Blight', 'Downy Mildew', 'Rust', 'Head Rot'],
        'pests': ['Head Borer', 'Jassids', 'Bihar Hairy Caterpillar'],
        'varieties': ['KBSH 1', 'Morden', 'DSH 1', 'PKVSH 27', 'RSFH 130', 'Jwalamukhi'],
        'growing_period': '90-100 days', 'seed_rate': '5-6 kg/ha',
        'npk': {'N': '60-80', 'P': '40-50', 'K': '40-50'}
    },
    'mustard': {
        'diseases': ['White Rust', 'Alternaria Blight', 'Powdery Mildew', 'Sclerotinia Rot'],
        'pests': ['Mustard Aphid', 'Painted Bug', 'Sawfly', 'Leaf Miner'],
        'varieties': ['Pusa Bold', 'Varuna', 'RH 749', 'Pusa Jai Kisan', 'NRCHB 101', 'RGN 48'],
        'growing_period': '120-140 days', 'seed_rate': '4-5 kg/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '20-40'}
    },
    'lentil': {
        'diseases': ['Rust', 'Wilt', 'Blight', 'Powdery Mildew'],
        'pests': ['Pod Borer', 'Aphids', 'Cutworms'],
        'varieties': ['Pusa Masoor-5', 'Pant L-4', 'K-75', 'PL 639', 'DPL 62'],
        'growing_period': '100-120 days', 'seed_rate': '30-35 kg/ha',
        'npk': {'N': '20-40', 'P': '30-40', 'K': '20-30'}
    },
    'chickpea': {
        'diseases': ['Wilt', 'Blight', 'Rust', 'Ascochyta Blight'],
        'pests': ['Pod Borer', 'Aphids', 'Cutworms', 'Termites'],
        'varieties': ['Desi - JG 11', 'Kabuli - L 550', 'Pusa 1053', 'Pusa 1103', 'PBG 1'],
        'growing_period': '90-110 days', 'seed_rate': '60-80 kg/ha',
        'npk': {'N': '20-30', 'P': '40-50', 'K': '20-30'}
    },
    'barley': {
        'diseases': ['Rust', 'Powdery Mildew', 'Loose Smut', 'Net Blotch'],
        'pests': ['Aphids', 'Armyworm', 'Wireworm'],
        'varieties': ['BH 393', 'BH 902', 'RD 2508', 'RD 2552', 'PL 807'],
        'growing_period': '100-130 days', 'seed_rate': '80-100 kg/ha',
        'npk': {'N': '60-80', 'P': '30-40', 'K': '20-30'}
    },
    'orange': {
        'diseases': ['Citrus Canker', 'Gummosis', 'Scab', 'Tristeza'],
        'pests': ['Citrus Psylla', 'Leaf Miner', 'Fruit Fly', 'Mite'],
        'varieties': ['Nagpur Orange', 'Kinnow', 'Khasi Orange', 'Darjeeling Orange'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '275-300 plants/ha',
        'npk': {'N': '60-100', 'P': '40-60', 'K': '40-60'}
    },
    'pomegranate': {
        'diseases': ['Bacterial Blight', 'Wilt', 'Alternaria Leaf Spot', 'Fruit Rot'],
        'pests': ['Fruit Borer', 'Aphids', 'Mealybug', 'Mite'],
        'varieties': ['Bhagwa', 'Ganesh', 'Amildana', 'Mridula', 'Arakta'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '400-500 plants/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'muskmelon': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Fusarium Wilt', 'Mosaic Virus'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'],
        'varieties': ['Punjab Sunehri', 'Pusa Madhuras', 'Arka Rajhans', 'Hara Madhu'],
        'growing_period': '80-100 days', 'seed_rate': '2-3 kg/ha',
        'npk': {'N': '60-80', 'P': '30-50', 'K': '30-50'}
    },
    'turmeric': {
        'diseases': ['Leaf Spot', 'Rhizome Rot', 'Bacterial Wilt', 'Leaf Blight'],
        'pests': ['Shoot Borer', 'Rhizome Fly', 'Scale Insect'],
        'varieties': ['Alleppey', 'Salem', 'Erode', 'Nizamabad', 'Kasturi'],
        'growing_period': '7-9 months', 'seed_rate': '2500-3000 kg/ha',
        'npk': {'N': '80-100', 'P': '40-60', 'K': '60-80'}
    },
    'ginger': {
        'diseases': ['Rhizome Rot', 'Leaf Spot', 'Bacterial Wilt', 'Mosaic Virus'],
        'pests': ['Shoot Borer', 'Rhizome Fly', 'Nematodes'],
        'varieties': ['Maran', 'Varada', 'Nadia', 'Siddharth', 'IISR Varada'],
        'growing_period': '8-9 months', 'seed_rate': '1500-2000 kg/ha',
        'npk': {'N': '60-80', 'P': '30-50', 'K': '40-60'}
    },
    'coconut': {
        'diseases': ['Root Wilt', 'Bud Rot', 'Leaf Rot', 'Tanjore Wilt'],
        'pests': ['Rhinoceros Beetle', 'Red Palm Weevil', 'Coconut Mite', 'Black Headed Caterpillar'],
        'varieties': ['West Coast Tall', 'Chowghat Orange Dwarf', 'Kalpatharu', 'Malayan Tall'],
        'growing_period': 'Perennial (60+ years)', 'seed_rate': '175-200 plants/ha',
        'npk': {'N': '150-200', 'P': '80-100', 'K': '150-200'}
    },
    'jute': {
        'diseases': ['Stem Rot', 'Root Rot', 'Leaf Mosaic', 'Jute Wilt'],
        'pests': ['Jute Semilooper', 'Jute Hairy Caterpillar', 'Stem Weevil', 'Mite'],
        'varieties': ['JRO 204', 'JRC 321', 'JRO 524', 'Surenma'],
        'growing_period': '120-150 days', 'seed_rate': '8-10 kg/ha',
        'npk': {'N': '60-80', 'P': '30-40', 'K': '30-40'}
    },
    'pigeonpea': {
        'diseases': ['Wilt', 'Sterility Mosaic', 'Phytophthora Blight', 'Alternaria Leaf Spot'],
        'pests': ['Pod Borer', 'Pod Fly', 'Plume Moth', 'Spotted Pod Borer'],
        'varieties': ['Maruti', 'Sharad', 'BSMR 736', 'ICP 8863', 'Asha'],
        'growing_period': '140-180 days', 'seed_rate': '15-20 kg/ha',
        'npk': {'N': '25-35', 'P': '20-30', 'K': '20-30'}
    },
    'blackgram': {
        'diseases': ['Yellow Mosaic', 'Leaf Crinkle', 'Powdery Mildew', 'Cercospora Leaf Spot'],
        'pests': ['Pod Borer', 'Aphids', 'Jassids', 'Whitefly'],
        'varieties': ['LBG 20', 'LBG 402', 'PU 31', 'Vamban 4', 'Pant U-31'],
        'growing_period': '70-90 days', 'seed_rate': '20-25 kg/ha',
        'npk': {'N': '25-35', 'P': '20-30', 'K': '20-30'}
    },
    'greengram': {
        'diseases': ['Yellow Mosaic', 'Leaf Crinkle', 'Powdery Mildew', 'Root Rot'],
        'pests': ['Pod Borer', 'Aphids', 'Jassids', 'Whitefly'],
        'varieties': ['Pusa Vishal', 'Pusa Ratna', 'SML 668', 'IPM 02-3', 'Pant Mung-5'],
        'growing_period': '60-70 days', 'seed_rate': '15-20 kg/ha',
        'npk': {'N': '25-30', 'P': '20-30', 'K': '20-30'}
    },
    'horsegram': {
        'diseases': ['Powdery Mildew', 'Rust', 'Leaf Spot', 'Root Rot'],
        'pests': ['Pod Borer', 'Aphids', 'Leaf Eating Caterpillar'],
        'varieties': ['Kadmal', 'Paiyur 2', 'Bilaspur Local', 'HPK 2'],
        'growing_period': '90-120 days', 'seed_rate': '30-40 kg/ha',
        'npk': {'N': '25-30', 'P': '20-30', 'K': '20-30'}
    },
    'sesame': {
        'diseases': ['Leaf Spot', 'Alternaria Blight', 'Powdery Mildew', 'Phyllody'],
        'pests': ['Leaf Roller', 'Aphids', 'Gall Fly', 'Pod Bug'],
        'varieties': ['Pragati', 'TKG 22', 'GT 1', 'GT 2', 'RT 46'],
        'growing_period': '70-90 days', 'seed_rate': '4-5 kg/ha',
        'npk': {'N': '40-60', 'P': '40-60', 'K': '40-60'}
    },
    'castor': {
        'diseases': ['Alternaria Blight', 'Seedling Blight', 'Powdery Mildew', 'Wilt'],
        'pests': ['Castor Semilooper', 'Jassids', 'Shoot Borer', 'Tobacco Caterpillar'],
        'varieties': ['DCH 519', 'GCH 7', '48-1', 'TMV 5', 'Jyoti'],
        'growing_period': '120-150 days', 'seed_rate': '10-15 kg/ha',
        'npk': {'N': '40-60', 'P': '30-50', 'K': '30-50'}
    },
    'coriander': {
        'diseases': ['Powdery Mildew', 'Wilt', 'Stem Rot', 'Leaf Spot'],
        'pests': ['Aphids', 'Whitefly', 'Cutworm'],
        'varieties': ['Sadhana', 'Gujarat Coriander 1', 'R Cr 20', 'R Cr 436'],
        'growing_period': '90-110 days', 'seed_rate': '12-15 kg/ha',
        'npk': {'N': '40-60', 'P': '30-40', 'K': '30-40'}
    },
    'cumin': {
        'diseases': ['Powdery Mildew', 'Blight', 'Fusarium Wilt', 'Root Rot'],
        'pests': ['Aphids', 'Fruit Borer', 'Thrips'],
        'varieties': ['GC 1', 'GC 4', 'RZ 19', 'RZ 223', 'Gujarat Cumin 5'],
        'growing_period': '120-140 days', 'seed_rate': '12-15 kg/ha',
        'npk': {'N': '40-60', 'P': '30-40', 'K': '30-40'}
    },
    'fennel': {
        'diseases': ['Powdery Mildew', 'Wilt', 'Leaf Spot', 'Root Rot'],
        'pests': ['Aphids', 'Fruit Borer', 'Cutworm'],
        'varieties': ['GF 1', 'GF 2', 'RF 125', 'PF 36', 'Gujarat Fennel 2'],
        'growing_period': '180-210 days', 'seed_rate': '10-12 kg/ha',
        'npk': {'N': '40-60', 'P': '30-40', 'K': '30-40'}
    },
    'fenugreek': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Root Rot', 'Leaf Spot'],
        'pests': ['Aphids', 'Jassids', 'Leaf Eating Caterpillar'],
        'varieties': ['Methi No.1', 'RMT 1', 'RMT 305', 'Pant Raje', 'HM 103'],
        'growing_period': '90-110 days', 'seed_rate': '20-25 kg/ha',
        'npk': {'N': '40-60', 'P': '30-40', 'K': '30-40'}
    },
    'strawberry': {
        'diseases': ['Grey Mould', 'Powdery Mildew', 'Leaf Spot', 'Anthracnose'],
        'pests': ['Aphids', 'Spider Mite', 'Slugs', 'Thrips'],
        'varieties': ['Camarosa', 'Chandler', 'Sweet Charlie', 'Festival', 'Winter Dawn'],
        'growing_period': '90-120 days', 'seed_rate': '40000-50000 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'mint': {
        'diseases': ['Powdery Mildew', 'Leaf Spot', 'Rust', 'Wilt'],
        'pests': ['Aphids', 'Leaf Roller', 'Cutworm'],
        'varieties': ['Kosi', 'Himalaya', 'Saksham', 'Saryu', 'CIM Kranti'],
        'growing_period': '90-110 days', 'seed_rate': '500-600 kg/ha (suckers)',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'beans': {
        'diseases': ['Rust', 'Powdery Mildew', 'Bacterial Blight', 'Mosaic Virus'],
        'pests': ['Pod Borer', 'Aphids', 'Jassids', 'Thrips'],
        'varieties': ['Contender', 'Masterpiece', 'Pusa Parvati', 'Arka Komal', 'VL Bauni 1'],
        'growing_period': '70-90 days', 'seed_rate': '60-75 kg/ha',
        'npk': {'N': '20-30', 'P': '40-60', 'K': '20-30'}
    },
    'pumpkin': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Fruit Rot', 'Mosaic Virus'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids', 'Cucumber Beetle'],
        'varieties': ['Arka Suryamukhi', 'Pusa Vikas', 'Pusa Hybrid 1', 'Punjab Samrat'],
        'growing_period': '80-100 days', 'seed_rate': '3-4 kg/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'bittergourd': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Fusarium Wilt', 'Mosaic Virus'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'],
        'varieties': ['Pusa Purvi', 'Arka Harit', 'Priya', 'VNR 26', 'Jolly'],
        'growing_period': '55-75 days', 'seed_rate': '3-4 kg/ha',
        'npk': {'N': '60-80', 'P': '30-50', 'K': '40-60'}
    },
    'bottlegourd': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Fruit Rot', 'Mosaic Virus'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'],
        'varieties': ['Pusa Naveen', 'Pusa Samridhi', 'Arka Bahaar', 'Punjab Long'],
        'growing_period': '60-80 days', 'seed_rate': '4-5 kg/ha',
        'npk': {'N': '60-80', 'P': '30-50', 'K': '40-60'}
    },
    'ridgegourd': {
        'diseases': ['Powdery Mildew', 'Downy Mildew', 'Leaf Spot', 'Fruit Rot'],
        'pests': ['Fruit Fly', 'Red Pumpkin Beetle', 'Aphids'],
        'varieties': ['Pusa Nasdar', 'Pusa Smooth', 'Arka Sumeet', 'Shalimar'],
        'growing_period': '60-80 days', 'seed_rate': '3-4 kg/ha',
        'npk': {'N': '60-80', 'P': '30-50', 'K': '40-60'}
    },
    'sweetpotato': {
        'diseases': ['Leaf Spot', 'Stem Rot', 'Root Rot', 'Mosaic Virus'],
        'pests': ['Weevil', 'Leaf Eating Caterpillar', 'Wireworm'],
        'varieties': ['Sree Bhadra', 'Sree Kanaka', 'Sree Naveen', 'Sree Vardhini'],
        'growing_period': '90-120 days', 'seed_rate': '40000-50000 cuttings/ha',
        'npk': {'N': '80-120', 'P': '40-60', 'K': '60-80'}
    },
    'yam': {
        'diseases': ['Leaf Spot', 'Anthracnose', 'Tuber Rot', 'Mosaic Virus'],
        'pests': ['Yam Beetle', 'Root Knot Nematode', 'Mealybug'],
        'varieties': ['Sree Ravi', 'Sree Priya', 'Neelakanta', 'Sree Subhra'],
        'growing_period': '8-10 months', 'seed_rate': '4000-5000 kg/ha (tubers)',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '60-80'}
    },
    'tamarind': {
        'diseases': ['Leaf Spot', 'Powdery Mildew', 'Sooty Mould', 'Stem Rot'],
        'pests': ['Mealybug', 'Scale Insect', 'Fruit Borer', 'Tamarind Moth'],
        'varieties': ['PKM 1', 'Yercaud', 'DTS 1', 'Gulbarga Pride'],
        'growing_period': 'Perennial (30+ years)', 'seed_rate': '200-250 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'jackfruit': {
        'diseases': ['Fruit Rot', 'Leaf Spot', 'Stem Canker', 'Wilt'],
        'pests': ['Fruit Fly', 'Mealybug', 'Jack Shoot Borer', 'Scale Insect'],
        'varieties': ['Singapore', 'Mutton', 'Kenya', 'Varikkha', 'Rudrakshi'],
        'growing_period': 'Perennial (30+ years)', 'seed_rate': '200-250 plants/ha',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '60-80'}
    },
    'litchi': {
        'diseases': ['Anthracnose', 'Powdery Mildew', 'Leaf Spot', 'Fruit Rot'],
        'pests': ['Fruit Borer', 'Mite', 'Mealybug', 'Litchi Bug'],
        'varieties': ['Shahi', 'China', 'Bedana', 'Calcutta', 'Dehra Rose', 'Early Large Red'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '275-300 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'saffron': {
        'diseases': ['Corm Rot', 'Leaf Spot', 'Mosaic Virus', 'Root Rot'],
        'pests': ['Bulb Mite', 'Aphids', 'Nematodes'],
        'varieties': ['Kashmir Saffron', 'Mongra', 'Lacha', 'Zarda'],
        'growing_period': '90-120 days', 'seed_rate': '500-600 kg/ha (corms)',
        'npk': {'N': '30-40', 'P': '20-30', 'K': '20-30'}
    },
    'aloe_vera': {
        'diseases': ['Root Rot', 'Leaf Spot', 'Rust', 'Bacterial Soft Rot'],
        'pests': ['Whitefly', 'Mite', 'Mealybug'],
        'varieties': ['IC 111269', 'IC 111280', 'Edible Aloe', 'Curacoa'],
        'growing_period': 'Perennial (5-6 years)', 'seed_rate': '15000-20000 plants/ha',
        'npk': {'N': '30-40', 'P': '20-30', 'K': '30-40'}
    },
    'broccoli': {
        'diseases': ['Black Rot', 'Downy Mildew', 'Club Root', 'Alternaria Leaf Spot'],
        'pests': ['Diamondback Moth', 'Aphids', 'Cabbage Worm'],
        'varieties': ['Pusa KTS 1', 'Pusa Snowball', 'Ooty 1', 'Green Head', 'Premium Crop'],
        'growing_period': '60-80 days', 'seed_rate': '400-500 g/ha',
        'npk': {'N': '100-150', 'P': '50-60', 'K': '60-80'}
    },
    'cardamom': {
        'diseases': ['Clump Rot', 'Rhizome Rot', 'Leaf Spot', 'Mosaic Virus'],
        'pests': ['Cardamom Borer', 'Thrips', 'Scale Insect', 'Nematodes'],
        'varieties': ['IISR Avinash', 'IISR Sree', 'IISR Vijaya', 'IISR Revathy'],
        'growing_period': 'Perennial (10-15 years)', 'seed_rate': '2000-2500 clumps/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'clove': {
        'diseases': ['Leaf Spot', 'Die Back', 'Root Rot', 'Leaf Blight'],
        'pests': ['Clove Scale', 'Borers', 'Mite'],
        'varieties': ['Zanzibar', 'Ambon', 'Siputih', 'Sikotok'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '500-600 plants/ha',
        'npk': {'N': '60-80', 'P': '30-50', 'K': '40-60'}
    },
    'cocoa': {
        'diseases': ['Black Pod', 'Witches Broom', 'Frosty Pod Rot', 'Vascular Streak Dieback'],
        'pests': ['Mirid Bug', 'Cocoa Pod Borer', 'Mealybug', 'Thrips'],
        'varieties': ['Forastero', 'Criollo', 'Trinitario', 'DRC 1', 'DRC 2'],
        'growing_period': 'Perennial (30+ years)', 'seed_rate': '800-1100 plants/ha',
        'npk': {'N': '80-100', 'P': '40-60', 'K': '60-80'}
    },
    'rubber': {
        'diseases': ['Abnormal Leaf Fall', 'White Root Disease', 'Red Rot', 'Stem Canker'],
        'pests': ['Mite', 'Scale Insect', 'Mealybug', 'Termite'],
        'varieties': ['RRII 105', 'RRII 203', 'GT 1', 'PB 86', 'PB 235'],
        'growing_period': 'Perennial (30+ years)', 'seed_rate': '500-600 plants/ha',
        'npk': {'N': '80-100', 'P': '40-60', 'K': '60-80'}
    },
    'avocado': {
        'diseases': ['Phytophthora Root Rot', 'Powdery Mildew', 'Anthracnose', 'Scab'],
        'pests': ['Mite', 'Thrips', 'Mealybug', 'Fruit Fly'],
        'varieties': ['Fuerte', 'Hass', 'Pinkerton', 'Reed', 'Gwen'],
        'growing_period': 'Perennial (40+ years)', 'seed_rate': '250-300 plants/ha',
        'npk': {'N': '80-100', 'P': '40-50', 'K': '60-80'}
    },
    'fig': {
        'diseases': ['Fig Rust', 'Anthracnose', 'Canker', 'Leaf Spot'],
        'pests': ['Fig Borer', 'Mealybug', 'Fruit Fly', 'Nematodes'],
        'varieties': ['Poona Fig', 'Black Ischia', 'Dauphine', 'Brown Turkey', 'Excel'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '275-300 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '60-80'}
    },
    'pear': {
        'diseases': ['Pear Scab', 'Fire Blight', 'Powdery Mildew', 'Leaf Spot'],
        'pests': ['Pear Psylla', 'Codling Moth', 'Mite', 'Aphids'],
        'varieties': ['Bartlett', 'Conference', 'Nijisseiki', 'Patharnakh', 'China Pear'],
        'growing_period': 'Perennial (30+ years)', 'seed_rate': '400-500 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'apricot': {
        'diseases': ['Bacterial Canker', 'Brown Rot', 'Powdery Mildew', 'Leaf Spot'],
        'pests': ['Aphids', 'Codling Moth', 'Mite', 'Scale'],
        'varieties': ['New Castle', 'Royal', 'Kaisha', 'Kashmir Apricot', 'Halman'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '400-500 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'cherry': {
        'diseases': ['Brown Rot', 'Cherry Leaf Spot', 'Powdery Mildew', 'Bacterial Canker'],
        'pests': ['Cherry Fruit Fly', 'Aphids', 'Mite', 'Borers'],
        'varieties': ['Early Red', 'Bigarreau Noir', 'Merton Glory', 'Hedelfingen', 'Van'],
        'growing_period': 'Perennial (20+ years)', 'seed_rate': '400-500 plants/ha',
        'npk': {'N': '60-80', 'P': '40-60', 'K': '40-60'}
    },
    'chickoo': {
        'diseases': ['Leaf Spot', 'Powdery Mildew', 'Fruit Rot', 'Sooty Mould'],
        'pests': ['Chikoo Moth', 'Fruit Fly', 'Mealybug', 'Scale'],
        'varieties': ['Kali Patti', 'Cricket Ball', 'Kalipatti', 'Pala', 'Dwar']
    }
}


# Detailed growing process / cultivation steps for each crop
CROP_CULTIVATION = {
    'rice': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Puddle field thoroughly, apply FYM 10 t/ha, level properly | **Sowing:** Transplant 25-day seedlings at 20x15cm spacing, 2-3 seedlings/hill | **Water:** Maintain 5cm standing water; drain 2 weeks before harvest | **Harvest:** 110-150 days, when grains turn golden yellow, moisture <20%",
    'wheat': "**Sowing Time:** Oct-Dec (Rabi) | **Land Prep:** Deep plough + 2 harrowings, apply well-decomposed FYM | **Sowing:** Drill sowing at 4-5cm depth, row spacing 22.5cm, seed 100-125 kg/ha | **Water:** 4-6 irrigations at crown root, tillering, flowering, grain filling stages | **Harvest:** 110-150 days, when stalks turn golden, moisture <14%",
    'maize': "**Sowing Time:** Jun-Jul (Kharif) / Oct-Nov (Rabi) | **Land Prep:** Plough + harrow, apply FYM 5-10 t/ha | **Sowing:** Ridge sowing at 60x25cm spacing, 2 seeds/hole, thin to 1 | **Water:** Light irrigation after sowing; critical at tasseling, silking, grain filling | **Harvest:** 90-110 days, when husk turns brown, grains hard with <20% moisture",
    'ragi': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Plough 2-3 times, incorporate FYM 10 t/ha | **Sowing:** Broadcast or line sow at 25x10cm spacing, seed rate 8-10 kg/ha | **Water:** Rainfed mostly; irrigate at tillering, earhead emergence if dry | **Harvest:** 110-120 days, when earheads turn golden brown",
    'millets': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Plough once, harrow twice, no fine tilth needed | **Sowing:** Line sowing at 45x15cm spacing, seed rate 4-5 kg/ha | **Water:** Mostly rainfed; 1-2 irrigations at flowering if dry | **Harvest:** 80-90 days, when grains harden and heads bend",
    'potato': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Deep plough + ridge making, apply FYM 25 t/ha | **Sowing:** Plant whole/sprouted tubers at 60x20cm spacing, 4-5cm deep | **Water:** Light but frequent irrigation; critical at tuber initiation, bulking | **Harvest:** 90-100 days, when vines senesce, skin sets",
    'tomato': "**Sowing Time:** Oct-Nov (Rabi) / Jun-Jul (Kharif) | **Land Prep:** Deep plough + FYM 20 t/ha, raised beds | **Sowing:** Transplant 25-30 day seedlings at 75x60cm spacing | **Water:** Drip irrigation ideal; regular moisture at flowering, fruit set | **Harvest:** 100-120 days, when fruits turn red but firm",
    'onion': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Fine tilth with FYM 20 t/ha, raised beds | **Sowing:** Transplant 6-8 week seedlings at 15x10cm spacing | **Water:** Light irrigation weekly; stop 2 weeks before harvest | **Harvest:** 120-150 days, when tops fall over, necks soften",
    'brinjal': "**Sowing Time:** Jun-Jul (Kharif) / Oct-Nov (Rabi) | **Land Prep:** Plough + FYM 25 t/ha, beds or ridges | **Sowing:** Transplant 6-8 week seedlings at 75x60cm spacing | **Water:** Weekly irrigation; critical at flowering, fruit development | **Harvest:** 120-150 days from seed; pick fruits when glossy, before seeds harden",
    'cabbage': "**Sowing Time:** Sep-Oct (Rabi) | **Land Prep:** Fine tilth + FYM 25 t/ha, raised beds | **Sowing:** Transplant 4-6 week seedlings at 45x45cm spacing | **Water:** Regular irrigation; keep soil moist during head formation | **Harvest:** 90-120 days, when heads are firm and compact",
    'cauliflower': "**Sowing Time:** Sep-Oct (Rabi) | **Land Prep:** Well-drained beds + FYM 25 t/ha | **Sowing:** Transplant 4-5 week seedlings at 60x45cm spacing | **Water:** Weekly irrigation; critical at curd initiation, development | **Harvest:** 80-130 days, when curds are compact and white",
    'carrot': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Deep plough + fine tilth, loose soil without clods | **Sowing:** Direct line sowing at 30x8cm spacing, 5-6 kg seed/ha | **Water:** Light irrigation every 5-7 days; avoid waterlogging | **Harvest:** 90-120 days, when roots attain proper size and colour",
    'radish': "**Sowing Time:** Sep-Oct (Rabi) | **Land Prep:** Loose friable soil + FYM 10 t/ha | **Sowing:** Direct sowing on ridges at 30x10cm spacing, 8-10 kg seed/ha | **Water:** Light irrigation weekly | **Harvest:** 50-60 days, when roots are tender and pencil-thick",
    'beans': "**Sowing Time:** Jun-Jul (Kharif) / Feb-Mar (Spring) | **Land Prep:** Plough + harrow, FYM 10 t/ha | **Sowing:** Line sowing at 45x15cm spacing, 50-60 kg seed/ha | **Water:** Light irrigation at flowering, pod filling | **Harvest:** 80-120 days, pick green pods before seeds bulge",
    'peas': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Well-drained loam + FYM 15 t/ha | **Sowing:** Line sowing at 30x10cm spacing, 80-100 kg seed/ha | **Water:** 2-3 irrigations at branching, flowering, pod filling | **Harvest:** 90-130 days, when pods are green and well-filled",
    'lentil': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + 2 harrowings, no nitrogen fertilizer needed | **Sowing:** Line sowing at 30cm spacing, 30-35 kg seed/ha, 4-5cm deep | **Water:** 1-2 irrigations if dry; sensitive to waterlogging | **Harvest:** 100-120 days, when pods turn brown and rattle",
    'chickpea': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + harrow, apply FYM 10 t/ha | **Sowing:** Line sowing at 30x10cm spacing, 75-100 kg seed/ha | **Water:** 1-2 irrigations at branching & pod filling; avoid excess | **Harvest:** 100-130 days, when pods turn yellow-brown",
    'blackgram': "**Sowing Time:** Jun-Jul (Kharif) / Feb-Mar (Spring) | **Land Prep:** Plough + harrow, no heavy fertilization | **Sowing:** Line sowing at 30x10cm spacing, 15-20 kg seed/ha | **Water:** Mostly rainfed; 1-2 irrigations if prolonged dry spell | **Harvest:** 70-90 days, when pods turn black, harvest before shattering",
    'greengram': "**Sowing Time:** Jun-Jul (Kharif) / Feb-Mar (Spring) | **Land Prep:** Plough + 2 harrowings | **Sowing:** Line sowing at 30x10cm spacing, 12-15 kg seed/ha | **Water:** Rainfed; light irrigation at flowering if dry | **Harvest:** 60-70 days, when pods turn black, pick in 2-3 rounds",
    'horsegram': "**Sowing Time:** Jul-Aug (Kharif) | **Land Prep:** Minimum tillage, grows in poor soils | **Sowing:** Broadcast or line sow at 30cm, 20-25 kg seed/ha | **Water:** Fully rainfed, drought-tolerant crop | **Harvest:** 90-120 days, when pods turn brown and dry",
    'mothbeans': "**Sowing Time:** Jul-Aug (Kharif) | **Land Prep:** Plough once, grows well in sandy soils | **Sowing:** Broadcast at 15-20 kg seed/ha | **Water:** Rainfed; extremely drought-tolerant | **Harvest:** 70-90 days, when pods mature unevenly, pick selectively",
    'pigeonpea': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Deep plough + 2 harrowings | **Sowing:** Line sowing at 75x30cm spacing, 12-15 kg seed/ha | **Water:** Rainfed; irrigate at flowering if dry | **Harvest:** 140-180 days, when 75% pods turn brown, harvest in stages",
    'cotton': "**Sowing Time:** May-Jun (Kharif) | **Land Prep:** Deep plough + FYM 10 t/ha, ridges | **Sowing:** Line sowing at 90x60cm spacing (hybrid), 5-7 kg seed/ha | **Water:** Critical at flowering, boll development; 6-8 irrigations | **Harvest:** 150-180 days, when bolls burst, pick in 4-5 rounds",
    'jute': "**Sowing Time:** Apr-May (Pre-Kharif) | **Land Prep:** Fine tilth + FYM 10 t/ha | **Sowing:** Broadcast or line sow at 30cm, 8-10 kg seed/ha | **Water:** Light irrigation at seedling stage; rainfed rest | **Harvest:** 120-150 days, when flowering starts, cut and ret in water",
    'sugarcane': "**Sowing Time:** Jan-Mar (Spring) / Sep-Oct (Autumn) | **Land Prep:** Deep plough + ridges, apply FYM 25 t/ha | **Sowing:** Plant setts (3-bud) in furrows at 90cm spacing | **Water:** 1-2 weeks interval; critical at tillering, grand growth, ripening | **Harvest:** 10-14 months, when juice brix >16, bottom leaves dry",
    'banana': "**Sowing Time:** Jun-Oct (Year-round in tropics) | **Land Prep:** Deep pits 60x60x60cm, fill with FYM 10 kg + soil | **Sowing:** Plant suckers/tissue-culture at 2x2m spacing | **Water:** Drip irrigation ideal; 20-25L/day/plant | **Harvest:** 11-14 months, when fruits plump, ridges smooth, colour changes",
    'mango': "**Sowing Time:** Jul-Sep (Monsoon) | **Land Prep:** Pits 1x1x1m, fill with FYM 20kg + topsoil | **Sowing:** Plant grafted saplings at 8x8m spacing | **Water:** Weekly for first 2 years; stop 2 months before flowering | **Harvest:** 4-5 years to fruit, pick when shoulder rises, colour breaks",
    'apple': "**Sowing Time:** Jan-Feb (Dormant season) | **Land Prep:** Pits 1x1x1m, fill with FYM + soil, need cold climate | **Sowing:** Plant 2-year grafted saplings at 4x4m spacing | **Water:** Regular irrigation; critical at fruit set, cell division | **Harvest:** 4-5 years to fruit; pick when seeds turn brown, background colour changes",
    'orange': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 60x60x60cm, fill with FYM 10kg + topsoil | **Sowing:** Plant grafted saplings at 5x5m spacing | **Water:** Weekly; critical at flowering, fruit set, fruit development | **Harvest:** 3-4 years to fruit; pick when colour changes 70-80%",
    'grapes': "**Sowing Time:** Jan-Feb (Spring) | **Land Prep:** Deep pits, trellis/bower system, apply FYM 20 t/ha | **Sowing:** Plant cuttings at 3x3m spacing on bower | **Water:** Drip irrigation; stress after harvest, irrigate at bud burst | **Harvest:** 8-12 months (prune for 2 crops); pick at 18-22°Brix",
    'guava': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 60x60x60cm, FYM 10kg + SSP 200g | **Sowing:** Plant saplings at 6x6m spacing | **Water:** Weekly; critical at flowering, fruit development | **Harvest:** 2-3 years to fruit; pick when colour turns light green-yellow",
    'pomegranate': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 60x60x60cm, well-drained soil | **Sowing:** Plant saplings at 4.5x4.5m spacing | **Water:** Drip irrigation; stress 30 days before flowering for better yield | **Harvest:** 2-3 years; pick when skin turns reddish-yellow, makes metallic sound",
    'papaya': "**Sowing Time:** Jun-Dec (Year-round) | **Land Prep:** Deep plough + FYM 10 t/ha, raised beds | **Sowing:** Transplant 2-month seedlings at 2x2m spacing, 1 female : 1 male | **Water:** Weekly; critical at flowering, fruit development | **Harvest:** 9-12 months; pick when 25% fruit turns yellow",
    'lemon': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 60x60x60cm, FYM 10kg + topsoil | **Sowing:** Plant grafted saplings at 5x5m spacing | **Water:** Weekly; irrigate during flowering, fruit set | **Harvest:** 3-4 years; pick when fully yellow, harvest in 4-5 rounds",
    'watermelon': "**Sowing Time:** Feb-Mar (Summer) / Jun-Jul (Kharif) | **Land Prep:** Sandy loam + FYM 10 t/ha, raised beds | **Sowing:** Direct sowing at 3x1.5m spacing, 2 seeds/hill | **Water:** Weekly; critical at flowering, fruit development, stop at ripening | **Harvest:** 80-100 days; thump test (dull sound), tendril dry, ground spot yellow",
    'cucumber': "**Sowing Time:** Feb-Mar (Summer) / Jun-Jul (Kharif) | **Land Prep:** Raised beds + FYM 15 t/ha | **Sowing:** Direct sowing at 1.5x1m spacing, 3-4 seeds/hill | **Water:** Regular irrigation; keep moist during fruit set | **Harvest:** 50-70 days; pick green, tender, before seeds mature",
    'pumpkin': "**Sowing Time:** Oct-Nov (Rabi) / Jan-Feb (Summer) | **Land Prep:** Pits 60x60x30cm, FYM 5kg/pit | **Sowing:** 3-4 seeds/pit at 2x2m spacing, thin to 2 plants | **Water:** Weekly; critical at flowering, fruit development | **Harvest:** 90-120 days; when skin hardens, stem corky, deep colour",
    'strawberry': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Raised beds + plastic mulch + drip, FYM 25 t/ha | **Sowing:** Plant runners at 30x30cm spacing on beds | **Water:** Drip irrigation daily; avoid overhead | **Harvest:** 60-90 days from planting; pick fully red fruit every 2-3 days",
    'coconut': "**Sowing Time:** Jun-Dec (Year-round) | **Land Prep:** Pits 1x1x1m, fill with topsoil + FYM | **Sowing:** Plant 1-year-old seedlings at 7.5x7.5m spacing | **Water:** Weekly in summer; drip irrigation 40L/palm/week | **Harvest:** 5-6 years to fruit; harvest every 45 days year-round",
    'coffee': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Shade management, deep pits 50x50x50cm | **Sowing:** Plant seedlings at 2.5x2.5m spacing under shade | **Water:** Mulching for moisture retention; irrigate in dry months | **Harvest:** 3-4 years; pick ripe red cherries, 2-3 rounds at 15-day intervals",
    'tea': "**Sowing Time:** Jun-Sep (Monsoon) | **Land Prep:** Terraces on slopes, dig pits 45x45x45cm | **Sowing:** Plant 1-year clonal cuttings at 1.5x1.5m spacing, 3 rows/bed | **Water:** Mulch to retain moisture; irrigate in dry months | **Harvest:** 3-4 years for first plucking; pluck 2 leaves + bud every 7-10 days",
    'cocoa': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 60x60x60cm under coconut/shade canopy | **Sowing:** Plant grafted seedlings at 3x3m spacing under partial shade | **Water:** Mulch + drip irrigation in dry months | **Harvest:** 3-4 years; harvest ripe yellow pods, extract beans, ferment 5-7 days",
    'rubber': "**Sowing Time:** Jun-Sep (Monsoon) | **Land Prep:** Terracing, pits 60x60x60cm on slopes | **Sowing:** Plant budded stumps at 6x3m spacing | **Water:** Mulching; drought protection in early years | **Harvest:** 6-7 years to tap; tap at 50% spiral, collect latex every 2-3 days",
    'cardamom': "**Sowing Time:** May-Jun (Pre-monsoon) | **Land Prep:** Shade management, pits 60x60x45cm under forest canopy | **Sowing:** Plant 1-year seedlings at 2x2m spacing, 50% shade | **Water:** Mulch + sprinkler in dry months; high humidity needed | **Harvest:** 2-3 years; pick ripe capsules when pale green, before splitting",
    'turmeric': "**Sowing Time:** Apr-Jun (Pre-kharif) | **Land Prep:** Deep plough + FYM 25 t/ha, raised beds | **Sowing:** Plant rhizome bits (40-50g) at 45x20cm spacing, 5-7cm deep | **Water:** Light irrigation weekly; critical at tillering, rhizome bulking | **Harvest:** 7-9 months, when leaves yellow and dry; cure in boiling water + dry",
    'ginger': "**Sowing Time:** Apr-May (Pre-kharif) | **Land Prep:** Deep plough + FYM 25 t/ha, raised beds | **Sowing:** Plant rhizome bits (20-30g) at 40x20cm spacing, 5cm deep | **Water:** Light irrigation; keep soil moist, drain excess | **Harvest:** 7-8 months, when leaves yellow; cured or fresh market",
    'sunflower': "**Sowing Time:** Jun-Jul (Kharif) / Jan-Feb (Spring) | **Land Prep:** Plough + harrow, FYM 10 t/ha | **Sowing:** Line sowing at 60x30cm spacing, 5-7 kg seed/ha | **Water:** Critical at flowering, seed filling; 3-4 irrigations | **Harvest:** 80-100 days, when back of head turns yellow-brown, seeds firm",
    'mustard': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + 2 harrowings + FYM 10 t/ha | **Sowing:** Line sowing at 45x10cm spacing, 4-5 kg seed/ha | **Water:** 1-2 irrigations at flowering, siliqua filling; sensitive to frost | **Harvest:** 90-130 days, when siliqua turn yellow-brown, thresh on floor",
    'groundnut': "**Sowing Time:** Jun-Jul (Kharif) / Jan-Feb (Summer) | **Land Prep:** Well-drained sandy loam + FYM 12 t/ha | **Sowing:** Line sowing at 30x10cm spacing, 100-120 kg shelled nuts/ha | **Water:** Critical at peg penetration, pod filling; 4-5 irrigations | **Harvest:** 110-140 days, when leaves yellow, inner shell has dark veins",
    'soybean': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Plough + harrow + FYM 10 t/ha | **Sowing:** Line sowing at 45x5cm spacing, 60-80 kg seed/ha | **Water:** Critical at flowering, pod filling; 3-4 irrigations if dry | **Harvest:** 90-120 days, when leaves fall, pods turn brown, beans rattle",
    'sesame': "**Sowing Time:** Jun-Jul (Kharif) / Feb-Mar (Spring) | **Land Prep:** Fine tilth + FYM 5 t/ha | **Sowing:** Line sowing at 30x10cm spacing, 4-5 kg seed/ha | **Water:** Sensitive to excess; 2-3 irrigations at flowering, capsule development | **Harvest:** 70-120 days, when lower capsules turn brown, cut and dry upside-down",
    'saffron': "**Sowing Time:** Jul-Aug (Summer) | **Land Prep:** Well-drained calcareous soil, beds 15cm high | **Sowing:** Plant corms at 20x10cm spacing, 10-15cm deep | **Water:** Rain during dormancy; stop in flower season | **Harvest:** Oct-Nov, pick red stigmas early morning, dry in shade",
    'castor': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Plough + harrow, grows in marginal soils | **Sowing:** Line sowing at 120x60cm spacing (hybrid), 8-10 kg seed/ha | **Water:** Rainfed; 1-2 irrigations at flowering if severe drought | **Harvest:** 180-270 days, when spikes turn brown, harvest in 4-5 rounds",
    'barley': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + 2 harrowings | **Sowing:** Line sowing at 22.5cm spacing, 100-125 kg seed/ha | **Water:** 2-3 irrigations at crown root, tillering, flowering | **Harvest:** 120-150 days, when ears bend, grains hard",
    'pear': "**Sowing Time:** Dec-Jan (Winter dormant) | **Land Prep:** Pits 1x1x1m + FYM 15kg + soil | **Sowing:** Plant grafted saplings at 4x4m spacing | **Water:** Weekly; critical at fruit set, development | **Harvest:** 4-5 years; pick when fruit separates easily from spur, seeds brown",
    'apricot': "**Sowing Time:** Dec-Jan (Winter dormant) | **Land Prep:** Pits 1x1x1m + FYM 15kg, well-drained loam | **Sowing:** Plant grafted saplings at 5x5m spacing | **Water:** Weekly; sensitive to excess moisture | **Harvest:** 3-4 years; pick when golden-orange, slightly soft, twist off",
    'litchi': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 1x1x1m + FYM 20kg + soil, needs humid climate | **Sowing:** Plant grafted saplings at 8x8m spacing | **Water:** Weekly; critical at flowering, fruit set, growth | **Harvest:** 4-5 years; pick whole cluster when fruits turn pink-red, skin bumpy",
    'jackfruit': "**Sowing Time:** Jun-Sep (Monsoon) | **Land Prep:** Pits 1x1x1m + FYM 20kg | **Sowing:** Plant saplings at 10x10m spacing | **Water:** Weekly for first 2 years | **Harvest:** 3-4 years; pick when fruit develops dull thud sound and emits strong smell",
    'avocado': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 1x1x1m + FYM 15kg, well-drained | **Sowing:** Plant grafted saplings at 6x6m spacing | **Water:** Weekly; critical during flowering, fruit set | **Harvest:** 3-4 years; pick when skin colour changes, fruit yields to gentle pressure",
    'fig': "**Sowing Time:** Jan-Feb (Winter) | **Land Prep:** Pits 60x60x60cm + FYM 10kg | **Sowing:** Plant cuttings at 5x5m spacing | **Water:** Weekly; reduce during ripening | **Harvest:** 2-3 years; pick when fruit droops, neck bends, skin colour changes",
    'tamarind': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 1x1x1m + FYM 10kg | **Sowing:** Plant grafted saplings at 10x10m spacing | **Water:** Weekly for first 2 years; drought-tolerant after | **Harvest:** 5-7 years; harvest ripe pods when shell turns brown, brittle",
    'fennel': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + FYM 10 t/ha, well-drained | **Sowing:** Line sowing at 45x20cm spacing, 8-10 kg seed/ha | **Water:** 2-3 irrigations at flowering, seed formation | **Harvest:** 200-220 days, when seeds turn greenish-brown, umbels cut and dried",
    'fenugreek': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Fine tilth + FYM 10 t/ha | **Sowing:** Line sowing at 25x10cm spacing, 20-25 kg seed/ha | **Water:** 2-3 irrigations; leafy stage, pod formation | **Harvest:** 120-150 days (seed) / 25-30 days (leaves); pull whole plant for seed",
    'cumin': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Fine tilth + FYM 8 t/ha, well-drained | **Sowing:** Line sowing at 45x15cm spacing, 5-6 kg seed/ha | **Water:** 2 irrigations at flowering, seed formation; sensitive to frost | **Harvest:** 130-150 days, when plants turn yellow-brown, umbels cut and threshed",
    'coriander': "**Sowing Time:** Oct-Nov (Rabi) / Jun-Jul (Kharif) | **Land Prep:** Plough + FYM 10 t/ha, fine tilth | **Sowing:** Line sowing at 30x10cm spacing, 10-12 kg seed/ha | **Water:** Light irrigation weekly; stop when seeds mature | **Harvest:** 90-120 days (seed) / 25-30 days (leaves); cut at base for leaf, umbel turns brown for seed",
    'spices': "**Sowing Time:** Varies by spice type | **Land Prep:** Well-drained fertile soil + FYM | **Sowing:** Follow specific spacing for each spice | **Water:** Moderate irrigation; avoid waterlogging | **Harvest:** Varies by spice type",
    'coriander_leaf': "**Sowing Time:** Year-round in mild climate | **Land Prep:** Fine tilth + FYM 10 t/ha, raised beds | **Sowing:** Broadcast or line sow at 30cm, 15-20 kg seed/ha | **Water:** Frequent light irrigation for tender leaves | **Harvest:** 25-35 days, cut leaves 3-4cm above ground",
    'mint': "**Sowing Time:** Feb-Mar (Spring) / Jul-Aug (Kharif) | **Land Prep:** Fine tilth + FYM 20 t/ha, well-drained beds | **Sowing:** Plant rooted runners at 45x15cm spacing | **Water:** Weekly; keep soil consistently moist | **Harvest:** 70-80 days; cut 5cm above ground, regrows for 2-3 cuts",
    'spinach': "**Sowing Time:** Sep-Oct (Rabi) / Feb-Mar (Spring) | **Land Prep:** Fine tilth + FYM 15 t/ha | **Sowing:** Broadcast at 25-30 kg seed/ha | **Water:** Light irrigation weekly | **Harvest:** 25-40 days; cut leaves when 4-5 true leaves appear, regrows",
    'okra': "**Sowing Time:** Jun-Jul (Kharif) / Feb-Mar (Spring) | **Land Prep:** Plough + FYM 15 t/ha, raised beds | **Sowing:** Direct sowing at 60x30cm spacing, 8-10 kg seed/ha | **Water:** Weekly; critical at flowering, pod development | **Harvest:** 55-70 days; pick tender pods 6-8cm every 2-3 days",
    'sweetpotato': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Raised ridges + FYM 10 t/ha | **Sowing:** Plant vine cuttings (30cm) at 60x20cm spacing on ridges | **Water:** Light irrigation weekly; stop 15 days before harvest | **Harvest:** 100-120 days, when leaves yellow, soil cracks near vines",
    'yam': "**Sowing Time:** Apr-Jun (Pre-kharif) | **Land Prep:** Deep pits 60x60x60cm + FYM 10kg, mounds | **Sowing:** Plant small whole tubers/minisetts at 90x90cm spacing | **Water:** Regular; critical during vine growth, tuber bulking | **Harvest:** 8-10 months, when vines senesce, carefully dig tubers",
    'beetroot': "**Sowing Time:** Sep-Oct (Rabi) / Jan-Feb (Spring) | **Land Prep:** Loose friable soil + FYM 15 t/ha | **Sowing:** Direct sowing at 45x10cm spacing, 8-10 kg seed/ha | **Water:** Weekly; keep soil moist for uniform root development | **Harvest:** 90-120 days, when roots 5-7cm diameter, tender and sweet",
    'capsicum': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Green house/shade net + FYM 25 t/ha | **Sowing:** Transplant 5-6 week seedlings at 60x45cm spacing | **Water:** Drip irrigation; keep soil evenly moist | **Harvest:** 70-90 days from transplant; pick green or coloured firm fruits",
    'chickoo': "**Sowing Time:** Jun-Aug (Monsoon) | **Land Prep:** Pits 1x1x1m + FYM 10kg | **Sowing:** Plant grafted saplings at 8x8m spacing | **Water:** Weekly for first 2 years; drought-tolerant after | **Harvest:** 4-5 years; pick when fruit turns brownish, slightly soft, remove astringency",
    'aloe_vera': "**Sowing Time:** Feb-Mar (Spring) / Jun-Jul (Kharif) | **Land Prep:** Sandy loam + FYM 10 t/ha, raised beds | **Sowing:** Plant root suckers at 50x40cm spacing | **Water:** Minimal; drought-tolerant, avoid waterlogging | **Harvest:** 8-12 months; harvest lower mature leaves, leaves regrow",
    'sweet_corn': "**Sowing Time:** Jun-Jul (Kharif) / Oct-Nov (Rabi) | **Land Prep:** Plough + harrow + FYM 10 t/ha | **Sowing:** Line sowing at 60x20cm spacing, 2 seeds/hole, thin to 1 | **Water:** Critical at tasseling, silking; 4-5 irrigations | **Harvest:** 75-90 days; pick when silks turn brown, kernels exude milky juice",
    'baby_corn': "**Sowing Time:** Jun-Jul (Kharif) / Oct-Nov (Rabi) | **Land Prep:** Plough + harrow + FYM 10 t/ha | **Sowing:** Line sowing at 45x15cm spacing, high density (80k plants/ha) | **Water:** Light frequent irrigation | **Harvest:** 55-65 days; pick 2-3 days after silk emergence, before fertilisation",
    'palak': "**Sowing Time:** Sep-Oct (Rabi) / Feb-Mar (Spring) | **Land Prep:** Fine tilth + FYM 10 t/ha | **Sowing:** Broadcast at 20-25 kg seed/ha | **Water:** Light irrigation weekly; keep soil moist | **Harvest:** 25-30 days; uproot whole plant or cut tender leaves",
    'arsenic': "**Sowing Time:** N/A | **Land Prep:** N/A | **Sowing:** N/A | **Water:** N/A | **Harvest:** N/A",
    'toor_dal': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Plough + 2 harrowings | **Sowing:** Line sowing at 75x30cm, 12-15 kg seed/ha | **Water:** Rainfed; irrigate at flowering if dry | **Harvest:** 140-180 days, when 75% pods turn brown",
    'masoor_dal': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + 2 harrowings | **Sowing:** Line sowing at 30cm spacing, 30-35 kg seed/ha | **Water:** 1-2 irrigations if dry | **Harvest:** 100-120 days, when pods turn brown",
    'moong_dal': "**Sowing Time:** Jun-Jul (Kharif) / Feb-Mar (Spring) | **Land Prep:** Plough + 2 harrowings | **Sowing:** Line sowing at 30x10cm, 12-15 kg seed/ha | **Water:** Rainfed; light irrigation at flowering if dry | **Harvest:** 60-70 days, when pods turn black, pick in 2-3 rounds",
    'sabut_masoor': "**Sowing Time:** Oct-Nov (Rabi) | **Land Prep:** Plough + 2 harrowings | **Sowing:** Line sowing at 30cm, 30-35 kg seed/ha | **Water:** 1-2 irrigations if dry | **Harvest:** 100-120 days, when pods turn brown",
    'soyabean': "**Sowing Time:** Jun-Jul (Kharif) | **Land Prep:** Plough + harrow + FYM 10 t/ha | **Sowing:** Line sowing at 45x5cm, 60-80 kg seed/ha | **Water:** Critical at flowering, pod filling; 3-4 irrigations if dry | **Harvest:** 90-120 days, when leaves fall, pods turn brown",
}


def get_crop_details(crop_name):
    """Get detailed information for a crop, with fallbacks for missing data."""
    return CROP_DETAILED.get(crop_name, {
        'diseases': [],
        'pests': [],
        'varieties': [],
        'growing_period': None,
        'seed_rate': None,
        'npk': {}
    })


def get_crop_diseases_info(crop_name, crop_info):
    """Format disease information for a crop."""
    details = get_crop_details(crop_name)
    diseases = details['diseases']
    if not diseases:
        return None
    disease_list = "\n".join(f"• {d}" for d in diseases)
    return (
        f"{crop_info.get('icon', '🌾')} **{crop_name.title()} - Diseases**\n\n"
        f"Common diseases affecting {crop_name.title()}:\n{disease_list}\n\n"
        "💡 **Prevention:** Use disease-resistant varieties, practice crop rotation, "
        "maintain proper spacing, and apply recommended fungicides at early stages."
    )


def get_crop_pests_info(crop_name, crop_info):
    """Format pest information for a crop."""
    details = get_crop_details(crop_name)
    pests = details['pests']
    if not pests:
        return None
    pest_list = "\n".join(f"• {p}" for p in pests)
    return (
        f"{crop_info.get('icon', '🌾')} **{crop_name.title()} - Pests**\n\n"
        f"Common pests affecting {crop_name.title()}:\n{pest_list}\n\n"
        "💡 **Control:** Use integrated pest management (IPM), biological controls, "
        "and judicious use of pesticides at threshold levels."
    )


def get_crop_varieties_info(crop_name, crop_info):
    """Format variety information for a crop."""
    details = get_crop_details(crop_name)
    varieties = details['varieties']
    if not varieties:
        return None
    var_list = "\n".join(f"• {v}" for v in varieties)
    return (
        f"{crop_info.get('icon', '🌾')} **{crop_name.title()} - Varieties**\n\n"
        f"Popular varieties of {crop_name.title()}:\n{var_list}\n\n"
        "💡 Choose varieties based on your climate, soil type, and market demand."
    )


def get_crop_growing_info(crop_name, crop_info):
    """Format growing period, seed rate, and step-by-step cultivation process."""
    details = get_crop_details(crop_name)
    period = details.get('growing_period')
    seed_rate = details.get('seed_rate')
    if not period and not seed_rate:
        return None
    parts = [f"🌱 **{crop_name.title()} - Growing Information**\n"]
    if period:
        parts.append(f"\n📅 **Growing Period:** {period}")
    if seed_rate:
        parts.append(f"\n🌰 **Seed Rate:** {seed_rate}")
    if crop_info.get('season'):
        parts.append(f"\n📆 **Season:** {crop_info.get('season')}")

    # Add cultivation process if available
    cultivation = CROP_CULTIVATION.get(crop_name)
    if cultivation:
        parts.append("\n\n🌾 **How to Grow:**")
        for step in cultivation.split('|'):
            step = step.strip()
            if step:
                parts.append(f"\n• {step}")
    else:
        parts.append("\n\n💡 Proper timing of sowing is crucial for optimal yields.")
    return "".join(parts)


def get_crop_npk_info(crop_name, crop_info):
    """Format NPK requirement information."""
    details = get_crop_details(crop_name)
    npk = details.get('npk', {})
    if not npk:
        return None
    fert = crop_info.get('fert', 'Standard fertilizer')
    return (
        f"🧪 **{crop_name.title()} - NPK Requirements**\n\n"
        f"📊 **Recommended Fertilizer:** {fert}\n\n"
        f"**Nutrient Requirements:**\n"
        f"🟢 **Nitrogen (N):** {npk.get('N', 'N/A')} kg/ha\n"
        f"🔵 **Phosphorus (P):** {npk.get('P', 'N/A')} kg/ha\n"
        f"🔴 **Potassium (K):** {npk.get('K', 'N/A')} kg/ha\n\n"
        "💡 Apply fertilizers based on soil test recommendations for best results."
    )
