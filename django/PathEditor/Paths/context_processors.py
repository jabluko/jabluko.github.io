from .models import UserProfile, Background

def background_context(request):
    """Dodaje URL wybranego tła do kontekstu szablonu."""
    background_url = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.select_related('selected_background').get(user=request.user)
            if profile.selected_background and profile.selected_background.image:
                background_url = profile.selected_background.image.url
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user)
            pass

    return {'user_selected_background_url': background_url}