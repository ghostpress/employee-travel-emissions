# Quantifying the Carbon Emissions Caused by BU Employee Air Travel for Business and Research Purposes

Boston University has very ambitious Climate Action goals outlined in its [Climate Action Plan](https://www.bu.edu/climateactionplan/) (CAP), among them to reduce the University's emissions to net-zero by 2040. The CAP considers Scope 3 emissions, such as those from travel, to be an important area of investigation that has not yet been thoroughly explored. In September 2020, the [Campus Climate Laboratory](https://www.bu.edu/urbanclimate/campus-climate-lab/) granted funding to our group to attempt to quantify these emissions, using a dataset containing records of employee flights during the calendar years 2017 through early 2020. Our group consists of undergraduate students Olivia Henning and Lucia Vilallonga, and Dr. Jacqueline Ashmore, Executive Director of the [Institute for Sustainable Energy](https://www.bu.edu/ise/) and Research Associate Professor at the Department of Mechanical Engineering. For her full credentials, see Dr. Ashmore's [profile](https://www.bu.edu/ise/profile/jacqueline-ashmore/).

We have organized our code for this project in the following directories. Each directory contains its own readme with further details.

## analysis
This directory contains code for analyzing our data, once emissions have been calculated. Please see the readme in the analysis directory for more details.

## clean
This directory contains code for cleaning our data. Please see the readme in the clean directory for more details.

## scraper
This directory contains code for scraping the emissions values from the ICEC (ICAO Carbon Emissions Calculator), located at [ICAO.int](https://www.icao.int/environmental-protection/Carbonoffset/Pages/default.aspx). Please see the readme in the scraper directory for more details.

# Use Instructions
Using the anaconda environment managing tool and our requirements.txt file, this work can be replicated in any machine. To do so, enter the following command in a terminal window:

conda create --name myenv --file requirements.txt

Where myenv is the name of your local environment.

After cloning this repository, you must download the chromedriver associated with your version of the browser. Check your version of Chrome here and then download the corresponding chromedriver .zip file for your OS and browser version here. Then place the unzipped chromedriver file in scraper/code and make it executable.
