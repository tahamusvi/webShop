from .models import UserVisit
import uuid

def generate_unique_identifier():
    return str(uuid.uuid4())

class UserVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for the existence of the user identifier cookie
        user_identifier = request.COOKIES.get('user_identifier')

        if not user_identifier:
            user_identifier = generate_unique_identifier()  # Generate a unique value
            response = self.get_response(request)
            response.set_cookie('user_identifier', user_identifier)
        else:
            response = self.get_response(request)

        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')  # Get the X-Forwarded-For header value
        ip_address = ip_address.split(',')[-1].strip() if ip_address else request.META.get('REMOTE_ADDR', '')  # Get the last IP address from the list


        # Create and save an instance of the UserVisit model
        user_visit = UserVisit(
            user_identifier=user_identifier,
            ip_address=ip_address,
            http_method=request.method,
            request_url=request.build_absolute_uri(),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            referred_from=request.META.get('HTTP_REFERER')
        )
        # user_visit.get_user_location()
        user_visit.save()

        return response