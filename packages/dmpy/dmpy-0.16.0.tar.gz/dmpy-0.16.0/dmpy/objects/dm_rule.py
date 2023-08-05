import attr


def convert_to_list(val):
    if val is None:
        return []
    if isinstance(val, str):
        return [val]
    if None in val:
        raise ValueError('deps may not include None type: {}'.format(val))
    return list(val)


@attr.s(slots=True)
class DMRule(object):
    target = attr.ib()
    deps = attr.ib(attr.Factory(list), convert=convert_to_list)
    recipe = attr.ib(attr.Factory(list), convert=convert_to_list)

    @target.validator
    def not_none(self, attribute, value):
        if value is None:
            raise ValueError("target may not be None type")

    @property
    def name(self):
        return self.recipe[0].lstrip().partition(' ')[0]
