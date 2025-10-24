from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Comment
from news.models import Berita
from .forms import CommentForm


def show_json(request, news_id):
    """Return all comments for a news item as JSON."""
    try:
        news = get_object_or_404(Berita, id=news_id)
        comments = Comment.objects.filter(news=news).select_related('user').order_by('-created_at')
        
        data = [
            {
                "id": c.id,
                "user": c.user.username,
                "content": c.content,
                "is_edited": c.is_edited,
                "date": c.created_at.strftime("%d %b %Y, %H:%M"),
                "is_owner": c.user == request.user if request.user.is_authenticated else False,
            }
            for c in comments
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url='/login/')  # Redirect ke login jika tidak authenticated
@require_POST
def add_comment(request, news_id):
    """Add a new comment via AJAX POST request."""
    try:
        news = get_object_or_404(Berita, id=news_id)
        
        content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({"error": "Comment cannot be empty."}, status=400)
        
        # Create comment
        comment = Comment.objects.create(
            user=request.user,
            news=news,
            content=content
        )
        
        return JsonResponse({
            "success": True,
            "message": "Comment added successfully.",
            "comment": {
                "id": comment.id,
                "user": comment.user.username,
                "content": comment.content,
                "is_edited": comment.is_edited,
                "date": comment.created_at.strftime("%d %b %Y, %H:%M"),
                "is_owner": True,
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url='/login/')
@require_POST
def edit_comment(request, comment_id):
    """Edit an existing comment."""
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Check ownership
        if comment.user != request.user:
            return JsonResponse({"error": "You don't have permission to edit this comment."}, status=403)
        
        new_content = request.POST.get("content", "").strip()
        
        if not new_content:
            return JsonResponse({"error": "Comment cannot be empty."}, status=400)
        
        # Update comment if content changed
        if comment.content != new_content:
            comment.content = new_content
            comment.is_edited = True
            comment.save()
        
        return JsonResponse({
            "success": True,
            "message": "Comment updated successfully.",
            "comment": {
                "id": comment.id,
                "user": comment.user.username,
                "content": comment.content,
                "is_edited": comment.is_edited,
                "date": comment.created_at.strftime("%d %b %Y, %H:%M"),
            }
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url='/login/')
@require_POST
def delete_comment(request, comment_id):
    """Delete a comment."""
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Check ownership
        if comment.user != request.user:
            return JsonResponse({"error": "You don't have permission to delete this comment."}, status=403)
        
        comment.delete()
        
        return JsonResponse({
            "success": True,
            "message": "Comment deleted successfully."
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)