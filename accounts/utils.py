from accounts.models import AdminProfile, Franchisor, Franchisee

def get_user_role(user):
    """Returns the role type of the logged-in user."""
    if AdminProfile.objects.filter(user=user).exists():
        return "admin"
    elif Franchisor.objects.filter(user=user).exists():
        return "franchisor"
    elif Franchisee.objects.filter(user=user).exists():
        return "franchisee"
    else:
        return "unknown"
