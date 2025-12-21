from django.db.models import Exists, OuterRef
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import base64
import uuid

from .models import Following, CabangOlahraga
from .forms import FollowingForm, OlahragaForm

from main.models import CustomUser
from main.forms import CustomUserUpdateForm
from event.models import Event
from news.models import Berita
from comment.models import Comment
from profil_atlet.models import Atlet

# Create your views here.
def createSportOnStart():
    for atlet in Atlet.objects.all():
        discipline = atlet.discipline
        if not CabangOlahraga.objects.filter(name=discipline).exists():
            CabangOlahraga.objects.create(name=discipline)

def checkNewsCabangOlahraga():
    for berita in Berita.objects.all():
        for cabor in CabangOlahraga.objects.all():
            if cabor.name.lower() in berita.title.lower() or cabor.name.lower() in berita.content.lower():
                berita.cabangOlahraga = cabor
                berita.save()
                break

def is_admin(user):
    return user.is_superuser

def getListOfEvents(user):
    createSportOnStart()
    followed_sports = Following.objects.all().filter(user=user, cabangOlahraga=OuterRef('cabangOlahraga'))
    return (Event.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

def getListOfNews(user):
    createSportOnStart()
    checkNewsCabangOlahraga()
    followed_sports = Following.objects.all().filter(user=user, cabangOlahraga=OuterRef('cabangOlahraga'))
    return (Berita.objects.annotate(is_followed=Exists(followed_sports)).order_by('-is_followed', '-created_at'))

@login_required
@require_POST
@csrf_exempt
def unfollow(request, follow_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            follow = Following.objects.get(id=follow_id, user=request.user)
            sport_name = follow.cabangOlahraga.name
            sport_id = follow.cabangOlahraga.id
            follow.delete()
            
            return JsonResponse({
                'success': True,
                'sport_id': sport_id,
                'sport_name': sport_name
            }, status=400)
        except Following.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Follow not found'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    }, status=400)

def createCabangOlahraga(request):
    if (request.method == 'GET'):
        form = OlahragaForm()
        context = {'form': form,'page_title': 'Add Sport'}
        return JsonResponse(context)
    else:
        form = OlahragaForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect('main:show_main')
        
@login_required
def profilePage(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'update_profile' in request.POST or request.FILES:
            try:
                custom_user = CustomUser.objects.get(user=request.user)
                form = CustomUserUpdateForm(request.POST, request.FILES, instance=custom_user)
                
                if form.is_valid():
                    updated_user = form.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Profile updated successfully',
                        'data': {
                            'name': updated_user.name,
                            'picture': updated_user.get_picture_url() if updated_user.picture else None
                        }
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Validation failed',
                        'errors': form.errors
                    }, status=400)
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'User profile not found'
                }, status=404)
        
        form = FollowingForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            
            return JsonResponse({
                'success': True,
                'follow_id': str(follow.id),
                'sport_id': str(follow.cabangOlahraga.id),
                'sport_name': follow.cabangOlahraga.name
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form data'
            }, status=400)
    
    elif request.method == "POST":
        form = FollowingForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user = request.user
            follow.save()
            return redirect('profile')
    
    else:
        form = FollowingForm()
        already_chosen = Following.objects.filter(user=request.user).values_list('cabangOlahraga', flat=True)
        form.fields['cabangOlahraga'].queryset = CabangOlahraga.objects.exclude(id__in=already_chosen)
        
        try:
            currentUser = CustomUser.objects.get(user=request.user)
        except CustomUser.DoesNotExist:
            currentUser = CustomUser.objects.create(
                user=request.user,
                username=request.user.username,
                name=request.user.username
            )
        
        profilePicture = currentUser.picture if currentUser.picture else None
        userId = request.user.id
        name = currentUser.name if currentUser.name else request.user.username
        username = currentUser.username
        
        following = Following.objects.filter(user=request.user)
        comment = Comment.objects.filter(user=request.user)
        event = Event.objects.filter(creator=request.user)
        news = Berita.objects.filter(author=request.user)

        threeRecentActivity = list(comment) + list(event)
        threeRecentActivity.sort(key=lambda x: x.created_at, reverse=True)
        threeRecentActivity = threeRecentActivity[:3]
        recentActivity = []
        for activity in threeRecentActivity:
            recentActivity.append({
                "object": activity,
                "type": activity.__class__.__name__,
                "description": activity.title if hasattr(activity, 'title') else activity.content,
                "date": activity.created_at.strftime("%Y-%m-%d")
            })

        followingCount = following.count()
        commentCount = comment.count()
        eventCount = event.count()
        is_admin = request.user.is_superuser
        profile_form = CustomUserUpdateForm(instance=currentUser)

        return render(request, "profilePage.html", {
            "form": form,
            "profile_form": profile_form,
            "profilePicture": profilePicture,
            "user": userId,
            "name": name,
            "username": username,
            "following": following,
            "followingCount": followingCount,
            "commentCount": commentCount,
            "eventCount": eventCount,
            "is_admin": is_admin,
            "recentActivity": recentActivity
        }, status=200)
        # return JsonResponse({
        #     "form": form,
        #     "profile_form": profile_form,
        #     "profilePicture": profilePicture,
        #     "user": userId,
        #     "name": name,
        #     "username": username,
        #     "following": following,
        #     "followingCount": followingCount,
        #     "commentCount": commentCount,
        #     "eventCount": eventCount,
        #     "is_admin": is_admin,
        #     "recentActivity": recentActivity
        # }, status=200)
    
def getJSONFollowing(request):
    followings = Following.objects.all()
    data = []
    for follow in followings:
        data.append({
            'id': follow.id,
            'user': follow.user.id,
            'cabangOlahraga': follow.cabangOlahraga.id
        })
    return JsonResponse({'followings': data}, status=200)


@ensure_csrf_cookie
def getJSONCabangOlahraga(request):
    cabangOlahraga = CabangOlahraga.objects.all()
    data = []
    for cabor in cabangOlahraga:
        data.append({
            'id': cabor.id,
            'name': cabor.name
        })
    return JsonResponse({'cabangOlahraga': data}, status=200) 

def getJSONCustomUser(request):
    customUser = CustomUser.objects.all()
    data = []
    for customUser in customUser:
        data.append({
            'uuid': str(customUser.uuid),
            'user': customUser.user.id,
            'join_date': customUser.join_date.isoformat(),
            'username': customUser.username,
            'name': customUser.name,
            'picture': customUser.get_picture_url() if customUser.picture else None
        })
    return JsonResponse({'customUser': data}, status=200)

def getProfilePictureURLs(user):
    profile_urls = []
    for custom_user in CustomUser.objects.all():
        if custom_user.picture:
            profile_urls.append(custom_user.get_picture_url())
    return JsonResponse({'profile_urls':profile_urls}, status=200)

@login_required
def getCurrentUser(request):
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        return JsonResponse({
            'user_id': request.user.id,
            'username': custom_user.username,
            'name': custom_user.name,
            'picture': custom_user.get_picture_url(),
            'join_date': custom_user.join_date.isoformat(),
        }, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'error': 'User profile not found'
        }, status=404)
    
def getUsers(request):
    try:
        customUser = CustomUser.objects.all()
        return JsonResponse({
            'users': [
                {
                    'user_id': user.user.id,
                    'user_uuid': str(user.uuid),
                    'username': user.username,
                    'name': user.name,
                    'picture': user.get_picture_url(),
                    'join_date': user.join_date.isoformat(),
                } for user in customUser
            ]
        }, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({
            'error': 'User profile not found'
        }, status=404)

@csrf_exempt
def profilePage2(request):
    if request.method == 'POST':
        try:
            custom_user = CustomUser.objects.get(user=request.user)
            post_data = request.POST.copy()
            file_data = request.FILES.copy()
            picture_data = request.POST.get('picture')
            
            if picture_data and picture_data.startswith('data:image'):
                try:
                    format_header, imgstr = picture_data.split(';base64,') 
                    mime_type = format_header.split(':')[-1]
                    ext = mime_type.split('/')[-1]
                    file_name = f"{request.user.username}_{uuid.uuid4().hex[:8]}.{ext}"
                    image_content = base64.b64decode(imgstr)

                    upload_file = SimpleUploadedFile(
                        name=file_name,
                        content=image_content,
                        content_type=mime_type
                    )
                    
                    file_data['picture'] = upload_file
                    
                    if 'picture' in post_data:
                        del post_data['picture']
                except Exception as e:
                    print(f"Error decoding base64 image: {e}")

            if 'update_profile' in request.POST or picture_data:
                form = CustomUserUpdateForm(post_data, file_data, instance=custom_user)
                
                if form.is_valid():
                    updated_user = form.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Profile updated successfully',
                        'data': {
                            'name': updated_user.name,
                            'picture': updated_user.get_picture_url()
                        }
                    }, status=200)
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Validation failed',
                        'errors': form.errors
                    }, status=400)

            elif 'cabangOlahraga' in request.POST:
                cabang_id = request.POST.get('cabangOlahraga')
                
                if Following.objects.filter(user=request.user, cabangOlahraga_id=cabang_id).exists():
                    return JsonResponse({'success': False, 'error': 'Already following'}, status=400)
                
                cabang = CabangOlahraga.objects.get(id=cabang_id)
                follow = Following.objects.create(user=request.user, cabangOlahraga=cabang)
                
                return JsonResponse({
                    'success': True,
                    'follow_id': str(follow.id),
                    'sport_id': str(follow.cabangOlahraga.id),
                    'user': str(follow.user.id),
                    'sport_name': follow.cabangOlahraga.name
                }, status=201)

        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    try:
        custom_user = CustomUser.objects.get(user=request.user)
        
        following_list = [
            {
                'id': str(follow.id),
                'user': follow.user.id,
                'cabangOlahraga': str(follow.cabangOlahraga.id),
                'sport_name': follow.cabangOlahraga.name
            } for follow in Following.objects.filter(user=request.user).select_related('cabangOlahraga')
        ]
        
        already_chosen_ids = Following.objects.filter(user=request.user).values_list('cabangOlahraga_id', flat=True)
        available_sports = [
            {'id': str(sport.id), 'name': sport.name} 
            for sport in CabangOlahraga.objects.exclude(id__in=already_chosen_ids)
        ]

        activities = sorted(
            list(Comment.objects.filter(user=request.user)) + 
            list(Event.objects.filter(creator=request.user)),
            key=lambda x: x.created_at, 
            reverse=True
        )[:3]

        recent_activity = []
        for activity in activities:
            act_type = activity.__class__.__name__
            desc = f'posted an event: {activity.title}' if act_type == 'Event' else 'made a comment'
            recent_activity.append({
                'type': act_type,
                'description': desc,
                'date': activity.created_at.strftime('%Y-%m-%d')
            })

        return JsonResponse({
            'success': True,
            'user': request.user.id,
            'name': custom_user.name,
            'username': custom_user.username,
            'profilePicture': custom_user.get_picture_url(),
            'join_date': custom_user.join_date.isoformat() if custom_user.join_date else None,
            'following': following_list,
            'available_sports': available_sports,
            'followingCount': len(following_list),
            'commentCount': Comment.objects.filter(user=request.user).count(),
            'eventCount': Event.objects.filter(creator=request.user).count(),
            'recentActivity': recent_activity
        }, status=200)

    except CustomUser.DoesNotExist:
        custom_user = CustomUser.objects.create(user=request.user, username=request.user.username)
        return JsonResponse({
            'success': True,
            'userId': request.user.id,
            'name': custom_user.name,
            'username': custom_user.username,
            'profilePicture': custom_user.get_picture_url(),
            'join_date': custom_user.join_date.isoformat() if custom_user.join_date else None,
            'following': following_list,
            'available_sports': available_sports,
            'followingCount': len(following_list),
            'commentCount': Comment.objects.filter(user=request.user).count(),
            'eventCount': Event.objects.filter(creator=request.user).count(),
            'recentActivity': recent_activity
        }, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def unfollow2(request, follow_id):
    try:
        follow = Following.objects.get(id=follow_id, user=request.user)
        sport_name = follow.cabangOlahraga.name
        sport_id = follow.cabangOlahraga.id
        follow.delete()
        
        return JsonResponse({
            'success': True,
            'sport_id': str(sport_id),
            'sport_name': sport_name
        }, status=200)
        
    except Following.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Follow not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)