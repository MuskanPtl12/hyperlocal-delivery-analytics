"""
    Identify the product sub-category based on keywords
    present in the product name.
    """

SUBCATEGORY_KEYWORDS = {
"Flour": [
    "whole wheat atta",
    "atta",
    "maida",
    "besan",
    "suji",
    "rava",
    "semolina",
    "flour"
    ],

"Rice": [
    "brown rice",
    "basmati",
    "sona masoori",
    "kolam",
    "rice"
    ],

"Pulses": [
    "dal",
    "lentil",
    "chana",
    "moong",
    "urad",
    "toor",
    "masoor",
    "rajma",
    "pulse",
    "pulses",
    ],

"Edible Oil": [
    "sunflower oil",
    "mustard oil",
    "groundnut oil",
    "olive oil",
    "coconut oil",
    "soybean oil",
    "oil"
    ],

"Sugar": [
    "brown sugar",
    "sugar",
    "jaggery",
    "honey",
    ],

"Salt": [
    "rock salt",
    "sendha",
    "salt",
    "namak"
    ],

"Spices": [
    "garam masala",
    "red chilli",
    "turmeric",
    "haldi",
    "chilli",
    "coriander",
    "dhania",
    "jeera",
    "cumin",
    "pepper",
    "magic masala",
    "masala","mdh", "deggi", "deggi mirch","baking powder",
    ],

"Baby Food": ["baby food"],

"Sauces & Spreads" : [
   "ketchup", "tomato ketchup" ,"schezwan", "chutney"
],

"Dry Fruits": [
    "dry fruit",
    "almonds",
    "cashew",
    "raisin",
    "pista",
    "walnut",
    "nuts"
    ],
        
# ============================================================
# Fruits & Vegetables
# ============================================================

"Fruits": [

    # Common Fruits
    "apple", "apples",
    "banana", "bananas",
    "mango", "mangoes",
    "orange", "oranges",
    "grape", "grapes",
    "watermelon",
    "muskmelon",
    "papaya",
    "pineapple",
    "guava",
    "kiwi",
    "pear",
    "peach",
    "plum",
    "pomegranate",
    "dragon fruit",
    "strawberry",
    "blueberry",
    "raspberry",
    "blackberry",
    "cherry",
    "litchi",
    "lychee",
    "coconut",
    "sweet lime",
    "mosambi",
    "avocado",
    "custard apple",
    "sitaphal",
    "jamun",
    "fig",
    "anjir","lemon", "lemons","kiwifruit", "zespri",
],


"Vegetables": [

    # Leafy
    "spinach",
    "palak",
    "lettuce",
    "cabbage",
    "cauliflower",
    "broccoli",

    # Root Vegetables
    "potato", "potatoes",
    "onion", "onions",
    "tomato", "tomatoes",
    "carrot", "carrots",
    "beetroot",
    "radish",
    "turnip",
    "ginger",
    "garlic",

    # Other Vegetables
    "brinjal",
    "eggplant",
    "capsicum",
    "bell pepper",
    "chilli",
    "green chilli",
    "cucumber",
    "bottle gourd",
    "lauki",
    "ridge gourd",
    "turai",
    "bitter gourd",
    "karela",
    "pumpkin",
    "ash gourd",
    "okra",
    "lady finger",
    "bhindi",
    "peas",
    "green peas",
    "sweet corn",
    "corn",
    "mushroom",
    "zucchini"
],


"Herbs": [

    "coriander",
    "coriander leaves",
    "cilantro",
    "mint",
    "mint leaves",
    "pudina",
    "curry leaves",
    "parsley",
    "basil",
    "thyme",
    "rosemary",
    "dill"
],

# ============================================================
# Dairy & Breakfast
# ============================================================

"Milk": [

    "milk",
    "toned milk",
    "full cream milk",
    "double toned milk",
    "skimmed milk",
    "cow milk",
    "buffalo milk",
    "a2 milk","amul kool", "flavoured milk", "flavored milk",
],


"Curd": [

    "curd",
    "dahi",
    "yogurt",
    "yoghurt",
    "greek yogurt",
    "greek yoghurt",
    "lassi",
    "chaas",
    "buttermilk"
],


"Butter & Ghee": [

    "butter",
    "salted butter",
    "unsalted butter",
    "ghee",
    "cow ghee",
    "desi ghee",
    "clarified butter"
],


"Cheese": [

    "cheese",
    "cheddar",
    "mozzarella",
    "parmesan",
    "cheese slice",
    "cheese cubes",
    "cheese spread",
    "cream cheese",
    "paneer"
],


"Bread": [

    "bread",
    "brown bread",
    "white bread",
    "whole wheat bread",
    "multigrain bread",
    "garlic bread",
    "burger bun",
    "buns",
    "pav"
],


"Eggs": [

    "egg",
    "eggs"
],


"Breakfast Cereals": [

    "corn flakes",
    "muesli",
    "oats",
    "rolled oats",
    "instant oats",
    "granola",
    "cereal",
    "breakfast cereal",
    "chocos",
    "flakes"
],

# ============================================================
# Snacks & Beverages
# ============================================================

"Biscuits": [

    "biscuit",
    "biscuits",
    "cookie",
    "cookies",
    "cracker",
    "crackers",
    "rusk",
    "toast","sunfeast", "dark fantasy",
],


"Chips": [

    "chips",
    "nachos",
    "popcorn",
    "makhana",
    "khakhra",
    "bhujia",
    "sev",
    "mixture",
    "namkeen","bingo", "mad angles","uncle chipps",
    "bhel","too yumm", "karare",
],


"Chocolates": [

    "chocolate",
    "chocolates",
    "candy",
    "candies",
    "toffee",
    "toffees",
    "wafer",
    "wafers",
    "bar",
    "cocoa","cadbury","dairy milk", "5 star",
    "perk","fuse","gems"
],


"Soft Drinks": [
    
    "cola",
    "soft drink",
    "soft drinks",
    "soda",
    "sparkling water",
    "energy drink",
    "sports drink",
    "tonic water",
    "drink",
    "drinks",
    "coca-cola", "coke", "sprite", "fanta", "thums up"
],


"Juices": [

    "juice",
    "juices",
    "fruit juice",
    "coconut water",
    "nectar",
    "lemonade"
],

"Tea": [

    "tea",
    "green tea",
    "black tea",
    "herbal tea",
    "masala tea",
    "tea bags"
],


"Coffee": [

    "coffee",
    "instant coffee",
    "filter coffee",
    "ground coffee",
    "coffee beans",
    "cold coffee"
],

# ============================================================
# Instant & Frozen Foods
# ============================================================

"Frozen Food": [

    "frozen",
    "frozen vegetables",
    "frozen peas",
    "frozen corn",
    "frozen fries",
    "frozen nuggets",
    "frozen paratha",
    "frozen pizza",
    "frozen kebab",
    "frozen momos",
    "frozen dessert",
    "ice cream","parota", "paratha","mccain", "smiles",
],


"Ready to Cook": [

    "ready to cook",
    "instant mix",
    "idli mix",
    "dosa mix",
    "upma mix",
    "poha mix",
    "cake mix",
    "gulab jamun mix",
    "pancake mix"
],


"Ready to Eat": [

    "ready to eat",
    "meal",
    "biryani",
    "pulao",
    "curry",
    "dal makhani",
    "rajma chawal",
    "khichdi"
],


"Instant Noodles": [

    "noodles",
    "instant noodles",
    "ramen",
    "pasta",
    "macaroni",
    "vermicelli",
    "sevai"
],


# ============================================================
# Personal Care
# ============================================================

"Soap & Body Wash": [

    "soap",
    "soaps",
    "body wash",
    "shower gel",
    "hand wash"
],


"Shampoo": [

    "shampoo",
    "conditioner",
    "hair cleanser"
],


"Hair Care": [

    "hair oil",
    "hair serum",
    "hair mask",
    "hair cream",
    "hair color",
    "hair gel",
    
],

"Deodorant" :[
    "deodorant", "deo",
],

"Skin Care": [

    "face wash",
    "face cream",
    "moisturizer",
    "lotion",
    "sunscreen",
    "sun cream",
    "serum",
    "scrub",
    "lip balm","hair removal cream", "veet","razor", "shaving"
],

"Feminine Hygiene": [
    "sanitary pad", "pads", "stayfree"
    ],

"Oral Care": [

    "toothpaste",
    "tooth brush",
    "toothbrush",
    "mouthwash",
    "dental floss"
],


"Baby Care": [

    "baby lotion",
    "baby soap",
    "baby shampoo",
    "baby powder",
    "baby oil",
    "baby wipes",
    "diaper",
    "diapers","huggies", "wonder pants"
],


# ============================================================
# Household
# ============================================================

"Detergent": [

    "detergent",
    "washing powder",
    "washing liquid",
    "laundry liquid",
    "fabric wash",
    "surf excel",
    "ariel matic",
    "tide","vanish", "stain remover",
],


"Dishwash": [

    "dishwash",
    "dish wash",
    "dish cleaner",
    "dishwashing liquid",
    "dishwashing bar"
],


"Floor Cleaner": [

    "floor cleaner",
    "floor disinfectant",
    "surface cleaner", "glass cleaner", "colin",
],


"Toilet Cleaner": [

    "toilet cleaner",
    "toilet freshener",
    "bathroom cleaner"
],


"Garbage Bags": [

    "garbage bag",
    "garbage bags",
    "trash bag",
    "dustbin bag"
],

"Batteries": [
    "battery", "batteries", "aa battery", "duracell" ,
    ],

"Air Fresheners": [

    "air freshener",
    "room freshener",
    "air spray"
],


"Paper Products": [

    "tissue",
    "tissues",
    "toilet paper",
    "paper towel",
    "kitchen towel",
    "napkin",
    "napkins",
    "aluminium foil",
    "aluminum foil",
    "cling film",
    "plastic wrap"
],

"Insect Repellent" : [
    "good knight", "mosquito", 
    "mosquito repellent","all out",
    "refill" ,"baygon", "insect killer",
    ],


# ============================================================
# Pharmacy & Wellness
# ============================================================

"Pharmacy & Wellness": [

    "medicine",
    "tablet",
    "capsule",
    "syrup",
    "ointment",
    "pain relief",
    "bandage",
    "cotton",
    "thermometer",
    "antiseptic",
    "sanitizer",
    "hand sanitizer",
    "mask",
    "vitamin",
    "protein powder",
    "electrolyte",
    "pain reliever",
    "vitamins"
],


# ============================================================
# Pet Care
# ============================================================

"Pet Care": [

    "dog food",
    "cat food",
    "pet food",
    "dog treat",
    "cat treat",
    "pet shampoo",
    "pet litter",
    "cat litter",
    "pet toy",
    "pet treats"
    
],
    }



# ============================================================
# Category Mapping
# ============================================================

CATEGORY_MAPPING = {

    # Fruits & Vegetables
    "Fruits": "Fruits & Vegetables",
    "Vegetables": "Fruits & Vegetables",
    "Herbs": "Fruits & Vegetables",

    # Grocery & Staples
    "Rice": "Grocery & Staples",
    "Flour": "Grocery & Staples",
    "Pulses": "Grocery & Staples",
    "Edible Oil": "Grocery & Staples",
    "Sugar": "Grocery & Staples",
    "Salt": "Grocery & Staples",
    "Spices": "Grocery & Staples",
    "Dry Fruits": "Grocery & Staples",
    "Baby Food" : "Grocery & Staples",
    "Sauces & Spreads" : "Grocery & Staples",
    
    # Dairy & Breakfast
    "Milk": "Dairy & Breakfast",
    "Curd": "Dairy & Breakfast",
    "Butter & Ghee": "Dairy & Breakfast",
    "Cheese": "Dairy & Breakfast",
    "Bread": "Dairy & Breakfast",
    "Eggs": "Dairy & Breakfast",
    "Breakfast Cereals": "Dairy & Breakfast",

    # Snacks & Beverages
    "Biscuits": "Snacks & Beverages",
    "Chips": "Snacks & Beverages",
    "Chocolates": "Snacks & Beverages",
    "Soft Drinks": "Snacks & Beverages",
    "Juices": "Snacks & Beverages",
    "Tea": "Snacks & Beverages",
    "Coffee": "Snacks & Beverages",

    # Instant & Frozen Foods
    "Frozen Food": "Instant & Frozen Foods",
    "Ready to Cook": "Instant & Frozen Foods",
    "Ready to Eat": "Instant & Frozen Foods",
    "Instant Noodles": "Instant & Frozen Foods",

    # Personal Care
    "Soap & Body Wash": "Personal Care",
    "Shampoo": "Personal Care",
    "Hair Care": "Personal Care",
    "Skin Care": "Personal Care",
    "Oral Care": "Personal Care",
    "Baby Care": "Personal Care",
    "Feminine Hygiene" : "Personal Care",
    "Deodorant": "Personal Care",

    # Household
    "Detergent": "Household",
    "Dishwash": "Household",
    "Floor Cleaner": "Household",
    "Toilet Cleaner": "Household",
    "Garbage Bags": "Household",
    "Air Fresheners": "Household",
    "Paper Products": "Household",
    "Insect Repellent" : "Household",
    "Batteries" :"Household",

    # Pharmacy & Wellness
    "Pharmacy & Wellness": "Pharmacy & Wellness",

    # Pet Care
    "Pet Care": "Pet Care"
}