
from pydantic import Field, BaseModel
from typing import Annotated
# ###
from oss_archive.schemas import owner, category, general



class GetOwnerByID_Res(
    owner.DescriptiveSchema,
    ):
    pass
    # main_category: category.MinimalSchema

class CreatingOwner_Req(
    owner.UsernameField,
    owner.NameField,
    owner.TypeField,
    owner.SourceField,
    owner.OtherSourcesField,
    owner.ActionsField,
    owner.ActionsOnField,
    owner.HTMLURLField,
    general.PriorityField,
    general.ReviewedField,
    # Relations
    general.MainCategoryKeyField,
):
    pass

class CreatingOwner_Res(
    owner.FullSchema
):
    pass

class CreateOwners_Req(
    BaseModel
    ):
    owners: Annotated[list[CreatingOwner_Req], Field()]

class CreateOwners_Res(
    BaseModel
    ):
    new_owners: Annotated[list[owner.FullSchema], Field()]
    already_exists: Annotated[list[str], Field()]


class UpdatingOwner_Req(
    owner.UsernameField_Optional,
    owner.NameField,
    owner.TypeField_Optional,
    owner.SourceField_Optional,
    owner.OtherSourcesField_Optional,
    owner.ActionsField_Optional,
    owner.ActionsOnField_Optional,
    owner.HTMLURLField_Optional,
    general.PriorityField_Optional,
    general.ReviewedField_Optional,
    # Relations
    general.MainCategoryKeyField_Optional,
):
    pass
