# Multidimensional Poverty Index (MPI) - Data package

This data package contains the data that powers the chart ["Multidimensional Poverty Index (MPI)"](https://ourworldindata.org/grapher/multidimensional-poverty-index-mpi-hot?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on January 26, 2026.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For normal countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The final column is the data column, which is the time series that powers the chart. If the CSV data is downloaded using the "full data" option, then the column corresponds to the time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data column is transformed depending on the chart type and thus the association with the time series might not be as straightforward.

## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

## Detailed information about the data


## Multidimensional Poverty Index (MPI) – Harmonized over time
Multidimensional poverty is defined as being deprived in a range of health, education and living standards indicators. The Multidimensional Poverty Index (MPI) is a measure that combines the prevalence and the intensity of multidimensional poverty on a scale from 0 to 1. Higher values indicate higher poverty.
Last updated: December 23, 2025  
Next update: December 2026  
Date range: 2001–2023  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
Alkire et al. (2025) - The Global Multidimensional Poverty Index (MPI) 2025 – with minor processing by Our World in Data

#### Full citation
Alkire et al. (2025) - The Global Multidimensional Poverty Index (MPI) 2025 – with minor processing by Our World in Data. “Multidimensional Poverty Index (MPI) – Harmonized over time” [dataset]. Alkire et al., “Global Multidimensional Poverty Index (MPI) 2025” [original data].
Source: Alkire et al. (2025) - The Global Multidimensional Poverty Index (MPI) 2025 – with minor processing by Our World In Data

### What you should know about this data
* The Multidimensional Poverty Index (MPI) is calculated by multiplying two values: the [share of people who are multidimensionally poor](https://ourworldindata.org/grapher/share-multi-poverty) and the [intensity of their poverty](https://ourworldindata.org/grapher/intensity-of-multidimensional-poverty-national).
* Being in multidimensional poverty means that a person lives in a household deprived in a third or more of ten indicators, grouped into three dimensions of well-being: **health** (using two indicators: nutrition, child mortality), **education** (using two indicators: years of schooling, school attendance), and **living standards** (using six indicators: cooking fuel, sanitation, drinking water, electricity, housing, assets).
* Each household is assessed against specific thresholds for these indicators. For example, a household is considered deprived in the _electricity_ indicator if it does not have access to it. [This article](https://ourworldindata.org/multidimensional-poverty-index) discusses specific thresholds in more detail.
* Each indicator contributes to one of the three dimensions of well-being.  Health and education indicators are weighted more (1/6 each) than living standards indicators (1/18 each) so that all three dimensions contribute equally to the overall measure.
* The intensity of multidimensional poverty is calculated as the average share of indicators in which those counted as MPI poor are deprived.
* This indicator is a harmonized over time (HOT) estimate. This harmonization seeks to make two or more MPI estimates comparable by aligning the indicator definitions in each survey. Look for the [current margin estimate (CME)](https://ourworldindata.org/grapher/multidimensional-poverty-index-mpi) to see the most recent survey data.

### How is this data described by its producer - Alkire et al. (2025) - The Global Multidimensional Poverty Index (MPI) 2025?
The global MPI is a measure of acute poverty covering over 100 countries in the developing regions of the world. This measure is based on the dual-cutoff counting approach to poverty developed by Alkire and Foster (2011). The global MPI was developed in 2010 by Alkire and Santos (2014, 2010) in collaboration with the UNDP’s Human Development Report Office (HDRO). Since its inception, the global MPI has used information from 10 indicators, which are grouped into three equally weighted dimensions: health, education, and living standards. These dimensions are the same as those used in the UNDP’s Human Development Index.

In 2018, the first major revision of the global MPI was undertaken, considering improvements in survey microdata and better align to the 2030 development agenda insofar as possible (Alkire and Jahan, 2018; OPHI, 2018). The revision consisted of adjustments in the definition of five out of the ten indicators, namely child mortality, nutrition, years of schooling, housing and assets. Alkire, Kanagaratnam, Nogales and Suppa (2022) provide a comprehensive analysis of the consequences of the 2018 revision. The normative and empirical decisions that underlie the revision of the global MPI, and adjustments related to the child mortality, nutrition, years of schooling and housing indicators are discussed in Alkire and Kanagaratnam (2021). The revision of assets indicator is detailed in Vollmer and Alkire (2022).

The global MPI begins by establishing a deprivation profile for each person, showing which of the 10 indicators they are deprived in. Each person is identified as deprived or non-deprived in each indicator based on a deprivation cutoff. In the case of health and education, each household member may be identified as deprived or not deprived according to available information for other household members. For example, if any household member for whom data exist is undernourished, each person in that household is considered deprived in nutrition. Taking this approach – which was required by the data – does not reveal intrahousehold disparities, but is intuitive and assumes shared positive (or negative) effects of achieving (or not achieving) certain outcomes. Next, looking across indicators, each person’s deprivation score is constructed by adding up the weights of the indicators in which they are deprived. The indicators use a nested weight structure: equal weights across dimensions and an equal weight for each indicator within a dimension. The normalised indicator weight structure of the global MPI means that the living standard indicators receive lower weight than health and education related indicators because from a policy perspective, each of the three dimensions is of roughly equal normative importance.

In the global MPI, a person is identified as multidimensionally poor or MPI poor if they are deprived in at least one-third of the weighted MPI indicators. In other words, a person is MPI poor if the person’s deprivation score is equal to or higher than the poverty cutoff of 33.33 percent. After the poverty identification step, we aggregate across individuals to obtain the incidence of poverty or headcount ratio (H) which represents the percentage of poor people in the population. We then compute the intensity of poverty (A), representing the average percentage of weighted deprivations experienced by the poor. We then compute the adjusted poverty headcount ratio (M0) or MPI by combining H and A in a multiplicative form (MPI = H x A).

Both the incidence and the intensity of these deprivations are highly relevant pieces of information for poverty measurement. The incidence of poverty is intuitive and understandable by anyone. People always want to know how many poor people there are in a society as a proportion of the whole population. Media tend to pick up on the incidence of poverty easily. Yet, the proportion of poor people as the headline figure is not enough (Alkire, Oldiges and Kanagaratnam, 2021).

A headcount ratio is also estimated using two other poverty cutoffs. The global MPI identifies individuals as vulnerable to poverty if they are close to the one-third threshold, that is, if they are deprived in 20 to 33.32 percent of weighted indicators. The tables also apply a higher poverty cutoff to identify those in severe poverty, meaning those deprived in 50 percent or more of the dimensions.

The AF methodology has a property that makes the global MPI even more useful—dimensional breakdown. This property makes it possible to consistently compute the percentage of the population who are multidimensionally poor and simultaneously deprived in each indicator. This is known as the censored headcount ratio of an indicator. The weighted sum of censored headcount ratios of all MPI indicators is equal to the MPI value.

The censored headcount ratio shows the extent of deprivations among the poor but does not reflect the weights or relative values of the indicators. Two indicators may have the same censored headcount ratios but different contributions to overall poverty, because the contribution depends both on the censored headcount ratio and on the weight assigned to each indicator. As such, a complementary analysis to the censored headcount ratio is the percentage contribution of each indicator to overall multidimensional poverty.

### Source

#### Alkire et al. – Global Multidimensional Poverty Index (MPI)
Retrieved on: 2025-12-23  
Retrieved from: https://ophi.org.uk/global-mpi  


    