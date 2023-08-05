class ValidationError(ValueError):
    pass

def validate(types, raise_on_failure=False, return_failures=False):
    # Make sure they give us a dict
    if not isinstance(types, dict):
        raise ValueError("Types must be of type dict")

    # Make sure each key is a valid type
    for key in types.keys():
        if not type(key) is type:
            raise TypeError("A valid type must be supplied")

    # Check to make sure the type of the value is the same as the given type
    # AKA validate
    failed = []
    for given_type, value in types.items():
        if not type(value) is given_type:
            # Failed Validation

            if return_failures:
                failed.append((given_type, value))
                continue
            if raise_on_failure:
                raise ValidationError("Validation Failed: type of given value (%s) does not match the given type (%s)" % (type(value), given_type))
            # Default behavior
            return False
    if failed:
        return failed
    return True
