
from django.shortcuts import render
import csv
import pandas as pd
from io import TextIOWrapper
from .forms import CSVUploadForm
from django.http import JsonResponse
import pandas as pd

def process_csv(file):
    csv_data = []
    df = pd.read_csv(TextIOWrapper(file, encoding='utf-8'))
    df = df.replace('', pd.NA)
    csv_data = df.values.tolist()
    return csv_data

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # print("files: ",request.FILES)
            csv_file = request.FILES['csv_file']
            csv_data = process_csv(csv_file)
            
            # return render(request, 'display.html', {'csv_data': csv_data, 'file': csv_file})
    else:
        form = CSVUploadForm()
        csv_data = ""

    return render(request, 'index.html', {'form': form, 'csv_data': csv_data})

def reverse_compliment(request):

    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            print("files", csv_file)
        except KeyError:
            return JsonResponse({'error': 'No file uploaded'})

        try:
            df = pd.read_csv(csv_file, skiprows=20)  # skiping the first 20 rows
        except pd.errors.EmptyDataError:
            return JsonResponse({'error': 'The uploaded CSV file is empty or invalid'})

        if 'index2' not in df.columns:
            return JsonResponse({'error': 'The "index2" column is not present in the CSV file'})

        fc = df["index2"]
        complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

        result_list = []  

        for data in range(8):
            sequence = fc[data]
            reversed_sequence = sequence[::-1]
            rc = "".join(complement[letter] for letter in reversed_sequence)
            result_list.append(rc)

        # returing the result as JSON
        return JsonResponse({'result': result_list})

    return JsonResponse({'error': 'Invalid request method'})
