from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def custom_view(request):
    # Your custom logic here
    data = {"message": "Hello from a model-less view!"}
    return Response(data)
