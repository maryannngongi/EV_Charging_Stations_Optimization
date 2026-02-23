# **Kenyan EV charging station location optimization using population** 
## **Business Understanding**
### **Overview** 
The transition to electric vehicles (EVs) in Kenya is steadily gaining momentum due to :


~ Rising fuel costs - https://www.africanews.com/2023/09/15/fuel-prices-hit-all-time-high-in-kenya/.

~ Environmental concerns - https://en.wikipedia.org/wiki/Environmental_issues_in_Kenya.

~ Government support for clean energy adoption - National EV Policy (government PDF) - https://www.transport.go.ke/sites/default/files/Emobility%20Policy%20Final.pdf.

However, the growth of EV usage is heavily dependent on the availability and accessibility of charging infrastructure. Poorly planned charging station placement can lead to underutilized assets, high operational costs, and limited EV adoption.

This project focuses on developing a data-driven optimization framework to determine the most strategic locations for EV charging stations across Kenya using population data as the primary demand indicator. 


By integrating:

~ Population density data

~ Geospatial analysis (latitude & longitude coordinates)

~ Demand forecasting models

~ Machine learning and clustering techniques

The system aims to rank and recommend optimal charging station locations.

Ultimately, this project provides policymakers, investors, utility providers, and urban planners with a practical decision-support tool to guide efficient EV infrastructure deployment across Kenya.
### **Business Problem and Stakeholders**
According to this source; [Kenya: EV numbers surge, more charging stations to be rolled out](https://www.esi-africa.com/news/kenya-ev-numbers-surge-more-charging-stations-to-be-rolled-out/),
 the increase in electric vehicles in Kenya has created pressure on charging infrastructure. Many areas lack sufficient charging stations, while others are underutilized. 
 
A Single Station Cuts Charging Time and Hints at What a Functioning National EV Network Might Finally Look Like. This is from, [The new charger lands in a city where riders are counting every minute they lose to slow stations that still sit too far apart](https://techtrendske.co.ke/2025/11/19/kenya-ev-fast-charging-network/)

The primary stakeholders for this problem are Government; Ministry of Transport and Ministry of Energy, EV charging investors, EV drivers and EV charging companies.The government uses the system for data-driven infrastructure planning, investors identify profitable charging locations, EV companies improve fleet operations and expansion decisions, and EV drivers gain easier access to reliable nearby charging stations.

 ### **Objectives**
 1. Where should new EV charging stations be placed in each county in Kenya to ensure equitable population coverage?

2. How many charging stations are currently available per county, and how many additional stations are required to meet minimum population-based infrastructure needs?

3. How can charging infrastructure be spatially distributed within counties to maximize coverage and reduce clustering inefficiencies?

4. How can projected population growth be used to estimate the number of additional EV charging stations needed in the future?
### **Business Solution**
This project aims to develop a data-driven EV charging infrastructure optimization model for Kenya that integrates population distribution, county area size, existing station counts, and spatial coordinates to determine infrastructure gaps and recommend expansion strategies.  

Using population-based thresholds and applying spatial clustering techniques, number of new stations required per county are to be identified and the model should generate optimized geographic coordinates for their placement.  

Additionally, a machine learning model is to be trained to predict required charging stations based on demographic and spatial infrastructure features, enabling scalable and future-ready planning as population grows.  

The final outcome should be a strategic decision-support tool that guides policymakers, the kenyan government and energy stakeholders on where and how to expand Kenya’s EV charging network efficiently and equitably.
## **Data Understanding** 

The datasets utilized in this project are:
* `charging_station.csv`  [Hugging Face](https://huggingface.co/datasets/tarekmasryo/global-ev-infra-dataset),
This dataset shows the co-ordinates, charging station names, power class, country code and state province of different charging stations across the world.


* `kenya_ev_charging_stations_sample_new.csv` [Fundi wa EV](https://www.fundiwaev.co.ke/ev_database) This dataset expounds deeper into charging stations in Kenya.
The columns utilized in this dataset are County/City, Station name, Charger Type and Co-ordinates.

* `kenya-poulation-distribution-2019.csv` [Kaggle](https://www.kaggle.com/datasets/paulmaluki/kenyapopulationdistibution-2019-censuscsv) This dataset shows population density in different counties across Kenya.

* `ken_adminboundaries_tabulardata.xlsx` [OCHA services](https://data.humdata.org/dataset/cod-ab-ken) This dataset shows details on county boundaries across the country.
The Shape Area for each county was the core column utilized in this dataset.

* `county_coordinates.csv` This dataset contains county co-ordinate centroids.
