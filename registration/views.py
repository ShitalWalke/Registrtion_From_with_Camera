import base64
from PIL import Image
from io import BytesIO
import os
from django.http import HttpResponse
from .models import Registration
import cv2
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import RegistrationForm


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('camera')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration_form.html', {'form': form})


def camera_view(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        uploaded_image_path = 'media/' + str(uploaded_image)

        # Load the uploaded image
        uploaded_img = cv2.imread(uploaded_image_path)
        gray_uploaded = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_uploaded, 1.1, 4)

        if len(faces) > 0:
            # Perform face matching logic
            # If match is successful, record the time and date
            registration = Registration.objects.last()  # Get the last registered user
            registration.registration_date = datetime.now()
            registration.save()
            return redirect('success')

    return render(request, 'registration/camera.html')


# registration/views.py

def process_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        image_data = image_data.replace('data:image/png;base64,', '')
        image_data = base64.b64decode(image_data)

        # Define where to save the image
        directory = 'C:\\Users\\Shital\\PycharmProjects\\Swapra_Company\\registration_project\\media\\captured_images'

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Define the image file path
        image_path = os.path.join(directory, 'captured_image.png')

        # Save the captured image to a file
        image = Image.open(BytesIO(image_data))
        image.save(image_path)

        # Here, you should include the face matching logic and save the date and time to the database if matched

        # Assuming face matching is successful
        matched = True  # Placeholder for actual face matching result
        if matched:
            registration = Registration.objects.last()
            registration.timestamp = datetime.now()
            registration.save()
            return redirect('success')

        # If not matched, handle accordingly (e.g., return an error message)

    return HttpResponse('Error: Invalid request method.')


def success_view(request):
    return render(request, 'registration/success.html')
