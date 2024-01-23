# Facebook City dataset

Data Dictionary for CSV/XLSX File

- Table: List of Facebook place groups in Greater London
- Geographic scope: Greater London
- Temporal scope: 2020-2022
- Status: Complete and manually verified as of 2022
- Entries: 3132

Refer to the article for more details about the column meaning.

| Column Name              | Description |
|--------------------------|-------------|
| group_uid                | Facebook unique identifier for each group |
| group_url                | URL of the Facebook group |
| found_via                | Source or method through which the group was discovered |
| group_type_manual        | Manually assigned group type, categorisation by research team |
| london_wide              | Flag indicating if the group is London-wide |
| sub_london               | Flag indicating if the group is sub-London |
| borough_name             | Name of the London borough associated with the group |
| ward_gss                 | GSS code for the electoral ward (UK administrative geography) |
| lat_long_google_maps     | Latitude and longitude coordinates from Google Maps, if point |
| osm_ids_merged           | OpenStreetMap (OSM) IDs of object associated with the group |
| large_object_osm_id      | OSM ID for a large object associated with the group |
| place_name_manual        | Manually assigned place name |
| recoded                  | Flag indicating if the data has been manually recoded |
| fb_group_name            | Name of the Facebook group |
| fb_description           | Description of the Facebook group (from Facebook) |
| fb_privacy               | Privacy settings of the Facebook group |
| fb_found                 | Flag indicating if the group is found on Facebook |
| creation_year            | Year the Facebook group was created |
| creation_yymm            | Year and month the Facebook group was created |
| creation_date            | Year, month, and day the Facebook group was created |
| fb_place                 | Place associated with the Facebook group |
| fb_group_type            | Type of the Facebook group (generic categories by Facebook) |
| stats_collection_date    | Date when statistics were last collected (2020-2022) |
| members_n                | Number of group members |
| lastmonth_posts          | Number of posts in the last month |
| dailyposts               | Daily posts count |
| group_rules_str          | Group rules in string format |
| posts_per_member         | Average posts per member |
| size                     | Size category of the group (small, medium, large, huge) |
| activity_level           | Overall activity level of the group |
| posts_per_1kmember       | Posts per 1,000 members |
| activity_per_user_level  | Activity level per user |
| geoscale_l2              | Geoscale level 2 information |
| geoscale                 | Geoscale information (level and type) |
| geoscale_level           | Geoscale level (0-6) |
| geoscale_type            | Type of geoscale (London-wide, Subregion, Borough, Suburb, Neighbourhood, Park, Point of interest) |
