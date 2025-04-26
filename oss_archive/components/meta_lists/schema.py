###
from oss_archive.schemas import meta_list, meta_item


class GetAllMetaListsItemRes(
    meta_list.DescriptiveSchema
    ):
    pass

class GetMetaListByKey(
    meta_list.DescriptiveSchema
    ):
    meta_items: list[meta_item.MinimalSchema]