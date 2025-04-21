# Database

## Tables
- meta_lists
- meta_items
- os_softwares
- licenses


### MetaList
- key: str (primary key)
- name: str
- tags: [str]
- reviewed: bool
<!-- internal timestamps -->
- created_at: datetime
- updated_at: datetime
<!-- Relations -->
- meta_items: (one-to-many relation)
- os_softwares: (one-to-many relation)

### MetaItem
- id: uuid (primary key)
<!-- Owner's data -->
- owner_username: str
- owner_name: str | None
- owner_type: OwnerType
- owner_created_at: datetime <!-- external from source -->
- owner_updated_at: datetime <!-- external from source -->
<!-- internal timestamps -->
- created_at: datetime 
- updated_at: datetime
<!-- urls -->
- html_url: str
<!-- sources -->
- source: str
- other_sources: [str]
<!-- Actions -->
- actions: ActionType
- actions_on: [str(repo_names)]
<!-- data about the repos -->
- seeded_repos: bool
- repos_count: int
- repos_updated_at: datetime
<!-- Relations -->
- meta_list_key: str (forign key)
- meta_list: (many-to-one relation)
- os_softwares (one-to-many relation)

### OSSoftware
- id: uuid (primary key)
- name: str
- fullname: str (unique)
- description: str
- topics: [str]
- reviewed: bool
- latest_version: bool
<!-- internal timestamps -->
- created_at: datetime
- updated_at: datetime
<!-- external timestamps from source -->
- oss_created_at: datetime
- oss_updated_at: datetime
<!-- urls -->
- html_url: str
- api_url: str
- clone_url: str
<!-- relations -->
- meta_list_key: str (foreign key)
- meta_list: (many-to-one relation)
- meta_item_id: uuid (foreign key)
- meta_item: (many-to-one relation)
- license_key: str (foreign key)

### License
- key: str (primary key)
- name: str
- fullname: str
<!-- urls -->
- html_url: str
- api_url: str