Steam Career [![Build Status](https://travis-ci.org/StephenChamberlain/steam-career.svg?branch=master)](https://travis-ci.org/StephenChamberlain/steam-career)
========
Experimental Python application which uses the Steam Web API to retrieve player data and present an overview in HTML 
form.

## Instructions
1. Log in to steam and generate an API key (see https://steamcommunity.com/dev/apikey).
2. Install the tool (TODO: link to installer!)
3. Provide the steam user ID of the player to generate results for, the API key you
defined in step 1 and the output location for the results and click "Go".  

![User interface](/docs/ui.png?raw=true)  

4. The resulting HTML file will be generated and opened in your default browser.

## Customisations
The result location will contain two files; the resulting HTML itself and
an external CSS style sheet. This stylesheet can be modified as you see fit, the
tool will not overwrite this file if it already exists. Results are stored in an 
HTML file with the name of the player, so you can modify the single stylesheet and
affect the look and feel of all results.

The HTML template itself can also be customised; it can be found in the installation
directory (e.g. C:\Program Files\Steam Career)\pkgs\steamcareer\templates directory.
The template uses Jinja2 syntax; see smiley's https://github.com/smiley/steamapi 
project for more information on the available functionality from the 'game' and
'user' references.

## Result
If all goes well, the application will generate output in HTML form. 
An example is given below.
![Resulting HTML file](/docs/result.png?raw=true)

## Environment
- Github.
- Eclipse (Oxygen.1a Release (4.7.1a)) with PyDev installed.
- Python (3.6.3).
- Travis CI.

## Components
- Steamapi (https://github.com/StephenChamberlain/steamapi forked from https://github.com/smiley/steamapi).
- Tkinter (UI).
- Jinja2 (templating engine).
- Pynsist (https://github.com/takluyver/pynsist installer).
- Icon from http://www.veryicon.com/icons/internet--web/modern-web/steam-7.html.

## Legal
This project is not endorsed in any way by Valve Corporation.