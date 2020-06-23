from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults


def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Patient_Blood_Pressure = int(request.POST.get('Patient_Blood_Pressure'))
        Patient_Heartrate = int(request.POST.get('Patient_Heartrate'))

        # Unpickle model
        model = pd.read_pickle(r"new_model.pickle")
        # Make prediction
        result = model.predict([[Patient_ID, Patient_Age, Patient_Gender, Patient_Blood_Pressure, Patient_Heartrate]])

        Heart_Disease = result[0]

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Patient_Blood_Pressure=Patient_Blood_Pressure, Patient_Heartrate=Patient_Heartrate, Heart_Disease=Heart_Disease)

        return JsonResponse({'result': Heart_Disease, 'Patient_ID': Patient_ID,
                             'Patient_Age': Patient_Age, 'Patient_Gender': Patient_Gender, 'Patient_Blood_Pressure': Patient_Blood_Pressure, 'Patient_Heartrate': Patient_Heartrate},
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)
