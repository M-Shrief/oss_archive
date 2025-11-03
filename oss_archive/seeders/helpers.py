### 
from oss_archive.utils.logger import logger
from oss_archive.database.models import OSS as OSSModel, Owner as OwnerModel, Category as CategoryModel
from oss_archive.schemas.general import ActionsEnum

def should_apply_action_on_oss(owner: OwnerModel, repo_name: str | None)-> bool:
    """Decide should we apply the owner.actions on the OSS or not."""
    if repo_name is None:
        return False

    should_download = False
    # Filter seeded repos depending on meta_item.actions && meta_item.actions_on
    match owner.actions:
        case ActionsEnum.ArchiveAll: # Get all repos without filtering
            should_download = True
        case ActionsEnum.ArchiveOnly:
            if repo_name in owner.actions_on:
                should_download = True
        case ActionsEnum.ArchiveAllExcept:
            if repo_name not in owner.actions_on:
                should_download = True
    
    return should_download

