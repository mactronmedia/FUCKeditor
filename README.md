# fuckeditor - FCKeditor Vulnerability Scanner

![Banner](banner.png)

A vulnerability scanner for FCKeditor instances, capable of detecting specific titles indicative of vulnerable installations.

## Table of Contents
- [Overview](#overview)
- [Usage](#usage)
- [Features](#features)
- [Installation](#installation)
- [Options](#options)
- [Results](#results)

## Overview
This Python script scans a list of target URLs for FCKeditor instances and identifies potential vulnerabilities based on the title of the returned pages.


## Features

**Performs scans using two methods:**

**- Quick Scan:** Utilizes a predefined list of common prefixes to explore potentially vulnerable locations.
**- Full Scan (Optional):** Employs a more extensive list of prefixes for a more thorough check, but may take longer.

**Outputs results:**

**- Successes:** URLs with titles indicating a vulnerable FCKeditor installation are written to a success.txt file.
**- Informative messages:** Provides feedback on the scan progress and encountered issues.

**Error handling:**
- Catches connection timeouts and gracefully skips those URLs.
- Handles general request exceptions and logs them for debugging.

## Prerequisites && Installation

### Prerequisites:
```bash
Python 3 (tested with 3.x on ArchLinux, & KaliLinux)
```

**Required libraries:**
```bash
requests
argparse
beautifulsoup4
colorama (optional for colored output)
urllib3 (may be included with requests)
```

### Installation:

```bash
git clone https://github.com/mactronmedia/fuckeditor.git
cd fuckeditor
pip install -r requirements.txt
```

## Usage

-t TARGETS_FILE: Specify the targets file (default: targets.txt).
-f, --full-scan: Perform a full scan using full_prefixes.txt.
-q, --quick-scan: Perform a common scan using common_prefixes.txt.

```bash
python fuckeditor.py [-h] [-t TARGETS_FILE] [-f] [-q]
```

## Results

![Results](results.png)


