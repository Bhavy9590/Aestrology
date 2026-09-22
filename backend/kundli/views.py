import json, os
from datetime import date,time
from zoneinfo import ZoneInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import KundliRequest
from .engine import calc
import requests

CACHE={}

def _location_results(q):
    key=q.lower().strip()
    if key in CACHE: return CACHE[key]
    url="https://geocoding-api.open-meteo.com/v1/search"
    r=requests.get(url,params={"name":q,"count":10,"language":"en","format":"json"},timeout=8); r.raise_for_status()
    data=r.json().get("results",[]); out=[]
    for x in data:
        label=", ".join([v for v in [x.get("name"),x.get("admin1"),x.get("country")] if v])
        out.append({"label":label,"city":x.get("name",""),"state":x.get("admin1",""),"country":x.get("country",""),"country_code":x.get("country_code",""),"lat":x.get("latitude"),"lon":x.get("longitude"),"timezone":x.get("timezone") or "UTC"})
    CACHE[key]=out; return out

@csrf_exempt
def places_api(request):
    q=request.GET.get("q","").strip()
    if len(q)<2:return JsonResponse({"results":[]})
    try:return JsonResponse({"results":_location_results(q)})
    except Exception as e:return JsonResponse({"results":[],"error":"Location service temporarily unavailable."},status=503)

@csrf_exempt
def kundli_api(request):
    if request.method!="POST":return JsonResponse({"ok":False,"error":"POST required"},status=405)
    try:
        d=json.loads(request.body); dob=date.fromisoformat(d["dob"]); tob=time.fromisoformat(d["tob"])
        lat=float(d["latitude"]); lon=float(d["longitude"]); tz=d.get("timezone") or "UTC"
        # Convert local birth time to UTC offset using the selected timezone, including historical DST.
        local=__import__('datetime').datetime.combine(dob,tob).replace(tzinfo=ZoneInfo(tz)); offset=int(local.utcoffset().total_seconds()/60)
        result=calc(dob,tob,lat,lon,tz,offset)
        KundliRequest.objects.create(name=d["name"],dob=dob,tob=tob,place=d["place"],latitude=lat,longitude=lon,timezone=tz)
        return JsonResponse({"ok":True,"name":d["name"],"place":d["place"],"birth":{"date":d["dob"],"time":d["tob"]},"kundli":result})
    except Exception as e:return JsonResponse({"ok":False,"error":str(e)},status=400)
