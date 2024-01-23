# Facebook City

## Overview

This repository contains the data and code associated with the paper titled "Facebook City: Place-named groups as urban communication infrastructure in Greater London". 
This is part of the "Localising Content Governance" project, funded by **Facebook Research** at Birkbeck, University of London and King's College London. 

**Keywords**: Facebook groups, Greater London, digital platform infrastructure, spatial social media, urban communication, neighbourhood groups, communication geography

## Paper abstract

This paper investigates the geography of Facebook use at an urban-regional scale, focussing on place-named groups, meaning various interest groups with names relating to places such as towns, neighbourhoods, or points of interest. Conceptualising Facebook as a digital infrastructure – that is, the platform’s urban footprint, in the form of its place-named groups, rather than what individuals share and create using the service – we explore the location, theme, and scale of 3016 groups relating to places in Greater London. Firstly, we address the quantitative and qualitative methodological challenges that we faced to identify the groups and ground them geographically. Secondly, we analyse the scale of the toponyms in the group names, which are predominantly linked to London’s suburbs. Thirdly, we study the spatial distribution of groups, both overall and by specific types, in relation to the socio-demographic characteristics of residents at the borough level. Through correlation and robust regression analyses, the presence and activity of groups are linked to a relatively older, non-deprived, and non-immigrant population living in less dense areas, with high variability across different group types. These results portray place-named Facebook groups as communication infrastructure skewed towards more banal interactions and places in Greater London’s outlying boroughs. This research is among the first to explore and visualize the urban geographies of Facebook groups at a metropolitan scale, showing the extent, nature and locational tendencies of large-scale social media use as increasingly ordinary aspects of how people come to know, experience, live and work in cities.

## Data

The main dataset is `data/facebook_city_data/facebook_city_data_groups.csv`, a table 
containing 3132 place-named Facebook groups in Greater London, collected between 2020 and 2022.
The data is also available in Excel format. The folder contains a data dictionary.
This dataset was collected through web scraping from Google and manual searches on Facebook.

Some redactions have been made from the main dataset. These are names, emails, telephone numbers and addresses relating to Facebook group administrators, moderators, founders, or others identified purely in connection with the Facebook group (e.g. photo/video contributors, other non-professional volunteers). Other names, emails, telephone numbers and addresses relating to businesses, governmental and non-governmental organisations, societies, celebrities, professionals, politicians, proprietors, and office holders have been retained in the dataset.

Derived data are stored in folder `data/analysis`.

The dataset has been assembled with reference to the Association of Internet Researchers (AoIR) Ethical Guidelines 3.0: https://aoir.org/reports/ethics3.pdf

## Code

For data protection issues, we cannot release fully reproducible code and data. However, the complete 
R and Python code is available in this folder. The Python code is a Google Search scraper. 
The analysis of data is entirely in the R file `fb_groups_analysis.Rmd`.

## Team

* Dr **Scott Rodgers** is Reader in Media and Geography at Birkbeck, University of London. He is a qualitative researcher whose work specialises in the relationships of media and cities and the geographies of communication. Scott is the Principal Investigator on the project.
* Dr **Andrea Ballatore** is Lecturer in Geographic Data Science at King's College London. His research focuses on spatial analysis, GIS, social media analytics and Internet geography. Andrea is a Co-Investigator on the project.
* Dr **Susan Moore** is Associate Professor in Urban Development and Planning at University College London. Her research focuses on urban development and governance, including the role of social media platforms in relation to local urban change. Susan is a Co-Investigator on the project.
* Dr **Liam McLoughlin** is a Lecturer in Communication and Media at the University of Liverpoool. His work spans qualitative and quantitative approaches, focusing on the study of internet cultures, content moderation practices, online harms and politics. Liam was the lead Field Researcher for the project.

## License

This work is licensed under CC BY-NC-ND 4.0. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/

## Acknowledgments

This work is part of the "Localising Content Governance" project, funded by Facebook Research in 2020.
Project URL: https://www.bbk.ac.uk/school/creative-arts-culture-and-communication/research/localising-content-governance

## Citation

If you find this data or code helpful, please consider citing our paper:

```
Ballatore, A., Rodgers, S., McLoughlin, L., and Moore, S. (2024) "Facebook city: Place-named groups as urban communication infrastructure in Greater London", Environment and Planning B: Urban Analytics and City Science.
```

## Contact

Andrea Ballatore (King's College London) https://aballatore.space

Feel free to open an issue if you have any questions.
