# Seeders

There's multiple ways to seed the data from json files to the database while getting the meta item data from its source (github,codeberg,...etc). 

There's mutliple ways to have fast speed in this initial seed operation, but more importantly we need to prioritize correctness. As this first step will be key for the upcoming steps to clone and archive the the data we want and to maintain it.

Rules:
- JSON files that we use to keep track of Meta Lists and Meta Items **shouldn't be modified**, and the don't require cleaning.
- All seeding operation should be decoupled from other seed operations, and we'll limit the use of metadata when seeding. And Especially the seeding operation for MetaItem and its related open-source software is decoupled from each other and shouldn't be seeded together.
    - For instance seeded_repos && not_seeded_repos fields in meta_item will be deleted, because we don't need it in seed operations as we don't want to couple the meta_item with os_software seeding operation. As we don't want to update meta_item's fields every time we add/delete a new OSS.
    - And we don't use the meta_item's JSON data when seeding its OSSs but we query the meta_item's data from the Database. 

Overview of the flow:
1 - First we add/insert all meta_list from its JSON file metadata to the database, doing it one by one while checking if it already exists or not in the databse -- 
2 - Then, we add/insert all licenses from its JSON file to the database
3 - Then we start metalist and start to add a meta item by item.
    3.1 - we get the meta item's external data from its source, then we insert it to the database. 
4 - We seed meta_item's open-source softwares, by getting meta_item's data from our database, then we get its repos data from meta_item's external source, and we add on OSS by one.
