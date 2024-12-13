from account.serializers import SignUpSerializer, MetaAiSerializer
import replicate
import re
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def Ai_Assistant(request):
    data = request.data
    serialize = MetaAiSerializer(data=data)
    if serialize.is_valid():
        ask = serialize.validated_data['ask']
        client = replicate.Client(api_token=settings.META_API_TOKEN)
        output = client.run(
            'meta/meta-llama-3-8b-instruct',
                input={'prompt': ask, "max_token": 512}
        )
        final_response = ''.join(output)
        cleaned_text = re.sub(r'\s+', ' ', final_response).strip()
        return Response({'answer': cleaned_text}, status=status.HTTP_200_OK)
    return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)