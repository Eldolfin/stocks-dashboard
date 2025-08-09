import { chromium, Page, Browser } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

interface ScreenshotConfig {
  url: string;
  name: string;
  waitFor?: string | number; // selector to wait for or time in ms
  fullPage?: boolean;
}

class WebsiteScreenshotter {
  private browser: Browser | null = null;
  private page: Page | null = null;
  private outputDir: string;

  constructor(outputDir: string = './screenshots') {
    this.outputDir = outputDir;
  }

  async initialize() {
    this.browser = await chromium.launch();
    this.page = await this.browser.newPage();
    
    // Ensure output directory exists
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  async takeScreenshot(config: ScreenshotConfig): Promise<string> {
    if (!this.page) {
      throw new Error('Browser not initialized. Call initialize() first.');
    }

    console.log(`Taking screenshot of: ${config.url}`);
    
    try {
      // Navigate to the URL
      await this.page.goto(config.url, { waitUntil: 'networkidle' });
      
      // Wait for specific element or time if specified
      if (config.waitFor) {
        if (typeof config.waitFor === 'string') {
          await this.page.waitForSelector(config.waitFor, { timeout: 10000 });
        } else {
          await this.page.waitForTimeout(config.waitFor);
        }
      }

      // Take screenshot
      const screenshotPath = path.join(this.outputDir, `${config.name}.png`);
      await this.page.screenshot({ 
        path: screenshotPath, 
        fullPage: config.fullPage || false 
      });
      
      console.log(`Screenshot saved: ${screenshotPath}`);
      return screenshotPath;
    } catch (error) {
      console.error(`Failed to screenshot ${config.url}:`, error);
      throw error;
    }
  }

  async takeMultipleScreenshots(configs: ScreenshotConfig[]): Promise<string[]> {
    const results: string[] = [];
    
    for (const config of configs) {
      try {
        const path = await this.takeScreenshot(config);
        results.push(path);
      } catch (error) {
        console.error(`Failed to take screenshot for ${config.name}:`, error);
        // Continue with other screenshots even if one fails
      }
    }
    
    return results;
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

// Default screenshot configurations for the stocks dashboard
const defaultScreenshots: ScreenshotConfig[] = [
  {
    url: 'http://localhost:8085/',
    name: 'homepage',
    waitFor: 'h1', // Wait for main heading
    fullPage: true
  },
  {
    url: 'http://localhost:8085/login',
    name: 'login-page',
    waitFor: 'button:text("Login")',
    fullPage: true
  },
  {
    url: 'http://localhost:8085/register',
    name: 'register-page', 
    waitFor: 'button:text("Register")',
    fullPage: true
  },
  {
    url: 'http://localhost:5000/openapi/',
    name: 'api-docs',
    waitFor: 2000, // Wait 2 seconds for API docs to load
    fullPage: true
  }
];

// Authenticated page screenshots (these require login)
const authenticatedScreenshots: ScreenshotConfig[] = [
  {
    url: 'http://localhost:8085/portfolio',
    name: 'portfolio-page',
    waitFor: 'button:text("Upload file")',
    fullPage: true
  },
  {
    url: 'http://localhost:8085/profile',
    name: 'profile-page',
    waitFor: 1000,
    fullPage: true
  },
  {
    url: 'http://localhost:8085/details/AAPL',
    name: 'details-page-aapl',
    waitFor: 2000, // Wait for charts to load
    fullPage: true
  },
  {
    url: 'http://localhost:8085/compare/AAPL,MSFT',
    name: 'compare-page',
    waitFor: 2000, // Wait for comparison chart to load
    fullPage: true
  }
];

// Authentication helper using the same pattern as the test fixtures
async function authenticateUser(page: Page): Promise<void> {
  const email = `screenshot-user-${Math.random().toString(36).substring(2, 15)}@test.com`;
  const password = "testpassword123";

  console.log('Authenticating user for protected pages...');
  
  // Register user
  await page.goto('http://localhost:8085/register');
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Register' }).click();
  
  // Login user
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();
  
  // Wait for login to complete
  await page.waitForSelector('button:text("Logout")', { timeout: 10000 });
  console.log('User authenticated successfully');
}

// Main function to handle CLI usage
async function main() {
  const args = process.argv.slice(2);
  const outputDir = args[0] || './screenshots';
  const targetUrl = args[1]; // Optional single URL to screenshot
  
  const screenshotter = new WebsiteScreenshotter(outputDir);
  
  try {
    await screenshotter.initialize();
    
    if (targetUrl) {
      // Single URL mode
      const config: ScreenshotConfig = {
        url: targetUrl,
        name: `screenshot-${Date.now()}`,
        waitFor: 2000,
        fullPage: true
      };
      await screenshotter.takeScreenshot(config);
    } else {
      // Full suite mode
      console.log('Taking screenshots of public pages...');
      await screenshotter.takeMultipleScreenshots(defaultScreenshots);
      
      console.log('Taking screenshots of authenticated pages...');
      // Create a new page for authenticated screenshots
      const authPage = await screenshotter['browser']!.newPage();
      await authenticateUser(authPage);
      
      // Use the authenticated page for protected screenshots
      const originalPage = screenshotter['page'];
      screenshotter['page'] = authPage;
      await screenshotter.takeMultipleScreenshots(authenticatedScreenshots);
      screenshotter['page'] = originalPage;
      
      await authPage.close();
    }
    
    console.log('All screenshots completed successfully!');
  } catch (error) {
    console.error('Screenshot process failed:', error);
    process.exit(1);
  } finally {
    await screenshotter.close();
  }
}

// Export for programmatic usage
export { WebsiteScreenshotter, defaultScreenshots, authenticatedScreenshots };

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}