"""
    Request and Reponse schemas to be used by the os_software router.
"""
from pydantic import BaseModel, Field
from typing import Annotated
###
from oss_archive.schemas import oss,  general

class GetOSSByID_Res(
    oss.DescriptiveSchema
    ):
    pass
    # category: category.MinimalSchema

class CreateOSS_Req(
    oss.RepoNameField,
    oss.DescriptionField,
    oss.TopicsField,
    oss.IsMirroredField,
    oss.DevelopmentStatusField,
    oss.DevelopmentStartedAtField,
    oss.HTMLURLField,
    oss.CloneURLField,
    general.MainCategoryKeyField,
    general.OwnerUsernameField,
    general.PriorityField,
    general.ReviewedField,
    ):
    pass

class CreateOSS_Res(
    oss.FullSchema
    ):
    pass

class CreateManyOSS_Req(
    BaseModel
    ):
    oss_list: Annotated[list[CreateOSS_Req], Field()]

class CreateManyOSS_Res(
    BaseModel
    ):
    new_oss_list: Annotated[list[oss.FullSchema], Field()]
    already_exists: Annotated[list[str], Field()]



class UpdateOSS_Req(
    oss.RepoNameField_Optional,
    oss.DescriptionField_Optional,
    oss.TopicsField_Optional,
    oss.IsMirroredField_Optional,
    oss.DevelopmentStatusField_Optional,
    oss.DevelopmentStartedAtField_Optional,
    oss.HTMLURLField_Optional,
    oss.CloneURLField_Optional,
    general.MainCategoryKeyField_Optional,
    general.OwnerUsernameField_Optional,
    general.PriorityField_Optional,
    general.ReviewedField_Optional,
):
    pass