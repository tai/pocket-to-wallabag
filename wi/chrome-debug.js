#!/usr/bin/env node

const puppeteer = require('puppeteer')

async function main() {
  const ua = await puppeteer.launch({
    headless: false,
    defaultViewport: null,
    args: ['--remote-debugging-port=9222']
  })

  let ep = new URL(ua.wsEndpoint())
  console.log(`=== Interrupt with ^C to end this script ===`)
  console.log(`Debug port is now open: http://${ep.host}`)

  // wait forever to keep browser alive
  await new Promise(() => {})
}

main()

