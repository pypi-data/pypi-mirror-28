# -*- coding: utf-8 -*-
import uuid
import jwt
import graphene
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model


def _get_user(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', '')
    if not authorization.startswith('Bearer '):
        return None
    token = authorization.split()[1]
    if not token:
        return None
    User = get_user_model()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        return User.objects.get(id=payload['id'])
    except User.DoesNotExist:
        return None


def _copy_user(user):
    result = User()
    result.username = user.username
    result.first_name = user.first_name
    result.last_name = user.last_name
    result.email = user.email
    result.last_login = user.last_login
    result.token = ''
    return result


class User(graphene.ObjectType):
    "Graphql schema for user model"
    username = graphene.Field(graphene.NonNull(graphene.String))
    email = graphene.Field(graphene.NonNull(graphene.String))
    first_name = graphene.Field(graphene.NonNull(graphene.String))
    last_name = graphene.Field(graphene.NonNull(graphene.String))
    last_login = graphene.Field(graphene.String)
    token = graphene.Field(graphene.NonNull(graphene.String))


class UserAvailable(graphene.ObjectType):
    """
    Result of an availavility user check. Used by mutation CheckAvailableUser.
    
    username: there is no user with the specified username
    email: there is no user with the specified email

    """
    username = graphene.Field(graphene.Boolean)
    email = graphene.Field(graphene.Boolean)


class AuthenticationQueries(graphene.AbstractType):
    "Abstract class of GraphQL queries for authentication"
    user_info = graphene.Field(User, token=graphene.String())
    logged_user = graphene.Field(User)

    def resolve_user_info(self, args, request, info):
        "Returns information from the logged user"
        token = args.get('token')
        if not token:
            return None
        payload = jwt.decode(token, settings.SECRET_KEY)
        User = get_user_model()
        try:
            user = User.objects.get(pk=payload['id'])
            return _copy_user(user)
        except User.DoesNotExist:
            return None
    
    def resolve_logged_user(self, args, request, info):
        "Returns information of the logged user"
        user = _get_user(request)
        if not user:
            return None
        return _copy_user(user)


class CheckAvailableUser(graphene.Mutation):
    "Checks if username and/or email are available"
    class Input:
        username = graphene.String()
        email = graphene.String()

    available = graphene.Field(UserAvailable)

    def mutate(self, args, request, info):
        "Returns if there is not user with the specified username or email"
        User = get_user_model()
        username = args.get('username')
        email = args.get('email')
        if not username and not email:
            raise ValueError("You have to specify username or email.")
        result = UserAvailable()
        if username:
            result.username = bool(User.objects.filter(username=username).count())
        else:
            result.username = None
        if email:
            result.email = bool(User.objects.filter(email=email).count())
        else:
            result.email = None
        return CheckAvailableUser(available=result)


class CheckAvailableUsername(graphene.Mutation):
    "Checks if the username is available"
    class Input:
        username = graphene.NonNull(graphene.String)

    is_available = graphene.Field(graphene.Boolean)

    def mutate(self, args, request, info):
        "Returns if there is not user with the specified username"
        User = get_user_model()
        is_available = not bool(User.objects.filter(username=args['username']).count())
        return CheckAvailableUsername(is_available=is_available)


class CheckAvailableEmail(graphene.Mutation):
    "Checks if the email is available"
    class Input:
        email = graphene.NonNull(graphene.String)

    is_available = graphene.Field(graphene.Boolean)

    def mutate(self, args, request, info):
        "Returns if there is not user with the specified email"
        User = get_user_model()
        is_available = not bool(User.objects.filter(email=args['email']).count())
        return CheckAvailableEmail(is_available=is_available)


class Login(graphene.Mutation):
    class Input:
        username = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    user = graphene.Field(User)

    def mutate(self, args, request, info):
        user = authenticate(username=args['username'], password=args['password'])
        if not user:
            return Login(user=None)
        result = _copy_user(user)
        payload = dict(id=user.id, username=user.username, uuid=str(uuid.uuid4()))
        result.token = jwt.encode(payload, settings.SECRET_KEY)
        return Login(user=result)


class RegisterUser(graphene.Mutation):
    class Input:
        username = graphene.NonNull(graphene.String)
        email = graphene.NonNull(graphene.String)
        first_name = graphene.NonNull(graphene.String)
        last_name = graphene.NonNull(graphene.String)
        password = graphene.NonNull(graphene.String)

    user = graphene.Field(User)

    def mutate(self, args, request, info):
        User = get_user_model()
        user = User()
        user.username = args['username']
        user.email = args['email']
        user.first_name = args['first_name']
        user.last_name = args['last_name']
        user.set_password(args['password'])
        user.save()
        result = _copy_user(user)
        payload = dict(id=user.id, username=user.username, uuid=str(uuid.uuid4()))
        result.token = jwt.encode(payload, settings.SECRET_KEY)
        return RegisterUser(user=result)
