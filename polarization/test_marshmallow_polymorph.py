import marshmallow
import marshmallow.fields
from marshmallow_oneofschema import OneOfSchema


class Foo:
    def __init__(self, foo):
        self.foo = foo


class Bar:
    def __init__(self, bar):
        self.bar = bar


class FooSchema(marshmallow.Schema):
    foo = marshmallow.fields.String(required=True)

    @marshmallow.post_load
    def make_foo(self, data, **kwargs):
        return Foo(**data)


class BarSchema(marshmallow.Schema):
    bar = marshmallow.fields.Integer(required=True)

    @marshmallow.post_load
    def make_bar(self, data, **kwargs):
        return Bar(**data)


class MyUberSchema(OneOfSchema):
    type_schemas = {"foo": FooSchema, "bar": BarSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Foo):
            return "foo"
        elif isinstance(obj, Bar):
            return "bar"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


MyUberSchema().dump([Foo(foo="hello"), Bar(bar=123)], many=True)
# => [{'type': 'foo', 'foo': 'hello'}, {'type': 'bar', 'bar': 123}]

MyUberSchema().load(
    [{"type": "foo", "foo": "hello"}, {"type": "bar", "bar": 123}], many=True
)
# => [Foo('hello'), Bar(123)]

# By default get_obj_type() returns obj.__class__.__name__, so you can just reuse that to save some typing:

"""
class MyUberSchema(OneOfSchema):
    type_schemas = {"Foo": FooSchema, "Bar": BarSchema}

# You can customize type field with type_field class property:

class MyUberSchema(OneOfSchema):
    type_field = "object_type"
    type_schemas = {"Foo": FooSchema, "Bar": BarSchema}


print(MyUberSchema().dump([Foo(foo="hello"), Bar(bar=123)], many=True))
# => [{'object_type': 'Foo', 'foo': 'hello'}, {'object_type': 'Bar', 'bar': 123}]

# You can use resulting schema everywhere marshmallow.Schema can be used, e.g.

import marshmallow as m
import marshmallow.fields as f


class MyOtherSchema(m.Schema):
    items = f.List(f.Nested(MyUberSchema))
"""
