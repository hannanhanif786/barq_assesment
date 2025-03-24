from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from rest_framework import status
from django.contrib.auth import authenticate
from markflow.models import Document, Tags
from rest_framework_simplejwt.tokens import RefreshToken
from markflow.serializer import DocumentSerializer, TagSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class DocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        updated_at = request.query_params.get("updated", None)
        created_at = request.query_params.get("created", None)
        tag_id = request.query_params.get("tag_id", None)
        id = request.query_params.get("id", None)

        filters = Q()

        # Apply filters based on parameters
        if updated_at:
            filters &= Q(updated_at__icontains=updated_at)
        if created_at:
            filters &= Q(created_at__icontains=updated_at)
        if tag_id:
            filters &= Q(tags_id=tag_id)

        if id:
            try:
                document = Document.objects.get(id=id)
                serializer = DocumentSerializer(document)
            except Document.DoesNotExist:
                return Response({"error": "document not found"}, 404)
        else:
            queryset = Document.objects.filter(filters)
            serializer = DocumentSerializer(queryset, many=True)

        return Response({"data": serializer.data})
    
    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Data saved Successfully"})
    

    def put(self, request):
        document_id = request.GET.get('id')
        if not document_id:
            return Response({"error": "selecet document id for deletion"}, 404)
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "document not found for updation"}, 404)
        
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Data Updated Successfully"})
    
    def delete(self, request):

        if not request.GET.get("id"):
            return Response(
                {"message": "Select Document id for deletion."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            document = Document.objects.get(id=request.GET.get("id"))
            document.delete()
            return Response({"message": f"document has been deleted"})

        except Document.DoesNotExist:
            return Response(
                {"message": "Document not found."}, status=status.HTTP_400_BAD_REQUEST
            )


