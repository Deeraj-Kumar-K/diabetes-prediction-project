import pickle
import numpy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

    
class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("welcome"))
        return super().get(request, *args, **kwargs)

class WelcomePage(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'

class HeartPredictionPage(LoginRequiredMixin, TemplateView):
    template_name = 'heart.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'


@csrf_exempt
def diabetes_prediction(request):
    pregnancies = request.POST.get("Pregnancies")
    glucose = request.POST.get("Glucose")
    bloodpressure = request.POST.get("BloodPressure")
    skinthickness = request.POST.get("SkinThickness")
    insulin = request.POST.get("Insulin")
    BMI = request.POST.get("BMI")
    DiabetesPedigreeFunction = request.POST.get("DiabetesPedigreeFunction")
    age = request.POST.get("Age")

    diabetes_data = [
        [pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]
        ]
    diabetes_model = pickle.load(open('diabetes_model.pickle', 'rb'))

    prediction = diabetes_model.predict(diabetes_data)

    outcome = prediction


    if outcome == 1:
        result = "Person is Diabetic"
        colors = "red"
    elif outcome == 0:
        result = "Person is not Diabetic"
        colors = "green"

    return render(request, 'welcome.html', {'result':result, 'res_color':colors})


@csrf_exempt
def heart_prediction(request):
    age = request.POST.get("age")
    gender = request.POST.get("gender")
    cp = request.POST.get("cp")
    trestbps = request.POST.get("trestbps")
    chol = request.POST.get("chol")
    fbs = request.POST.get("fbs")
    restecg = request.POST.get("restecg")
    thalach = request.POST.get("thalach")
    exang = request.POST.get("exang")
    oldpeak = request.POST.get("oldpeak")
    slope = request.POST.get("slope")
    ca = request.POST.get("ca")
    thal = request.POST.get("thal")

    heart_data = [
        age, gender, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        ]

    input_data_as_numpy_array=numpy.array(heart_data, dtype=numpy.float32)

    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    heart_model = pickle.load(open('heart_model.pickle', 'rb'))

    prediction = heart_model.predict(input_data_reshaped)

    outcome = prediction

    if outcome == 0:
        result = "Person's Heart is Healthy"
        colour = "green"
    else:
        result = "Person's Heart is not Healthy"
        colour = "red"

    return render(request, 'heart.html', {'result':result, 'colour':colour})
