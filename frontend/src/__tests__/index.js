// import React from 'react';
import puppeteer from 'puppeteer';

const A_TEST_FILEPATH = require.resolve('../../../asl-api/A_test.jpg');
const DOMAIN = process.env.FRONTEND_DOMAIN;
console.log('domain is ', DOMAIN);

describe('sample test', () => {
  it('works', () => {
    expect(1).toBe(1);
  });
});

describe('image upload', () => {
  let browser;
  let page;
  beforeAll(async () => {
    browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    page = await browser.newPage();
    await page.goto(DOMAIN);
    await page.waitForSelector('#imageupload input[type="file"]');
  });

  it('has successful result A', async () => {
    const input = await page.$('#imageupload input[type="file"]');
    await input.uploadFile(A_TEST_FILEPATH);
    await page.waitForSelector('#crop-confirm');
    await page.click('#crop-confirm');
    await page.waitForSelector('#prediction');

    const prediction = await page.$eval('#prediction h1', e => e.innerHTML);
    expect(prediction).toMatchSnapshot();
  });

  afterAll(async () => {
    await browser.close();
  });
});
