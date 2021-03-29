customers = [
    {"id": 2, "name": "fghi"},
]


contacts = [
    {"id": 1, "customer": 2, "contact_name": "aaaaaaa"},
    {"id": 2, "customer": 2, "contact_name": "bbbbbbb"},
]


addresses = [
    {"id": 1, "customer": 2, "address": "xxxxxxx"},
    {"id": 2, "customer": 2, "address": "yyyyyyy"},
    {"id": 3, "customer": 2, "address": "zzzzzzz"},
]


mocked_results = {
    "customers": customers,
    "contacts": contacts,
    "addresses": addresses,
}


class MockedProvider:
    def __init__(self, provider_name):
        self.provider_name = provider_name

    def resolve(self, query):
        source, params = query
        return mocked_results.get(source)
