# wi - Import (large) Pocket CSV into Wallabag

Pocket recently announced EOL and I have around 10k entries to be migrated.

While it was easy setting up wallabag, importing CSV data exported
from Pocket turned out to be quite a hassle. While there are many
available methods for migration, all failed or only partly worked.

I've written a set of tools to import Pocket CSV regardless of its size,
and publishing here so people can use it.

## Problems

- 'Import from Pocket' UI (using Pocket consumer key) is slow and only imported part of my entries (around 1000+ and it didn't proceed further)
- [Helper script to import CSV data over Wallabag API](https://github.com/wallabag/wallabag/issues/7635#issuecomment-2727691106) is slow and overwrites date of articles
  - This is because current Wallabag API does not provide a way to create an entry with past created_at date.

So, I decided to convert Pocket-exported CSV into Wallabag JSON format and use 'Import Wallabag JSON' UI to import the data. However,

- 'Import from Wallabag JSON' UI fails when JSON to be imported has more than few hundred entries
  - It failed with out-of-memory
  - It failed with timeout

I read on [a hard core way](https://www.claudiuscoenen.de/2025/05/pocket-to-wallabag-hardcore-edition/) with different backend/setup to mitigate these issues, but that's too cumbersome and I decided to take other route - DIY.

Currently, [a discussion is ongoing to support direct import of Pocket CSV from the UI](https://github.com/wallabag/wallabag/pull/8240),
but I presume this new feature is also prone to above out-of-memory/timeout errors.

## Workaround

I worked around the issue by following:

- Export CSV from Pocket
- Convert Pocket CSV into Wallabag V2 JSON in splitted form
- Launch Chrome with debug port enabled (for automation access)
- Import each chunk of JSON with browser automation tool

## Usage

```
$ ls -FCs
total 24
8 README.md     8 p2w2.py*      8 pocket.csv    0 wi/

// Convert Pocket CSV into Wallabag V2 JSON (out.json and out/*.json)
//
// Packaged pocket.csv is just a sample out from my CSV data to test
// the tool, so you should use your own Pocket CSV in real migration.
$ python3 p2w2.py pocket.csv

// Wallabag V2 JSON files are generated in out/ folder (out.json
// is a non-split version)
$ ls -FCs
total 32
8 README.md     8 out.json      8 pocket.csv
0 out/          8 p2w2.py*      0 wi/

// *In separate console*, launch browser with debugport enabled
//
// Now, open your wallabag site and login manually.
// This is needed because automation script does not have a code
// to login to the site.
$ node wi/chrome-debug.js

// *In other console*, run importer tool
$ node wi/index.js https://my.wallabag.host out/*.json

// Just re-run it multiple times in case of an error.
// These will continue from where it last failed.
// If re-run finishes without any error, then migration is complete.
$ node wi/index.js https://my.wallabag.host out/*.json
$ node wi/index.js https://my.wallabag.host out/*.json
$ node wi/index.js https://my.wallabag.host out/*.json
```

## Installation

I didn't put any effort in packaging, so this is not a standard
package which you can install by pip or npm. However, this should
almost work out of the box as only built-in libraries are used
except for puppeteer on Node.js.

```
$ git clone https://github.com/tai/pocket-to-wallabag
$ cd pocket-to-wallabag/wi
$ npm i
$ cd ..
$ ls -FCs
total 24
8 README.md     8 p2w2.py*      8 pocket.csv    0 wi/
```

Once done setting up, overwrite pocket.csv with your copy of Pocket CSV export and follow above example.
