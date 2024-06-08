class BaseForm:
    def to_dict(self):
        return self.__dict__.copy()
