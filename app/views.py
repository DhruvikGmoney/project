import csv
import os
from django.http import JsonResponse
from rest_framework.decorators import api_view
from pathlib import Path
from decimal import Decimal
cur_dir = Path.cwd()


@api_view(['POST'])
def filter_waist_measurements(request):
        if request.method == 'POST':
            try:
                height = request.data['height']
                print(height)
                weight = request.data['weight']
                print(weight)
                age = request.data['age']
                print(age)
                module_dir = os.path.dirname(__file__)
                print("module_dir >>",module_dir)

                file_path = os.path.join(module_dir, 'measurements.csv')
                print("file_path >>",file_path)

                with open(file_path, 'rb') as file:
                    reader = csv.DictReader(file)
                    data = list(reader)
                    filtered_data = [d for d in data if d.get('Height(cm)') == height and d.get('Weight(kgs)') == weight and d.get('Age') == age]
                    print("A"*10,filtered_data,"A"*10)
    
                    waist_measurements = sorted(list(set([d['Waist(cm)'] for d in filtered_data])))
                    waist_measurements.append("other")
       
                    return JsonResponse({'data': waist_measurements})
                
            except Exception as e:
                return JsonResponse({'error': 'Missing Some Parameters: {}'.format(e)})
        else:
            return JsonResponse({'error': 'POST request required'})


    

@api_view(['POST'])
def add_waist_measurements(request):
    if request.method == 'POST':
        try:
            height = request.data['height']
            weight = request.data['weight']
            age = request.data['age']
            waist = request.data['waist']
            print(height,weight,age,waist)
            
            with open(str(cur_dir)+'\measurements.csv', 'r') as file:
                reader = csv.DictReader(file)
                data = list(reader)
        
                filtered_data = [d for d in data if Decimal(d.get('Height(cm)')) == Decimal(height) and Decimal(d.get('Weight(kgs)')) == Decimal(weight) and Decimal(d.get('Age')) == Decimal(age) and Decimal(d.get('Waist(cm)')).quantize(Decimal('0.01')) == Decimal(waist).quantize(Decimal('0.01'))]

                if filtered_data:
                    waist_measurements = sorted(list(set([d['Waist(cm)'] for d in filtered_data])))
                    waist_measurements.append("other")
                    return JsonResponse({"msg":"Data Already Exists", 'waist_measurements': waist_measurements})
                else:
                    with open('measurements.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([height, weight, age, waist])
                        return JsonResponse({"msg":'Measurement added'}, safe=False)
        except Exception as e:
                return JsonResponse({'error': 'Missing Some Parameters: {}'.format(e)})
    else:
        return JsonResponse({'error': 'POST request required'})




















# import csv
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from pathlib import Path
# from decimal import Decimal
# cur_dir = Path.cwd()


# @api_view(['POST'])
# def filter_waist_measurements(request):
#     if request.method == 'POST':
#             height = request.data['height']
#             weight = request.data['weight']
#             age = request.data['age']
#             # Load the CSV data into memory as a list of dictionaries
#             with open(str(cur_dir)+'\measurements.csv', 'r') as file:
#                 reader = csv.DictReader(file)
#                 data = list(reader)
#                 filtered_data = [d for d in data if d.get(' Age') == age and d.get('Height (cm)') == height and d.get(' Weight (kgs)') == weight]
#                 # Get a list of unique waist measurements in the filtered data
#                 waist_measurements = sorted(list(set([d[' Waist (cm)'] for d in filtered_data])))
#                 waist_measurements.append("other")
#                 # Return the waist measurements as a JSON response
#                 return JsonResponse({'waist_measurements': waist_measurements})
#     else:
#         return JsonResponse({'error': 'POST request required'})
    

# @api_view(['POST'])
# def add_waist_measurements(request):
#     if request.method == 'POST':
#         height = request.data['height']
#         weight = request.data['weight']
#         age = request.data['age']
#         waist = request.data['waist']
#         print(height,weight,age,waist)
        
#         with open(str(cur_dir)+'\measurements.csv', 'r') as file:
#             reader = csv.DictReader(file)
#             data = list(reader)
    
#             filtered_data = [d for d in data if Decimal(d.get('Height (cm)')) == Decimal(height) and Decimal(d.get(' Weight (kgs)')) == Decimal(weight) and Decimal(d.get(' Age')) == Decimal(age) and Decimal(d.get(' Waist (cm)')).quantize(Decimal('0.01')) == Decimal(waist).quantize(Decimal('0.01'))]

#             if filtered_data:
#                 waist_measurements = sorted(list(set([d[' Waist (cm)'] for d in filtered_data])))
#                 waist_measurements.append("other")
#                 return JsonResponse({"msg":"Data Already Exists", 'waist_measurements': waist_measurements})
#             else:
#                 with open('measurements.csv', 'a', newline='') as csvfile:
#                     writer = csv.writer(csvfile)
#                     writer.writerow([height, weight, age, waist])
#                     return JsonResponse('Measurement added', safe=False)
#     else:
#         return JsonResponse({'error': 'POST request required'})

