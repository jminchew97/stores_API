from marshmallow import Schema, fields

'''What is the definition of an item?'''
class ItemSchema(Schema):
    """Schema used to create an item\n
    dump_only=id(str)\n
    required=name(str),price(float), store_id(str)"""
    # dump_only is data that is only required to be returned in a responsed from an endpoint
    id = fields.Str(dump_only=True)

    #Required data send to an endpoint
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)