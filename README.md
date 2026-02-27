
# **TwendeEV - Kenyan EV charging station location optimization using population**  
Link to the TwendeEv App ~ https://twende-ev.streamlit.app/

Dark Mode App
![Dark_mode_app](https://github.com/user-attachments/assets/aa757cad-7986-4e72-b7d7-27a2b32f29a0)


Light Mode App
![Light_mode_app](https://github.com/user-attachments/assets/d2f8a59c-1995-4295-9b13-03e970bff727)


## **Business Understanding**
### **Overview** 
The transition to electric vehicles (EVs) in Kenya is steadily gaining momentum due to :


- Rising fuel costs - [Africa News](https://www.africanews.com/2023/09/15/fuel-prices-hit-all-time-high-in-kenya/)

- Environmental concerns - [Wikipedia](https://en.wikipedia.org/wiki/Environmental_issues_in_Kenya)

- Government support for clean energy adoption - National EV Policy [government PDF](https://www.transport.go.ke/sites/default/files/Emobility%20Policy%20Final.pdf)

However, the growth of EV usage is heavily dependent on the availability and accessibility of charging infrastructure. Poorly planned charging station placement can lead to underutilized assets, high operational costs, and limited EV adoption.

This project focuses on developing a data-driven optimization framework to determine the most strategic locations for EV charging stations across Kenya using population data as the primary demand indicator. 


By integrating:

- Population density data

- Geospatial analysis (latitude & longitude coordinates)

- Demand forecasting models

- Machine learning and clustering techniques

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

* `county_coordinates.csv` We webscraped data from this site [Latitude.to](https://latitude.to/) This dataset contains county co-ordinate centroids.


## **Data Cleaning and Preparation**
The datasets were systematically cleaned and prepared to ensure accuracy and reliability in the modeling process. This involved standardizing column names and formats, removing irrelevant fields, handling missing values, correcting data types, and validating geographic coordinates to eliminate duplicates and incomplete records. Additional features such as population density and station-to-population ratios were engineered to strengthen predictive performance. Finally, the data was aggregated at the county level to align with administrative planning units, resulting in a structured, analysis-ready dataset suitable for machine learning and spatial optimization.


## **Feature Engineering**
We used these features for the modeling section:
- stations_per_100k: Normalized station count per 100,000 population

- population_density: Population per unit area

- population_per_station: Average population served per station (uses population as fallback for counties with no stations)

- station_spatial_density: Number of stations per unit area

- required_stations: Target number of stations based on population (1 per 200,000 people, minimum 1)

- additional_stations: Gap between required and existing stations


## **EDA**
A bar graph representing required additional stations per county
![Additional stations required](https://github.com/user-attachments/assets/7288e2d6-5e75-4449-a034-1475d557f771)



A bar graph representing population per county
![Population per county](https://github.com/user-attachments/assets/f145d6f7-3a31-4737-bb68-af429d291aa1)




A scatter plot representing county population vs available charging stations
![Population vs current station](https://github.com/user-attachments/assets/8e4cb2f4-8da7-4b60-bd9e-55b28d104a3e)




## **Modeling and Evaluation**
### **Additioanl Stations Model(Random Forest Regressor)** 
A Random Forest Regressor was trained to predict the number of additional stations needed per county:

**Features**: population, population_density, num_stations, station_spatial_density, shape area

**Target**: additional_stations

Model Performance (5-fold cross-validation, 5 repeats):

- Mean CV R²: 0.67 (strong performance for small structured datasets)

- Mean CV RMSE: 0.55 stations

- Mean CV MAE: 0.28 stations (average error less than one-third of a station)


### **Station Placement Model(KMeans Clustering)** 
For each county requiring new stations, a KMeans clustering model was developed to generate optimal coordinates:

**Process**: Synthetic candidate points generated around county centroids

**Training**: Points combined with existing station coordinates (where available)

**Output**: K cluster centers representing recommended new station locations

Total recommended stations: 75 across all counties

### **Model Evaluation Metrics**
KMeans clustering performance:

- Mean silhouette score: 0.47 (good cluster separation)

- Mean intra-cluster distance: 0.044 (points close to their assigned centers)

- Mean inter-cluster distance: 0.031 (good separation between clusters)

## **Recommendations**

1. **Prioritize High-Gap Counties**: The analysis identifies a significant infrastructure gap of 75 new stations required across 47 counties. We recommend that the Ministry of Transport and private investors prioritize deployment in counties with the highest predicted need, such as Nairobi (5 new stations), Mombasa (6), Kiambu (8), and Nakuru (4), to address the most severe service deficiencies first.

2. **Utilize Geospatial Model for Site Selection**: The KMeans clustering model provides optimized, data-driven co-ordinates for new stations within each county. We recommend that investors and utility providers use these generated co-ordinates as primary candidates for site feasibility studies, rather than relying on arbitrary or centralized placement, to ensure broader population coverage and reduce clustering.

3. **Adopt the Predictive Model for Scalable Planning**: The Random Forest model demonstrated strong predictive performance in forecasting additional station requirements based on demographic data. We recommend that policymakers and planners use this model to simulate how future population growth in different counties will impact infrastructure needs, enabling proactive and scalable expansion of the national charging network.

## **Conclusions**
This project successfully developed and implemented a data-driven optimization framework to address the strategic placement of EV charging stations across Kenya.

Through the integration of population distribution, geospatial data, and existing station information, the analysis was able to identify significant infrastructure gaps, calculate that a minimum of 75 new stations are needed to meet population-based requirements. By engineering key features such as population density and existing_stations, a Random Forest model was trained to accurately predict the number of additional stations needed per county.

Furthermore, a KMeans clustering approach was employed to generate optimized, data-driven co-ordinates for new station placement, moving beyond simple central points to ensure better spatial distribution. The final output provides a practical, interactive map and a clear, ranked list of recommended locations.

This analysis equips policymakers and investors with a robust decision-support tool to guide the efficient, equitable, and future-ready expansion of Kenya's EV charging infrastructure, directly supporting the country's transition to electric mobility.

## **Limitations**
1. **Data Source Limitations**: The primary limitation is the exclusive use of population as a proxy for demand. While a strong indicator, this model does not account for other critical factors such as traffic patterns, existing power grid capacity and road networks which are vital for a commercially viable charging network.

2. **Population Data Age**: The analysis relies on the 2019 Kenya census data. While it provides a solid baseline, it does not reflect the most current population distribution or recent urbanization trends, which could lead to minor inaccuracies in the predicted station requirements.

3. **Simplified Station Placement Logic**: The KMeans model generates candidate co-ordinates based on geographic spread around existing stations. It does not incorporate real-world constraints like land ownership, terrain, or proximity to existing buildings and infrastructure. The recommended sites should therefore be considered as highly informed starting points for site surveys, not definitive construction locations.

