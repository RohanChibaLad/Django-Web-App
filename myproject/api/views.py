from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Author, NewsStory, NewsAgency
import json

#NewsStory.objects.all().delete()


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({"error": "Both username and password are required."}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials."}, status=401)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logout successful!"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def post_story(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return JsonResponse({"error": "Username and password are required."}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            headline = request.POST.get('headline')
            category = request.POST.get('category')
            region = request.POST.get('region')
            details = request.POST.get('details')

            if not all([headline, category, region, details]):
                return JsonResponse({"error": "Incomplete data provided."}, status=400)

            author = Author.objects.get(user=user)
            story = NewsStory.objects.create(
                headline=headline,
                category=category,
                region=region,
                details=details,
                author=author
            )
            return JsonResponse({"message": "Story posted successfully."}, status=201)
        else:
            return JsonResponse({"error": "Authentication failed."}, status=401)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def get_stories(request):
    #print(request.method)
    if request.method == 'GET':
        story_cat = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date = request.GET.get('story_date', '*')
        #print(story_cat, story_region, story_date)

        filter_conditions = {}

        if story_cat != '*':
            filter_conditions['category'] = story_cat

        if story_region != '*':
            filter_conditions['region'] = story_region

        if story_date != '*':
            filter_conditions['date__gte'] = story_date

        # Query stories based on filter conditions
        if filter_conditions:
            stories = NewsStory.objects.filter(**filter_conditions)
        else:
            # No filter conditions provided, return all stories
            stories = NewsStory.objects.all()

        # Construct JSON response
        response_data = []
        for story in stories:
            response_data.append({
                'key': story.id,
                'headline': story.headline,
                'story_cat': story.category,
                'story_region': story.region,
                'author': story.author.name,
                'story_date': str(story.story_date),
                'story_details': story.details
            })

        return JsonResponse({'stories': response_data}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_story(request, key):
    if request.method == 'DELETE':
        username = request.headers.get('Username')
        password = request.headers.get('Password')

        if not (username and password):
            return JsonResponse({'error': 'Username and password are required in headers.'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                story = NewsStory.objects.get(id=key)
                if user == story.author.user:
                    story.delete()
                    return JsonResponse({'message': 'Story deleted successfully.'}, status=200)
                else:
                    return JsonResponse({'error': 'You are not authorized to delete this story.'}, status=403)
            except NewsStory.DoesNotExist:
                return JsonResponse({'error': 'Story does not exist.'}, status=404)
        else:
            return JsonResponse({'error': 'Authentication failed.'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def register_agency(request):
    if request.method == 'POST':
        agency_name = request.POST.get('agency_name')
        url = request.POST.get('url')
        agency_code = request.POST.get('agency_code')

        # Check if agency with the given code already exists
        if NewsAgency.objects.filter(code=agency_code).exists():
            return JsonResponse({'error': 'Agency with this code already exists.'}, status=400)

        # Create new agency
        agency = NewsAgency.objects.create(name=agency_name, url=url, code=agency_code)
        return JsonResponse({'message': 'Agency registered successfully.'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_agencies(request):
    if request.method == 'GET':
        agencies = NewsAgency.objects.all()
        agency_list = []
        for agency in agencies:
            agency_list.append({
                'agency_name': agency.name,
                'url': agency.url,
                'agency_code': agency.code
            })
        return JsonResponse({'agency_list': agency_list}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)