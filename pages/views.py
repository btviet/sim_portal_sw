from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse, HttpResponse
import json
import requests
import get_hapi_session_cookies as hapi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import datetime
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from .models import CME, Flare, Magnetogram, Spectrogram
from simulation_functions import return_simulation_time, return_event_start_time

def homepage_view(request, *args, **kwargs):
    context = {}
    current_simulation_time = return_simulation_time()
    context = {"time":current_simulation_time}
    return render(request, 'home.html', context)

class HomePageView(TemplateView):
    template_name = 'home.html'

class TestPageView(TemplateView):
    template_name = 'test.html'

class SESCPageView(TemplateView):
    template_name = 's_esc.html'

class HESCPageView(TemplateView):
    template_name = 'h_esc.html'

class RESCPageView(TemplateView):
    template_name = 'r_esc.html'

class IESCPageView(TemplateView):
    template_name = 'i_esc.html'

class GESCPageView(TemplateView):
    template_name = 'g_esc.html'

class FlarealertPageView(ListView):
    model = Flare
    template_name = 'sesc/sidc_flarealert.html'
    def get_queryset(self):
        # Get the current time
        current_time =  return_simulation_time()
        # Filter Flare instances where issue_time is in the past
        queryset = Flare.objects.filter(issue_time__lte=current_time)
        queryset = queryset.order_by('-issue_time')
        return queryset

class CactusPageView(ListView):
    model = CME
    template_name = 'sesc/cactus.html'
    def get_queryset(self):
        # Get the current time
        current_time =  return_simulation_time()
        # Filter Flare instances where issue_time is in the past
        queryset = CME.objects.filter(issue_time__lte=current_time)
        queryset = queryset.order_by('-issue_time')
        return queryset

class eCallistoPageView(ListView):
    model=Spectrogram
    template_name = 'sesc/ecallisto.html'
    def get_queryset(self):
        current_time = return_simulation_time()
        print("current time: ", current_time)
        queryset = Spectrogram.objects.filter(issue_time__lte=current_time)
        queryset = queryset.order_by('-issue_time')
        return queryset

def solarmap(request):
    username = 'yourusername'
    password = 'yourpassword'
    SSO_COOKIENAME="iPlanetDirectoryPro" 
    PORTAL_URL="https://swe.ssa.esa.int/"
    AUTHENTICATE_URL="https://sso.ssa.esa.int/am/json/authenticate"
    authenticated, auth_cookie = hapi.get_auth_cookie(username, password)

    current_simulation_time = return_simulation_time().strftime("%Y-%m-%dT%H:%M:%SZ")

    response = requests.get(
    "https://ssa.sidc.be/prod/API/index.php?component=archive&pc=S101&psc=c&timenavbar.date="+current_simulation_time,
    cookies = {

    SSO_COOKIENAME : auth_cookie, 
    })

    content = response.content
    data = {'content':  mark_safe(content), 
    'image_date':current_simulation_time}
    return render(request, 'sesc/sidc_solarmap.html', data)

def synoptic_view(request):

    current_time = return_simulation_time()
    try:
        instance = Magnetogram.objects.filter(issue_time__lt=current_time).latest('issue_time')
    except Magnetogram.DoesNotExist:
        # Handle the case where no instance with the current time is found
        instance = None
    return render(request, 'sesc/synoptic.html', {'instance': instance})

def dbem(request, *args, **kwargs):
    current_simulation_time = return_simulation_time()
    event_start = return_event_start_time()
    #current_simulation_time= timezone.make_aware(current_simulation_time, timezone.utc)
    #event_start = timezone.make_aware(event_start, timezone.utc)
    context = {"time":current_simulation_time, "eventstart": event_start}
    return render(request, 'hesc/dbem.html', context)

def solarwind(request):
    speed_df = pd.read_csv('dataframes/simulated_solarwind_speed.csv', parse_dates=['new_time'])
    density_df = pd.read_csv('dataframes/simulated_solarwind_density.csv', parse_dates=['new_time'])
    speed_df['new_time'] = speed_df['new_time'].dt.tz_localize('UTC') # make a timezone-aware column
    density_df['new_time'] = density_df['new_time'].dt.tz_localize('UTC') # make a timezone-aware column
    current_time = return_simulation_time()
    start_time = current_time - datetime.timedelta(hours=24)
    end_time = current_time
    speed_df = speed_df[(speed_df['new_time'] >= start_time) & (speed_df['new_time'] <= end_time)]
    density_df = density_df[(density_df['new_time'] >= start_time) & (density_df['new_time'] <= end_time)]
    fig, ax = plt.subplots(2,sharex=True)
    fig.subplots_adjust(hspace=1) 
    fig.subplots_adjust(bottom=0.2)  
    ax[0].plot(speed_df['new_time'], speed_df['speed'])
    ax[1].plot(density_df['new_time'], density_df['density'])
    ax[0].set_ylabel('Solar wind speed (km/s)')
    ax[1].set_ylabel('Solar wind density (1/cm^3)')
    ax[0].grid()
    ax[1].grid()
    num_ticks = 5  # number of ticks on the y-axis
    for axis in ax:
        axis.yaxis.set_major_locator(plt.MaxNLocator(num_ticks))
    labels = ax[1].get_xticklabels()
    ticks = ax[1].get_xticks()
    ax[1].set_xticks(ticks)
    ax[1].set_xticklabels(labels, rotation=15)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    current_time_string = current_time.strftime('%Y%m%d-%H%M%S')
    fig.savefig('media/solarwind/sw_'+current_time_string+'.png')
    image_url = '/media/solarwind/sw_'+current_time_string+'.png'
    latest_sw_speed = round(speed_df['speed'].iloc[-1],0)
    latest_sw_density = density_df['density'].iloc[-1]
    return render(request, 'hesc/solarwind.html', {'image_url': image_url, 'sw_speed': latest_sw_speed, 'sw_density': latest_sw_density} )

def protonflux(request):
    columnmap_het = {'h1':'13.6 - 15.1 MeV',
        'h2':'14.9 - 17.1 MeV',
        'h3':'17.0 - 19.3 MeV',
        'h4':'20.9 - 23.8 MeV',
        'h5':'23.9 - 26.4 MeV',
        'h6':'26.3 - 29.7 MeV',
        'h7':'29.5 - 33.4 MeV',
        'h8':'33.4 - 35.8 MeV',
        'h9':'35.5 - 40.5 MeV',
        'h10':'40.0 - 60.0 MeV',
        'h11':'60.0 - 100 MeV'} 
    flux_df = pd.read_csv('dataframes/simulated_proton_fluxes.csv', parse_dates=['new_time'])
    
    flux_df['new_time'] = flux_df['new_time'].dt.tz_localize('UTC') # make a timezone-aware column
    current_time =  return_simulation_time()
    ## define plotting window
    start_time = current_time - datetime.timedelta(hours=24)
    
    end_time = current_time
    flux_df = flux_df[(flux_df['new_time'] >= start_time) & (flux_df['new_time'] <= end_time)]
    fig, ax = plt.subplots(figsize=(10,5))
    plt.subplots_adjust(bottom=0.2)
    plt.subplots_adjust(right=0.7)  # Increase the space on the right side for the legend
    for i in range(1,12):
        column_name = 'h'+str(i)
        ax.plot(flux_df['new_time'], flux_df[column_name], label=columnmap_het[column_name])
    ax.set_ylabel('Proton flux (pfu)') 
    ax.grid()
    labels = ax.get_xticklabels()
    ticks = ax.get_xticks()
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation=15)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_yscale('log')
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    current_time_string = current_time.strftime('%Y%m%d-%H%M%S')
    fig.savefig('media/protonflux/protonflux_'+current_time_string+'.png')
    image_url = '/media/protonflux/protonflux_'+current_time_string+'.png'
    return render(request, 'hesc/protonflux.html', {'image_url': image_url} )

class ComeSEPPageView(TemplateView):
    template_name = 'resc/comesep.html'

class SYMHPageView(TemplateView):
    template_name = 'gesc/sym_h.html'

def kp(request):
    kp_df = pd.read_csv('dataframes/simulated_kp.csv', parse_dates=['datetime'])
    kp_df['datetime'] = kp_df['datetime'].dt.tz_localize('UTC') # make a timezone-aware column
    current_time = return_simulation_time()
    start_time = current_time - datetime.timedelta(hours=24)
    end_time = current_time
    kp_df = kp_df[(kp_df['datetime'] >= start_time) & (kp_df['datetime'] <= end_time)]

    fig, ax = plt.subplots(figsize=(10,6))
    fig.subplots_adjust(hspace=1) 
    fig.subplots_adjust(bottom=0.2)  
    ax.plot(kp_df['datetime'], kp_df['kp'])
    ax.set_ylabel('Kp')
    ax.grid()
    labels = ax.get_xticklabels()
    ticks = ax.get_xticks()
    ax.set_xticks(ticks)
    ax.set_ylim(0, 10)
    ax.set_xticklabels(labels, rotation=15)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    current_time_string = current_time.strftime('%Y%m%d-%H%M%S')
    fig.savefig('media/kp/kp_'+current_time_string+'.png')
    image_url = '/media/kp/kp_'+current_time_string+'.png'
    return render(request, 'gesc/kp.html', {'image_url': image_url} )

def anemos(request):
    gle_df =  pd.read_csv('dataframes/simulated_gle.csv', parse_dates=['datetime'])
    gle_df['datetime'] = gle_df['datetime'].dt.tz_localize('UTC') # make a timezone-aware column
    current_time = return_simulation_time()
    current_index = (gle_df['datetime'] <= current_time)[::-1].idxmax()
    current_row = gle_df.iloc[current_index]
    gle_text = current_row['gle_status']
    gle_time = current_row['datetime'] 

    return render(request, 'resc/anemos.html', {'gle_text': gle_text, 'gle_time': gle_time} )

def pcn(request):
    pcn_df = pd.read_csv('dataframes/simulated_pcn.csv', parse_dates=['datetime'])
    pcn_df['datetime'] = pcn_df['datetime'].dt.tz_localize('UTC') # make a timezone-aware column
    current_time = return_simulation_time()
    start_time = current_time - datetime.timedelta(hours=24)
    end_time = current_time
    pcn_df = pcn_df[(pcn_df['datetime'] >= start_time) & (pcn_df['datetime'] <= end_time)]
    fig, ax = plt.subplots()
    fig.subplots_adjust(hspace=1) 
    fig.subplots_adjust(bottom=0.2)  
    ax.plot(pcn_df['datetime'], pcn_df['value'])
    ax.set_ylabel('PCN (mV/m)')

    ax.grid()
    labels = ax.get_xticklabels()
    ticks = ax.get_xticks()
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation=15)
    num_ticks = 10  # number of ticks on the y-axis

    ax.yaxis.set_major_locator(plt.MaxNLocator(num_ticks))
    #ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45, ha='right') 
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    current_time_string = current_time.strftime('%Y%m%d-%H%M%S')
    fig.savefig('media/pcn/pcn_'+current_time_string+'.png')
    image_url = '/media/pcn/pcn_'+current_time_string+'.png'
    latest_pcn = pcn_df['value'].iloc[-1]
    return render(request, 'gesc/pcn.html', {'image_url': image_url, 'pcn': latest_pcn} )

class TECPageView(TemplateView):
    template_name = 'iesc/tec.html'

class AEPageView(TemplateView):
    template_name = 'gesc/AE.html'


