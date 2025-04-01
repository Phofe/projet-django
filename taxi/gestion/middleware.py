class DebugUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print(f"User groups: {list(request.user.groups.all())}")
            print(f"Has gestionnaire attr: {hasattr(request.user, 'gestionnaire')}")
        return self.get_response(request)