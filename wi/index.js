#!/usr/bin/env node

const puppeteer = require('puppeteer');

async function main() {
  const url = process.argv[2];
  const files = process.argv.slice(3);

  if (files.length == 0) {
    console.log('wi - Batch import Wallabag V2 JSON-like data');
    console.log('Usage: wi.js <wallabag-url> <json-files...>');
    process.exit(0);
  }

  const ua = await puppeteer.connect({ browserURL: 'http://localhost:9222' });
  const pages = await ua.pages();
  const page = pages[0];

  for (const file of files) {
    await page.goto(`${url}/import/wallabag-v2`);

    const input = await page.$('input[type="file"]');
    await input.uploadFile(file);
    await page.$eval(
      '#upload_import_file_mark_as_read',
      el => el.checked=true
    );

    let nav = page.waitForNavigation({timeout: 0});
    await page.$eval(
      'form[name="upload_import_file"]',
      form => form.submit()
    );
    await nav;

    console.log(file);
  }

  process.exit(0);
}

main()


