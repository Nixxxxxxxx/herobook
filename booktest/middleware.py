import json


class JsonMiddleware(object):
    def __init__(self, get_response):
        # web服务器启动执行的代码
        self.get_response = get_response

    def __call__(self, request):
        # view视图执行之前，执行的代码
        if request.content_type == 'application/json':
            request.json = json.loads(request.body)

        response = self.get_response(request)

        return response