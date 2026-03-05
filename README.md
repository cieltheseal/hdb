This project aims to detail price trends of HDBs (BTO and resales) across time and areas in Singapore.
Resale data from 1990 is available while BTO data is only available from 2008.
Regions are identified based on 2019 planning areas.

Sources: 
1) 2019 Planning Areas: https://data.gov.sg/datasets/d_8594ae9ff96d0c708bc2af633048edfb/view
2) HDB Resale Prices: https://data.gov.sg/collections/189/view
3) BTO Prices: https://data.gov.sg/datasets/d_2d493bdcc1d9a44828b6e71cb095b88d/view

Instructions:

The raw csvs are stored in the "raw" subfolder, or can be downloaded from the above links.

The "area", "bto", and "resale" scripts transform the corresponding datasets for use with Tableau.
The transformed datasets are stored in the "data" subfolder"

The dashboard may be found at https://public.tableau.com/app/profile/cieltheseal/viz/HDB_17723595916870/HDBPriceMaps?publish=yes.
A local copy can be found in the "outputs" subfolder.

Notes:

Most "Towns" from both datasets directly correspond to planning areas so are assigned accordingly.

"Central Area" from resale data corresponds to a set of planning areas, namely "Rochor", "Downtown Core", "Outram", and "Singapore River".
I have manually assigned the relevant resale data to the appropriate planning area based on the location of the street. 
A simpler approach would have been to group the planning areas together as "Central Area", but this is less granular.

The "Kallang/Whampoa" area from resale data is assigned to the "Kallang" planning area.

Todo (In no particular order): 
1) Adjust for inflation (Need to consider which measure to use)
2) Rental prices
3) Statistical analyses of contributory factors in pricing
