from django.shortcuts import render, redirect
from django.http import HttpResponse,FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InputFileForm
from .models import InputFile
import pandas as pd
import os
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        form = InputFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_file1 = InputFile(file=request.FILES['file1'])
            input_file1.save()
            input_file2 = InputFile(file=request.FILES['file2'])
            input_file2.save()
            return redirect('transform_file')
    else:
        form = InputFileForm()
    return render(request, 'excelapp/upload.html', {'form': form})


def transform_file(request):
    
    input_file1 = InputFile.objects.order_by('-uploaded_at')[0]
    input_file2 = InputFile.objects.order_by('-uploaded_at')[1]
    input_file_path1 = input_file1.file.path
    input_file_path2 = input_file2.file.path
    master_file_path = os.path.join(settings.BASE_DIR, 'exel_project/data/master.xlsx')  

 
    input_df1 = pd.read_excel(input_file_path1, header=None)
    input_df2 = pd.read_excel(input_file_path2, header=None)
    master_df = pd.read_excel(master_file_path)

    
    master_df.columns = ['insurer', 'name', 'clubbed_name']

   
    combined_df = pd.concat([input_df1, input_df2], axis=0, ignore_index=True)

   
    print("Input DF1 Columns:", input_df1.columns.tolist())
    print("Input DF2 Columns:", input_df2.columns.tolist())
    print("Master DF Columns:", master_df.columns.tolist())
    print("Combined DF Head:\n", combined_df.head())

    combined_df.columns = ['insurer', 'Health-Retail', 'Health-Group', 'Health-Government schemes', 'Overseas Medical', 'Grand Total', 'Growth %', 'Market %', 'Accretion']

    
    combined_df['clubbed_name'] = combined_df['insurer'].map(dict(zip(master_df['name'], master_df['clubbed_name']))).fillna(combined_df['insurer'])

    
    combined_df['Year'] = combined_df['insurer'].apply(lambda x: '2022' if 'Previous Year' in str(x) else '2023')

    
    input_df1_length = len(input_df1)
    combined_df['Month'] = ['Jan'] * input_df1_length + ['Dec'] * (len(combined_df) - input_df1_length)

   
    relevant_columns = ['Health-Retail', 'Health-Group', 'Health-Government schemes', 'Overseas Medical'] 
     
    combined_df = combined_df.melt(id_vars=['Year', 'Month', 'clubbed_name'], value_vars=relevant_columns,
                                   var_name='Product', value_name='Value')

  
    combined_df.dropna(inplace=True)

   
    combined_df['category'] = combined_df['Product'].apply(lambda x: 'PVT' if 'Retail' in x else ('SAHI' if 'Group' in x else 'SP'))

    
    combined_df = combined_df[['Year', 'Month', 'category', 'clubbed_name', 'Product', 'Value']]


 
    combined_df.sort_values(by=['Year', 'Month', 'category', 'clubbed_name', 'Product'], inplace=True)


    
    output_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/output.xlsx')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    combined_df.to_excel(output_file_path, index=False)

    return render(request, 'excelapp/transform.html', {
        'output_file_url': output_file_path
    })


# download file logic 
def download_file(request):
    output_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/output.xlsx')
    with open(output_file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=output.xlsx'
        return response


# image plot logic 
def plot_image(request):
    plot_image_path = os.path.join(settings.MEDIA_ROOT, 'uploads/plot.png')
    return FileResponse(open(plot_image_path, 'rb'), content_type='image/png')
