# Qt Webapp

## Overview

Qt Webapp is a desktop web-app program built using Python Qt and based on Chromium. Its primary purpose is to enable SaaS (Software as a Service) applications to run on desktop devices without relying on web browsers.

## Features

- Pop-up alert if the user attempts to close the window
- File downloading functionality
- Printing without a dialog, which is particularly useful for POS (Point of Sale) Web Applications


## Installation

```bash
pip install -r requirements.txt
```

## Exporting as .EXE setup file

To export the Qt Webapp as a standalone .EXE executable, follow these steps:

Run the following command to build the executable:

```bash
python setup.py build
```