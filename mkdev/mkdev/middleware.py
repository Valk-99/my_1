class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
      return self.get_response(request)


class StackOverflowMiddleware(BaseMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user_agent.is_mobile:
            print('It`s mobile version of site')
        elif request.user_agent.is_tablet:
            print('It`s tablet version of site')
        else:
            print('It`s pc version of site')
        return None

    def process_request(self, request):
        if request.user_agent.is_mobile:
            print('It`s mobile version of site')
        else:
            print('It`s pc version of site')
        return None
