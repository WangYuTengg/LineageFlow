from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .serializer import CreateRepositorySerializer
from myapp.serializers import FilesSerializer
from myapp.models import Files
import logging

# Set up logging
logger = logging.getLogger(__name__)


class OnboardingView(APIView):
    #{"username": "admin", "repo_name": "ADMIN", "default_branch": "master", "storage_bucket_name": "test"}
    def post(self, request):
        serializer = CreateRepositorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                repo = serializer.save()
                logger.info(
                    "Repo Created Successfully. Data: %s",
                    serializer.data,
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                logger.error("Validation error: %s", e.detail)
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error("Serializer validation failed. Errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)