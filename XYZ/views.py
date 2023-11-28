from django.shortcuts import render
from django.urls import reverse
from XYZ.models import BasicModel, InputModel, BasicForm, InputForm
from django.http import HttpResponseRedirect
import pandas as pd
import matplotlib.pyplot as plt

# Create your views here.

# initial form
def first_form(request):
    """ first view to show up , initial form """

    initial={
            'project_name': request.session.get('project_name', None),
            'project_description': request.session.get('project_description', None),
            'client': request.session.get('client', None),
            'contractor': request.session.get('contractor', None),
            }
    
    form = BasicForm(request.POST or None, initial=initial)

    if request.method == 'POST':
        if form.is_valid():
            request.session['project_name'] = form.cleaned_data['project_name']
            request.session['project_description'] = form.cleaned_data['project_description']
            request.session['client'] = form.cleaned_data['client']
            request.session['contractor'] = form.cleaned_data['contractor']

            return HttpResponseRedirect(reverse('XYZ:second_form'))
    return render(request, 'form1.html', {'form': form})


# second form
def second_form(request):
    """ this view will run if there is no csv file upload and sent all data to result page """

    form = InputForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            input_info = form.save(commit=False)
            basic_info = BasicModel.objects.create(
                project_name=request.session['project_name'],
                project_description=request.session['project_description'],
                client=request.session['client'],
                contractor=request.session['contractor'],
            )
        input_info.basic_model = basic_info
        input_info.save()

        return HttpResponseRedirect(reverse('XYZ:final_link'))
        
            
    context = {
            'form': form, 
        }
        
    return render(request, 'form2.html', context)

# save data in session
def csv_form(request):
    """ this view will run if there is a csv file upload, this view will store all the csv data into the session """

    initial={
        'maximum_x': request.session.get('maximum_x', None),
        'minimum_x': request.session.get('minimum_x', None),
        'maximum_y': request.session.get('maximum_y', None),
        'minimum_y': request.session.get('minimum_y', None),
        'maximum_z': request.session.get('maximum_z', None),
        'minimum_z': request.session.get('minimum_z', None),
    }

    form = InputForm(request.POST or None, initial=initial)

    if request.method == 'POST':

        file = request.FILES.get('myfile', None)

        if file:

            uploaded_csv = pd.read_csv(file)
            column_kp = uploaded_csv['KP'].values 
            column_x = uploaded_csv['X'].values 
            column_y = uploaded_csv['Y'].values 
            column_z = uploaded_csv['Z'].values 

            x_max = column_x.max()
            x_min = column_x.min()

            y_max = column_y.max()
            y_min = column_y.min()

            z_max = column_z.max()
            z_min = column_z.min()

            request.session['maximum_x'] = x_max
            request.session['minimum_x'] = x_min
            request.session['maximum_y'] = y_max
            request.session['minimum_y'] = y_min
            request.session['maximum_z'] = z_max
            request.session['minimum_z'] = z_min


            form = InputForm(initial={
                'maximum_x': request.session['maximum_x'],
                'minimum_x': request.session['minimum_x'],
                'maximum_y': request.session['maximum_y'],
                'minimum_y': request.session['minimum_y'],
                'maximum_z': request.session['maximum_z'],
                'minimum_z': request.session['minimum_z'],
            })

            # show chart before second form pre-populate

            plt.scatter(column_kp, column_x)
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title('Scatter Plot')
            plt.show()

    context = {
        'form' : form,
    }
    return render(request, 'form3.html', context)


# save data into the database
def csv_process(request):
    """ collect all the session data and actually save data into the database and return the result page """

    form = InputForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            input_info = form.save(commit=False)
            basic_info = BasicModel.objects.create(
                project_name=request.session['project_name'],
                project_description=request.session['project_description'],
                client=request.session['client'],
                contractor=request.session['contractor'],
            )
        input_info.basic_model = basic_info
        input_info.save()

        return HttpResponseRedirect(reverse('XYZ:final_link'))
    
    return render(request, 'result.html')

# render the final result page
def final_view(request):
    """ this will show the final result page """
    user_project = request.session['project_name']
    user_info = InputModel.objects.filter(basic_model__project_name=user_project)



    context = {
        'user' :  user_info,
    }

    return render(request, 'result.html', context)









