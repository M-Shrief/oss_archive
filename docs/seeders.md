# Seeders

There's multiple ways to seed the data from json files to the database while getting the meta item data from its source (github,codeberg,...etc). 

There's mutliple ways to have fast speed in this initial seed operation, but more importantly we need to prioritize correctness. As this first step will be key for the upcoming steps to clone and archive the the data we want and to maintain it.

Overview of the flow:
1 - First we add/insert all meta_list from its JSON file metadata to the database
2 - Then, we add/insert all licenses from its JSON file to the database
3 - Then we start by the prioritized metalist (by levels), and start to add a meta item by item.
    
    3.1 - we get the meta item's external data from its source, then we insert it to the database. 
    3.2 if the operation succeded, we check is_seeded=true, and follow on.
    3.3 - we get meta item's repos data from its external source, we add on OSS by one.
    3.4 - we check if every insert is successfull if it was, we add the OSS name to seeded_repos: [str]. If it wasn't successfull, we add it's name to not_seeded_repos: [str].
    3.5 we then update the item in the JSON file, 
