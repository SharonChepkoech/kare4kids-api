from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from .models import Sitter, Parent, Job
from .forms import UserRegistrationForm, LoginForm, SitterForm, ParentForm
from .serializers import SitterSerializer, UserSerializer, JobSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic.edit import CreateView, UpdateView
from rest_framework.generics import ListAPIView
from django.urls import reverse_lazy
from .models import Parent
from .forms import ParentForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Job
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserProfileSerializer, SitterProfileSerializer,ParentProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from babysitter_app.models import Sitter, Parent
from babysitter_app.serializers import UserProfileSerializer
import logging

logger = logging.getLogger(__name__)
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if hasattr(user, "sitter"):
        sitter = user.sitter

    if request.method == "PATCH":
        print(f"🔥 Received Data: {request.data}")  # Log incoming data

        serializer = SitterProfileSerializer(sitter, data=request.data.get("sitter", {}), partial=True)
        if serializer.is_valid():
            print(f"✅ Valid Data: {serializer.validated_data}")  # Log valid data
            serializer.save()
            sitter.refresh_from_db()  # 🔥 Ensure fresh data is fetched
            return Response(serializer.data, status=200)

        print(f"❌ Serializer Errors: {serializer.errors}")  # Log errors
        return Response(serializer.errors, status=400)  # Return errors if invalid

def update_profile(request):
    user = request.user

    print(f"🔹 User: {user.username}, Type: {user.user_type}")

    # Check if user has a sitter or parent profile
    if hasattr(user, "sitter"):
        profile = user.sitter
        print("✅ Found Sitter Profile")
    elif hasattr(user, "parent"):
        profile = user.parent
        print("✅ Found Parent Profile")
    else:
        print("❌ Profile not found")
        return Response({"error": "Profile not found"}, status=400)

    print(f"🔥 Incoming Request Data: {request.data}")

    # Extract sitter data
    sitter_data = request.data.get("sitter", None)

    if not sitter_data:
        print("❌ No sitter data provided")
        return Response({"error": "No sitter data provided"}, status=400)

    print(f"✅ Extracted Sitter Data: {sitter_data}")

    # Update fields
    updated_fields = []
    for key, value in sitter_data.items():
        if hasattr(profile, key):
            print(f"🔄 Updating {key} -> {value}")
            setattr(profile, key, value)
            updated_fields.append(key)
        else:
            print(f"⚠️ Ignoring unknown field: {key}")

    # Save if any fields were updated
    if updated_fields:
        profile.save()  # Force saving
        profile.refresh_from_db()
        print(f"✅ Updated Profile: {vars(profile)}")
        return Response({"message": "Profile updated successfully", "updated_fields": updated_fields})
    else:
        print("⚠️ No fields updated")
        return Response({"message": "No changes made"}, status=200)

class UpdateSitterProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows a logged-in sitter to update their profile details.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SitterProfileSerializer

    def get_object(self):
        user = self.request.user
        if hasattr(user, "sitter"):
            user.sitter.refresh_from_db()  # 🔥 Ensures fresh data
            return user.sitter
        return Response({"error": "User is not a sitter"}, status=400)



class UpdateParentProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows a logged-in parent to update their profile details.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ParentProfileSerializer

    def get_object(self):
        user = self.request.user
        if hasattr(user, "parent"):
            return user.parent
        return Response({"error": "User is not a parent"}, status=400)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user  # Returns the logged-in user

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])

def user_profile(request):
    user = request.user

    if hasattr(user, "sitter"):
        sitter = user.sitter

    if request.method == "PATCH":
        print(f"🔥 Received Data: {request.data}")  # Log incoming data
    serializer = SitterProfileSerializer(sitter, data=request.data, partial=True)
    if serializer.is_valid():
        print(f"✅ Valid Data: {serializer.validated_data}")  # Log valid data
        serializer.save()
        sitter.refresh_from_db()  # 🔥 Ensure fresh data is fetched
        return Response(serializer.data, status=200)
    print(f"❌ Serializer Errors: {serializer.errors}")  # Log errors
    return Response(serializer.errors, status=400)
   
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Make login public

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,                            
                "user_type": user.user_type,  # ✅ Send user_type to frontend
                "role": user.user_type if hasattr(user, 'user_type') else "user"
            })
        else:
            return Response({"error": "Invalid credentials"}, status=401)

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for API

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        form = UserRegistrationForm(data=request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = request.data.get('user_type', 'parent')
            user.save()

            if user.user_type == 'parent':
                Parent.objects.create(user=user, name=user.username)
            elif user.user_type == 'sitter':
                Sitter.objects.create(
                user=user,
                name=user.username,  # Assign a default name (or ask for it in the form)
                experience=request.data.get('experience', 0),  # Ensure experience is set
                location=request.data.get('location', 'Unknown'),  # Set a default location
                bio=request.data.get('bio', ''),  # Ensure bio is set
            )


            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Registration successful!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "role": user.user_type
            }, status=status.HTTP_201_CREATED)

        # 🚨 Debugging: Log form errors
        return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired redirect URL name
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

User = get_user_model()

class UserListView(ListAPIView):
    queryset = User.objects.all().only("id", "username", "email")  # Optimize fields
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

def home(request):
    sitters = Sitter.objects.all()
    return render (request, 'babysitter_app/home.html', {'sitters': sitters})
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Sitter, Job
from .serializers import JobSerializer

class RequestSitterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, sitter_id):
        try:
            user = request.user

            # Ensure the requesting user is a parent
            if not hasattr(user, "parent"):
                return Response({"error": "Only parents can request a sitter"}, status=403)

            sitter = Sitter.objects.get(id=sitter_id)

            job_data = request.data.copy()
            job_data["parent"] = user.parent.id if hasattr(user, "parent") else None
            job_data["sitter"] = sitter.id

            serializer = JobSerializer(data=job_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        except Sitter.DoesNotExist:
            return Response({"error": "Sitter not found"}, status=404)
        except Exception as e:
            return Response({"error": "Something went wrong"}, status=500)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "is_parent": hasattr(user, "parent"),
            "is_sitter": hasattr(user, "sitter"),
            "parent": {"id": user.parent.id} if hasattr(user, "parent") else None,  # 🔥 Ensure this is included
            "sitter": {"id": user.sitter.id} if hasattr(user, "sitter") else None,
        }
        return Response(data)


class JobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if hasattr(request.user, "parent"):
                jobs = Job.objects.select_related("sitter", "parent").filter(parent=request.user.parent)  # Parent's requests
            elif hasattr(request.user, "sitter"):
                jobs = Job.objects.select_related("parent", "sitter").filter(sitter=request.user.sitter) 
            else:
                return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SitterBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'sitter'):
            return Response({"error": "Unauthorized – Only sitters can access this."}, status=status.HTTP_403_FORBIDDEN)

        # Get pending and accepted jobs for the logged-in sitter
        jobs = Job.objects.filter(sitter=request.user.sitter)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateSitterView(FormView):
    template_name = 'babysitter_app/create_update_sitter.html'
    form_class = SitterForm

    def form_valid(self, form):
        form.save()  # Save the new sitter
        return redirect('sitter_list')  # Redirect to the sitter list view

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UpdateSitterView(FormView):
    template_name = 'babysitter_app/create_update_sitter.html'
    form_class = SitterForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Sitter, pk=pk)

    def get_initial(self):
        initial = super().get_initial()
        sitter = self.get_object()
        initial.update({
            'name': sitter.name,
            'bio': sitter.bio,
            'hourly_rate': sitter.hourly_rate,
            'location': sitter.location
        })
        return initial

    def form_valid(self, form):
        form.save()  # Save the updated sitter
        return redirect('sitter_list')  # Redirect to the sitter list view

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

def sitter_list(request):
    sitters = Sitter.objects.all().order_by('name')  
    paginator = Paginator(sitters, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'babysitter_app/sitter_list.html', {'page_obj': page_obj})

def delete_sitter(request, pk):  
    sitter = get_object_or_404(Sitter, pk=pk)

    if request.method == 'POST':
        sitter.delete()
        return redirect('sitter_list')

    return render(request, 'babysitter_app/delete_sitter.html', {'sitter': sitter})

def search_sitters(request):
    query = request.GET.get('query', '')  
    sitters = Sitter.objects.filter(location__icontains=query)  
    return render(request, 'babysitter_app/search_results.html', {'sitters': sitters, 'query': query})

class ParentCreateView(CreateView):
    model = Parent
    form_class = ParentForm
    template_name = 'babysitter_app/create_parent.html'
    success_url = reverse_lazy('parent_list')

class ParentUpdateView(UpdateView):
    model = Parent
    form_class = ParentForm
    template_name = 'babysitter_app/create_parent.html'
    success_url = reverse_lazy('parent_list')

def parent_list(request):
    parents = Parent.objects.all().order_by('id')  
    paginator = Paginator(parents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'babysitter_app/parent_list.html', {'page_obj': page_obj})  

class ParentDeleteView(DeleteView):
    model = Parent
    template_name = 'babysitter_app/delete_parent.html'
    success_url = reverse_lazy('parent_list')

class SitterList(APIView):
    def get(self, request):
        sitters = Sitter.objects.all()
        serializer = SitterSerializer(sitters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SitterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SitterDetail(APIView):
    def get(self, request, pk):
        sitter = get_object_or_404(Sitter, pk=pk)
        return Response(SitterSerializer(sitter).data, status=status.HTTP_200_OK)

class UpdateBookingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        user = request.user  # Logged-in user
        job = get_object_or_404(Job, id=id)  # Fetch the booking

        # ✅ Ensure the user is a sitter & owns the booking
        if not hasattr(user, 'sitter') or job.sitter.user != user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Ensure the booking is still pending
        if job.status != 'pending':
            return Response({"error": "Booking cannot be modified"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Get the new status from the request
        new_status = request.data.get('status')
        if new_status not in ["accepted", "declined"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Update the booking status
        job.status = new_status
        job.save()

        return Response({"message": f"Booking {id} marked as {new_status}"}, status=status.HTTP_200_OK)


class ParentBookingsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get_queryset(self):
        """Return bookings belonging to the logged-in parent."""
        user = self.request.user

        if not hasattr(user, "parent"):  # Ensure user is a parent
            return Job.objects.none()  # Return empty queryset if not a parent

        return Job.objects.filter(parent=user.parent).order_by("-job_date")
    
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user = request.user
        job = get_object_or_404(Job, id=id)

        # ✅ Ensure only the parent who created the booking can cancel
        if not hasattr(user, "parent") or job.parent.user != user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Only allow canceling if it's pending or accepted
        if job.status not in ["pending", "accepted"]:
            return Response({"error": "Cannot cancel this booking"}, status=status.HTTP_400_BAD_REQUEST)

        job.delete()
        return Response({"message": "Booking canceled successfully"}, status=status.HTTP_200_OK)

class ProfilePictureUploadView(APIView):
    def patch(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        
        # Check if file exists in request
        if "profile_picture" not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the uploaded file
        uploaded_file = request.FILES["profile_picture"]

        # ✅ Save the file
        user.profile_picture.save(uploaded_file.name, uploaded_file, save=True)

        # ✅ Now, return the full URL
        if user.profile_picture:
            profile_picture_url = request.build_absolute_uri(user.profile_picture.url)
        else:
            profile_picture_url = None

        return Response({"profile_picture": profile_picture_url}, status=status.HTTP_200_OK)
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer  # Make sure this is handling updates

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        print(f"🔥 Received Data in ProfileView: {request.data}")  # Debugging
        response = super().update(request, *args, **kwargs)
        print(f"✅ Updated Profile Data: {response.data}")  # Confirm updates
        return response