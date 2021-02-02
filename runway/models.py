class Property(object):

    def ___init__(self, prefix, product, class_name, text):
        self.property_name = prefix + "." + product


class TestRegisterParameters(object):
    parameters = [
        {"email": {"prefix": "vesync.account.email"}},
        {"password": {"prefix": "vesync.account.password"}},
    ]
