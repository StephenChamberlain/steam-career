Steam Career [![Build Status](https://github.com/StephenChamberlain/steam-career/actions/workflows/ci-cd.yml/badge.svg)](https://travis-ci.com/StephenChamberlain/steam-career) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
========
Python application which uses the Steam Web API to retrieve player data and present an overview in HTML 
form.

## Instructions
1. Log in to steam and generate an API key (see https://steamcommunity.com/dev/apikey).
2. Install the tool (https://github.com/StephenChamberlain/steam-career/releases/download/v1.1/Steam_Career_1.1.exe)
3. Provide the steam user ID of the player to generate results for, the API key you
defined in step 1 and the output location for the results and click "Go". You can
also optionally choose to force overwrite the CSS in the resulting location (see 
'Customisations').

![User interface](/docs/ui.png?raw=true)  

4. The resulting HTML site will be generated and opened in your default browser.

## Customisations
The result location will contain a directory with the steam user's name, itself 
containing several files; the resulting HTML site and an external CSS style 
sheet. This stylesheet can be modified as you see fit, the tool will not overwrite 
this file if it already exists, unless 'Overwrite CSS' is selected. You can modify the
stylesheet and affect the look and feel of all results.

The HTML templates themselves can also be customised; they can be found in the installation
directory (e.g. C:\Program Files\Steam Career)\pkgs\steamcareer\templates directory.
The template uses Jinja2 syntax; see smiley's https://github.com/smiley/steamapi 
project for more information on the available functionality from the 'game' and
'user' references.

## Result
If all goes well, the application will generate output in HTML form. 
An example is given below.
![Top most played](/docs/result1.png?raw=true)
![Hours played](/docs/result2.png?raw=true)
![Top 10](/docs/result3.png?raw=true)
![Price list](/docs/result4.png?raw=true)

## Environment
- Github.
- Microsoft Visual Code with pylance OR Eclipse (Oxygen.1a Release (4.7.1a)) with PyDev installed
- Python (3.6.3).
- Github Actions (CI/CD).

## Components
| Name     | Purpose      |  Link |
|:---------|:-------------|------:|
| Steamapi | Backend API, contains player and game information | https://github.com/StephenChamberlain/steamapi forked from https://github.com/smiley/steamapi |
| Steam Web API | Frontend API, store information | https://partner.steamgames.com/doc/webapi_overview |
| Tkinter | GUI | https://docs.python.org/3/library/tkinter.html |
| Jinja2 | Templating engine | https://docs.python.org/3/library/tkinter.html |
| Google charts | Top 10 view | https://developers.google.com/chart |
| Babel | Currency information | http://babel.pocoo.org/en/latest/ |
| Icon | Used in GUI | http://www.veryicon.com/icons/internet--web/modern-web/steam-7.html |
| Pynsist | NSIS installer for Python | https://github.com/takluyver/pynsist |
| NSIS 3.06.1 | NSIS installer engine | https://nsis.sourceforge.io/Main_Page |

## Legal
This project is not endorsed in any way by Valve Corporation.