from faker import Faker

fkr = None


def get_faker() -> Faker:
    global fkr
    if not fkr:
        fkr = Faker()
    return fkr
