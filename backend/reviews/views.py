from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
from django.http import  JsonResponse
from .models import Review, Progress
from .serializers import ReviewSerializer, ProgressSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Review
from .serializers import ReviewSerializer
from django.shortcuts import redirect




# reviews endpoints
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return JsonResponse(serializer.data,safe=False)

@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                data['user'] = request.user.id  

                serializer = ReviewSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
                return JsonResponse(serializer.errors, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        return JsonResponse({'error': 'Unsupported Content-Type'}, status=415)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@csrf_exempt
def review_by_id(request, id):
    print("Getting by id")
    
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)
    
    
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return JsonResponse(serializer.data, status=200)
    elif request.method == 'DELETE':
        review.delete()
        return JsonResponse({'message': 'Review deleted successfully'}, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

#Progress endpoints
@csrf_exempt
def progress_detail(request, progress_id):
    print("Progress method...")
    try:
        progress = Progress.objects.get(id=progress_id)
    except Progress.DoesNotExist:
        return JsonResponse({'error': 'Progress not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': progress.id,
            'user': progress.user.username,
            'course': progress.course,
            'percentage': progress.percentage,
            'updated_at': progress.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    elif request.method == 'DELETE':
        progress.delete()
        return JsonResponse({'message': 'Progress deleted successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
