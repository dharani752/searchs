from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, F
from .models import User, Paragraph, WordIndex
from .Serilizers import UserSerializer, ParagraphSerializer, WordIndexSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            content = request.data.get('content')
            if not content:
                return Response({"detail": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user  # Assuming the user is authenticated
            paragraphs = content.split('\n\n')
            print('hello')
            print(paragraphs)

            for para in paragraphs:
                print(f"Creating paragraph: {para[:30]}...")  # Print first 30 characters of paragraph
                paragraph = Paragraph(content=para, user=user)
                paragraph.save()
                words = para.split()
                for word in words:
                    word = word.lower()
                    print(f"Indexing word: {word} for paragraph ID: {paragraph.id}")
                    WordIndex.objects.create(word=word, paragraph=paragraph)

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"detail": "An error occurred while creating the paragraph"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request, word):
    try:
        word = word.lower()
        print(f"Searching for word: {word}")
        word_index_data = WordIndex.objects.all()
        word_index_serializer = WordIndexSerializer(word_index_data, many=True)
        print(f"WordIndex Data: {word_index_serializer.data}")

    # Check if the word exists in WordIndex
        word_entries = WordIndex.objects.filter(word=word)
        print(f"Word entries: {word_entries}")
        # Check if the word exists in WordIndex
        word_entries = WordIndex.objects.filter(word=word)
        
        if not word_entries.exists():
            return Response({"detail": "Word not found in the index"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch paragraphs that contain the word and sort them by the count of occurrences
        paragraphs = word_entries.values('paragraph').annotate(count=Count('id')).order_by('-count')[:10]
        print(f"Paragraphs with count: {paragraphs}")

        result = []
        for para in paragraphs:
            paragraph_id = para['paragraph']
            print(f"Fetching paragraph with ID: {paragraph_id}")
            paragraph = Paragraph.objects.get(id=paragraph_id)
            result.append({
                'id': paragraph.id,
                'content': paragraph.content
            })

        print(f"Search results: {result}")

        return Response(result)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"detail": "An error occurred during the search"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
