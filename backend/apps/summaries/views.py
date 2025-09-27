from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SummarySerializer
from .models import Summary

class SummaryListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = Summary.objects.filter(report__owner=request.user).order_by("-created_at")
        serializer = SummarySerializer(qs, many=True)
        return Response(serializer.data)
