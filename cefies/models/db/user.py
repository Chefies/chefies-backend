from fireo.typedmodels import TypedModel


class User(TypedModel):
    name: str
    email: str
    avatar: str
    password: str

    class Meta:
        collection_name = "users"
