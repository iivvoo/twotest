def create_request(method, *a, **b):
    """ setup a request with an anonymous user """
    from django.contrib.auth.models import AnonymousUser
    from django.test.client import RequestFactory

    if method == "GET":
        request = RequestFactory().get(*a, **b)
    elif method == "POST":
        request = RequestFactory().post(*a, **b)
    elif method == "PUT":
        request = RequestFactory().put(*a, **b)
    elif method == "DELETE":
        request = RequestFactory().delete(*a, **b)
    request.user = AnonymousUser()
    request.session = {}
    return request