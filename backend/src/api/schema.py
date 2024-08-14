from flask_marshmallow import Marshmallow, Schema

ma = Marshmallow()


class EmptySchema(Schema):
    pass
