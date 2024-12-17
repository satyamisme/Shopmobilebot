import { utils, writeFile } from 'xlsx';
import { mkdirSync, existsSync } from 'fs';

// Ensure data directory exists
if (!existsSync('data')) {
  mkdirSync('data');
}

// Sample data configurations
const brands = ['iPhone', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'OPPO', 'Vivo'];
const models = {
  'iPhone': ['13 Pro Max', '13 Pro', '13', '12 Pro Max', '12 Pro', '12', '11 Pro Max', '11 Pro', '11'],
  'Samsung': ['S23 Ultra', 'S23+', 'S23', 'S22 Ultra', 'S22+', 'S22', 'A73', 'A53'],
  'Google': ['Pixel 7 Pro', 'Pixel 7', 'Pixel 6 Pro', 'Pixel 6', 'Pixel 6a'],
  'OnePlus': ['11', '10 Pro', '10T', '9 Pro', '9', 'Nord 3'],
  'Xiaomi': ['13 Pro', '13', '12 Pro', '12', 'Poco F5', 'Redmi Note 12 Pro'],
  'OPPO': ['Find X6 Pro', 'Find X6', 'Reno 8 Pro', 'Reno 8'],
  'Vivo': ['X90 Pro', 'X90', 'V27 Pro', 'V27']
};

const ramOptions = ['4GB', '6GB', '8GB', '12GB', '16GB'];
const storageOptions = ['64GB', '128GB', '256GB', '512GB', '1TB'];
const networkOptions = ['4G', '5G'];
const colors = ['Black', 'White', 'Gold', 'Silver', 'Blue', 'Red', 'Purple', 'Green'];
const conditions = ['New', 'Like New', 'Used', 'Refurbished'];
const processors = {
  'iPhone': ['A16 Bionic', 'A15 Bionic', 'A14 Bionic'],
  'Samsung': ['Snapdragon 8 Gen 2', 'Snapdragon 8 Gen 1', 'Exynos 2200'],
  'Google': ['Google Tensor G2', 'Google Tensor'],
  'OnePlus': ['Snapdragon 8 Gen 2', 'Snapdragon 8 Gen 1'],
  'Xiaomi': ['Snapdragon 8 Gen 2', 'Snapdragon 8 Gen 1'],
  'OPPO': ['Snapdragon 8 Gen 2', 'Dimensity 9000'],
  'Vivo': ['Snapdragon 8 Gen 2', 'Dimensity 9000']
};

// Generate sample data
const products = [];
let id = 1;

brands.forEach(brand => {
  models[brand].forEach(model => {
    ramOptions.forEach(ram => {
      storageOptions.forEach(storage => {
        // Not all combinations make sense, so add some constraints
        if ((parseInt(ram) <= parseInt(storage)) && 
            (parseInt(storage) >= parseInt(ram) * 8)) {
          
          const basePrice = Math.floor(Math.random() * (1500 - 300) + 300);
          const isNewModel = model.includes('13') || model.includes('23') || model.includes('7');
          
          products.push({
            'ID': id++,
            'Brand': brand,
            'Model': `${brand} ${model}`,
            'RAM': ram,
            'Storage': storage,
            'Network': isNewModel ? '5G' : networkOptions[Math.floor(Math.random() * networkOptions.length)],
            'Processor': processors[brand][Math.floor(Math.random() * processors[brand].length)],
            'Display': getDisplaySpecs(brand, model),
            'Camera': getCameraSpecs(brand, model),
            'Battery': getBatterySpecs(brand, model),
            'NFC': 'Yes',
            'Fingerprint': getFingerprintType(brand, model),
            'Color': colors[Math.floor(Math.random() * colors.length)],
            'Condition': conditions[Math.floor(Math.random() * conditions.length)],
            'Price': basePrice + (parseInt(ram) * 50) + (parseInt(storage) * 0.5),
            'Stock': Math.floor(Math.random() * 10),
            'IMEI': generateIMEI(),
            'Serial': generateSerial(brand),
            'LastUpdated': new Date().toISOString()
          });
        }
      });
    });
  });
});

// Helper functions
function getDisplaySpecs(brand, model) {
  if (brand === 'iPhone') {
    return model.includes('Pro') ? '6.7" OLED 120Hz' : '6.1" OLED 60Hz';
  } else if (brand === 'Samsung') {
    return model.includes('Ultra') ? '6.8" AMOLED 120Hz' : '6.6" AMOLED 120Hz';
  }
  return '6.5" AMOLED 120Hz';
}

function getCameraSpecs(brand, model) {
  if (brand === 'iPhone' && model.includes('Pro')) {
    return '48MP+12MP+12MP';
  } else if (brand === 'Samsung' && model.includes('Ultra')) {
    return '108MP+12MP+10MP+10MP';
  }
  return '50MP+12MP+12MP';
}

function getBatterySpecs(brand, model) {
  if (brand === 'iPhone') {
    return model.includes('Max') ? '4352mAh' : '3095mAh';
  } else if (brand === 'Samsung') {
    return model.includes('Ultra') ? '5000mAh' : '4500mAh';
  }
  return '4500mAh';
}

function getFingerprintType(brand, model) {
  if (brand === 'iPhone') {
    return 'Face ID';
  }
  return 'In-Display';
}

function generateIMEI() {
  return Array.from({ length: 15 }, () => Math.floor(Math.random() * 10)).join('');
}

function generateSerial(brand) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  return brand.substring(0, 3).toUpperCase() + 
         Array.from({ length: 7 }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

// Create workbook and add data
const workbook = utils.book_new();
const worksheet = utils.json_to_sheet(products);

// Set column widths
const colWidths = [
  { wch: 5 },  // ID
  { wch: 10 }, // Brand
  { wch: 20 }, // Model
  { wch: 8 },  // RAM
  { wch: 10 }, // Storage
  { wch: 8 },  // Network
  { wch: 20 }, // Processor
  { wch: 20 }, // Display
  { wch: 20 }, // Camera
  { wch: 12 }, // Battery
  { wch: 6 },  // NFC
  { wch: 15 }, // Fingerprint
  { wch: 10 }, // Color
  { wch: 12 }, // Condition
  { wch: 10 }, // Price
  { wch: 8 },  // Stock
  { wch: 17 }, // IMEI
  { wch: 12 }, // Serial
  { wch: 20 }  // LastUpdated
];

worksheet['!cols'] = colWidths;

utils.book_append_sheet(workbook, worksheet, 'Products');

// Save the file
writeFile(workbook, 'data/products.xlsx');

console.log('Sample data has been generated in data/products.xlsx');