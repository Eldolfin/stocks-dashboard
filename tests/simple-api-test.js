/**
 * Simple API test to verify net worth endpoints work
 */
const fs = require('fs');
const path = require('path');

async function testNetWorthAPI() {
    const testExcelPath = path.join(__dirname, 'data', 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
    
    if (!fs.existsSync(testExcelPath)) {
        console.error('Test Excel file not found:', testExcelPath);
        return;
    }

    console.log('✓ Test Excel file exists');
    
    // Test the backend function directly
    const { execSync } = require('child_process');
    
    try {
        const result = execSync(`cd ../.. && python3 -c "
import sys
sys.path.append('backend/src')
from etoro_data import extract_net_worth
from pathlib import Path
import json

excel_file = Path('tests/data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx')
result = extract_net_worth(excel_file, 'D')
print(json.dumps({
    'success': True,
    'data_points': len(result['date']),
    'first_date': result['date'][0],
    'last_date': result['date'][-1],
    'first_value': result['net_worth'][0],
    'last_value': result['net_worth'][-1]
}, indent=2))
"`, { encoding: 'utf8' });
        
        const data = JSON.parse(result);
        console.log('✓ Backend net worth extraction works:');
        console.log(`  - Data points: ${data.data_points}`);
        console.log(`  - Date range: ${data.first_date} to ${data.last_date}`);
        console.log(`  - Value range: $${data.first_value} to $${data.last_value}`);
        
    } catch (error) {
        console.error('✗ Backend test failed:', error.message);
    }
}

if (require.main === module) {
    testNetWorthAPI();
}

module.exports = { testNetWorthAPI };