# Schemas

We'll have a directory that includes all schema files for the project entities, and every file will include only the schemas for this entity without its relations/populated fields from other schemas to prevent circular dependecy errors.

Every field of the entity schema will be made into a class, so that we reuse it, and remove the copy/paste duplication, and to standardize the schema.

Every entity will have 4 types of schemas:
- FullSchema: a schema that have every field corresponding the DB model, without it's relations.
- DescriptiveSchema: a schema that have the important fields for the entity without unneccassery fields like timestamps, and Private fields like passwords.
- MinimalSchema: a schema that shows the most minimal amount of data of the entity, used for populated fields for the entity.
- JSONschema: a schema for the json file(s) that the entity use.