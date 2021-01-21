# Quantifying the Carbon Emissions Caused by BU Employee Air Travel for Business and Research Purposes

Boston University has very ambitious Climate Action goals outlined in its [Climate Action Plan](https://www.bu.edu/climateactionplan/) (CAP), among them to reduce the University's emissions to net-zero by 2040. The CAP considers Scope 3 emissions, such as those from travel, to be an important area of investigation that has not yet been thoroughly explored. In September 2020, the [Campus Climate Laboratory](https://www.bu.edu/urbanclimate/campus-climate-lab/) granted funding to our group to attempt to quantify these emissions, using a dataset containing records of employee flights during the calendar years 2017 through early 2020. Our group consists of undergraduate students Olivia Henning and Lucia Vilallonga, and Dr. Jacqueline Ashmore, Executive Director of the [Institute for Sustainable Energy](https://www.bu.edu/ise/) and Research Associate Professor at the Department of Mechanical Engineering. For her full credentials, see Dr. Ashmore's [profile](https://www.bu.edu/ise/profile/jacqueline-ashmore/).

We have organized our code for this project in the following directories. Each directory contains its own readme with further details.

## analysis
This directory contains code for analyzing our data, once emissions have been calculated. 

## clean
This directory contains code for cleaning our data. In an attempt to get started with calculating the emissions quickly, we initially did the cleaning by hand using Microsoft Excel and LibreOffice Calc. In the interest of ensuring that our research is reproducible and transparent, we have started replicating the manual process in Python. These methods are still underway; to keep track of our progress, please see the code contained in the luciav-clean and oliviah-clean branches.

## scraper
This directory contains code for scraping the emissions values from the ICEC (ICAO Carbon Emissions Calculator), located at [ICAO.int](https://www.icao.int/environmental-protection/Carbonoffset/Pages/default.aspx). Please see the readme in the scraper directory for more details.
