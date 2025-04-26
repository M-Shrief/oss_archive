"""
    Request and Reponse schemas to be used by the os_software router.
"""
###
from oss_archive.schemas import os_software, meta_list, meta_item, license

# Limit inheritance and seperate Reponses schemas even if they're basically the same

class GetOSSoftwaresItemRes(
    os_software.DescriptiveSchema,
    ):
    meta_list: meta_list.MinimalSchema
    meta_item: meta_item.MinimalSchema
    license: license.MinimalSchema

class GetOSSoftwareByIDRes(
    os_software.DescriptiveSchema,
    ):
    meta_list: meta_list.MinimalSchema
    meta_item: meta_item.MinimalSchema
    license: license.MinimalSchema
