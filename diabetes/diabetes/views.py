import pickle

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
