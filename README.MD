# Web Crawler

![GitHub Created At](https://img.shields.io/github/created-at/gabimin/wanderer?style=flat-square&logoSize=auto&labelColor=black&color=teal)

Python script for a simple web crawler that parses webpages, follows hyperlinks, and repeats the process for a specified number of links.

## Features

- Starts from an initial URL and follows a user-defined number of links
- Avoids revisiting already parsed URLs
- Backtracks to previous pages when no new links are available
- Handles errors by returning to previous pages
- Logs the navigation history to a Markdown file

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/web-crawler.git
   cd web-crawler
   ```

2. Install the required libraries:

   ```
   pip install requests beautifulsoup4
   ```

## Use

Run the script from the command line:

```
python3 web_crawler.py
```

Prompt to enter:

1. The starting URL
2. The number of links to follow

The script will then start crawling and log its progress to both the console and a file named `navigation_history.md`.

## How it works

1. The script starts at the given URL and parses the page for hyperlinks.
2. It follows the third unvisited link it finds.
3. If a page has no unvisited links, it backtracks to the previous page and tries to find a new unvisited link.
4. This process continues until the specified number of links have been followed or no more unvisited links are available.
5. The script handles errors by returning to the previous page.

## Customization

Modification of the `headers` dictionary in the script to change the User-Agent string if needed.

## Output

The script generates a Markdown file named `navigation_history.md` that logs:

- The current page URL
- The next link being followed
- Any errors encountered during the crawling process

## Disclaimer

Please use this script responsibly and in accordance with the robots.txt file of the websites you're crawling. Respect the website's terms of service and do not overload servers with rapid or excessive requests.
