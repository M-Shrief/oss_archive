###
from oss_archive.schemas import meta_item, meta_list, os_software


class GetMetaItemRes(
    meta_item.DescriptiveSchema,
    ):
    meta_list: meta_list.MinimalSchema

class GetMetaItemByIDRes(
    meta_item.DescriptiveSchema,
    ):
    meta_list: meta_list.MinimalSchema
    os_softwares: list[os_software.MinimalSchema]