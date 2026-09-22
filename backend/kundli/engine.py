import math
from datetime import datetime, timedelta, timezone
import swisseph as swe

SIGNS=["મેષ","વૃષભ","મિથુન","કર્ક","સિંહ","કન્યા","તુલા","વૃશ્ચિક","ધન","મકર","કુંભ","મીન"]
SIGN_LORDS=["મંગળ","શુક્ર","બુધ","ચંદ્ર","સૂર્ય","બુધ","શુક્ર","મંગળ","ગુરુ","શનિ","શનિ","ગુરુ"]
NAKSHATRAS=["અશ્વિની","ભરણીઃ","કૃત્તિકા","રોહિણી","મૃગશીર્ષ","આર્દ્રા","પુનર્વસુ","પુષ્ય","આશ્લેષા","મઘા","પૂર્વાફાલ્ગુની","ઉત્તરાફાલ્ગુની","હસ્ત","ચિત્રા","સ્વાતિ","વિશાખા","અનુરાધા","જ્યેષ્ઠા","મૂળ","પૂર્વાષાઢા","ઉત્તરાષાઢા","શ્રવણ","ધનિષ્ઠા","શતભિષા","પૂર્વાભાદ્રપદ","ઉત્તરાભાદ્રપદ","રેવતી"]
NAK_LORDS=["કેતુ","શુક્ર","સૂર્ય","ચંદ્ર","મંગળ","રાહુ","ગુરુ","શનિ","બુધ"]*3
DASHA_YEARS={"કેતુ":7,"શુક્ર":20,"સૂર્ય":6,"ચંદ્ર":10,"મંગળ":7,"રાહુ":18,"ગુરુ":16,"શનિ":19,"બુધ":17}
DASHA_ORDER=["કેતુ","શુક્ર","સૂર્ય","ચંદ્ર","મંગળ","રાહુ","ગુરુ","શનિ","બુધ"]
PLANETS=[("સૂર્ય",swe.SUN), ("ચંદ્ર",swe.MOON), ("બુધ",swe.MERCURY), ("શુક્ર",swe.VENUS), ("મંગળ",swe.MARS), ("ગુરુ",swe.JUPITER), ("શનિ",swe.SATURN), ("રાહુ",swe.MEAN_NODE)]

def _sign(deg):
    i=int((deg%360)//30); within=deg%30
    return i, SIGNS[i], within

def _nak(deg):
    span=360/27; idx=int((deg%360)//span); within=(deg%360)-idx*span
    pada=min(4,int(within/(span/4))+1)
    return idx, NAKSHATRAS[idx], pada, NAK_LORDS[idx]

def _fmt_date(dt): return dt.strftime("%Y-%m-%d")

def _jd_utc(local_dt, offset_minutes):
    utc=local_dt - timedelta(minutes=offset_minutes)
    return swe.julday(utc.year,utc.month,utc.day,utc.hour+utc.minute/60+utc.second/3600)

def _planet_positions(jd):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags=swe.FLG_SWIEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
    out=[]
    for name,p in PLANETS:
        xx,_=swe.calc_ut(jd,p,flags)
        deg=xx[0]%360; si,rashi,within=_sign(deg); ni,nak,pada,nlord=_nak(deg)
        out.append({"name":name,"longitude":round(deg,6),"degree":round(within,4),"rashi":rashi,"rashi_index":si,"house":None,"nakshatra":nak,"nakshatra_pada":pada,"nakshatra_lord":nlord,"retrograde":bool(xx[3]<0)})
    rahu=out[-1]["longitude"]; ketu=(rahu+180)%360; si,rashi,within=_sign(ketu); ni,nak,pada,nlord=_nak(ketu)
    out.append({"name":"કેતુ","longitude":round(ketu,6),"degree":round(within,4),"rashi":rashi,"rashi_index":si,"house":None,"nakshatra":nak,"nakshatra_pada":pada,"nakshatra_lord":nlord,"retrograde":True})
    return out

def _houses(jd,lat,lon):
    cusps, angles=swe.houses_ex(jd,lat,lon,b'P', flags=0)
    # houses_ex returns tropical cusps; siderealize by subtracting ayanamsha
    ay=swe.get_ayanamsa_ut(jd)
    sid_cusps=[(c-ay)%360 for c in cusps]
    asc=(angles[0]-ay)%360
    return sid_cusps,asc

def _house_for_lon(lon,cusps):
    # cusps indexed 0..11 for houses 1..12
    for i in range(12):
        a=cusps[i]; b=cusps[(i+1)%12]
        if i==11: b+=360
        x=lon
        if i==11 and x<a: x+=360
        if a<=x<b: return i+1
    return 12

def _navamsa(lon):
    si=int((lon%360)//30); within=(lon%30); part=int(within/(30/9))
    # Movable signs start from same sign, fixed from 9th, dual from 5th.
    if si%3==0: start=si
    elif si%3==1: start=(si+8)%12
    else: start=(si+4)%12
    nsi=(start+part)%12
    return SIGNS[nsi],nsi

def _dasha(jd, birth_local, moon_lon):
    idx, nak, pada, lord=_nak(moon_lon); span=360/27; elapsed=(moon_lon-(idx*span))/(span)
    elapsed=min(max(elapsed,0),1)
    remaining_years=DASHA_YEARS[lord]*(1-elapsed)
    start_idx=DASHA_ORDER.index(lord)
    cur_start=birth_local
    first_end=cur_start+timedelta(days=remaining_years*365.2425)
    periods=[]; cursor=cur_start
    for k in range(9):
        ml=DASHA_ORDER[(start_idx+k)%9]
        years=remaining_years if k==0 else DASHA_YEARS[ml]
        end=cursor+timedelta(days=years*365.2425)
        periods.append({"lord":ml,"start":_fmt_date(cursor),"end":_fmt_date(end),"years":round(years,3)})
        cursor=end
    now=datetime.now().replace(tzinfo=None)
    if now < birth_local.replace(tzinfo=None):
        now=birth_local.replace(tzinfo=None)
    current=next((p for p in periods if datetime.fromisoformat(p["start"])<=now<=datetime.fromisoformat(p["end"])), periods[0])
    # Antardasha inside current mahadasha, proportional to MD years.
    ml=current["lord"]; md_years=DASHA_YEARS[ml]
    cstart=datetime.fromisoformat(current["start"]); cend=datetime.fromisoformat(current["end"])
    elapsed_days=max(0,(now-cstart).total_seconds()/86400); total_days=max(1,(cend-cstart).total_seconds()/86400)
    seq_start=DASHA_ORDER.index(ml); cursor=cstart; antars=[]
    for j in range(9):
        al=DASHA_ORDER[(seq_start+j)%9]
        days=total_days*(DASHA_YEARS[al]/120)
        end=cursor+timedelta(days=days)
        antars.append({"lord":al,"start":_fmt_date(cursor),"end":_fmt_date(end)})
        cursor=end
    antar=next((a for a in antars if datetime.fromisoformat(a["start"])<=now<=datetime.fromisoformat(a["end"])),antars[0])
    return {"birth_nakshatra":nak,"nakshatra_lord":lord,"mahadasa":periods,"current_mahadasa":current,"antardasha":antars,"current_antardasha":antar}

def _panchang(jd, local_dt):
    swe.set_sid_mode(swe.SIDM_LAHIRI); flags=swe.FLG_SWIEPH|swe.FLG_SIDEREAL
    sun=swe.calc_ut(jd,swe.SUN,flags)[0][0]%360; moon=swe.calc_ut(jd,swe.MOON,flags)[0][0]%360
    elong=(moon-sun)%360; tno=int(elong//12)+1; paksha="શુક્લ પક્ષ" if tno<=15 else "કૃષ્ણ પક્ષ"; num=tno if tno<=15 else tno-15
    tithi_names=["પ્રતિપદા","દ્વિતીયા","તૃતીયા","ચતુર્થી","પંચમી","ષષ્ઠી","સપ્તમી","અષ્ટમી","નવમી","દશમી","એકાદશી","દ્વાદશી","ત્રયોદશી","ચતુર્દશી","પૂર્ણિમા"]
    tithi=tithi_names[num-1] if num<=15 else "અમાવસ્યા"
    vara=["સોમવાર","મંગળવાર","બુધવાર","ગુરુવાર","શુક્રવાર","શનિવાર","રવિવાર"][local_dt.weekday()]
    yoga_names=["વિષ્કંભ","પ્રીતિ","આયુષ્માન","સૌભાગ્ય","શોભન","અતિગંડ","સુકર્મા","ધૃતિ","શૂલ","ગંડ","વૃદ્ધિ","ધ્રુવ","વ્યાઘાત","હર્ષણ","વજ્ર","સિદ્ધિ","વ્યતિપાત","વરીયાન","પરિઘ","શિવ","સિદ્ધ","સાધ્ય","શુભ","શુક્લ","બ્રહ્મ","ઇન્દ્ર","વૈધૃતિ"]
    yoga_no=int(((sun+moon)%360)/(360/27)); yoga=yoga_names[yoga_no]
    karana_names=["બવ","બાલવ","કૌલવ","તૈતિલ","ગર","વણિજ","વિષ્ટિ","શકુનિ","ચતુષ્પાદ","નાગ","કિંસ્તુઘ્ન"]
    karana_no=int(elong//6)
    if karana_no==0: karana=karana_names[-1]
    elif karana_no>=57: karana=karana_names[(karana_no-57)%7]
    else: karana=karana_names[(karana_no-1)%7]
    return {"tithi":tithi,"paksha":paksha,"number":num,"vara":vara,"yoga":yoga,"karana":karana}

def calc(dob,tob,lat,lon,timezone_name="Asia/Kolkata",offset_minutes=330):
    local_dt=datetime.combine(dob,tob); jd=_jd_utc(local_dt,offset_minutes)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    planets=_planet_positions(jd); cusps,asc=_houses(jd,lat,lon); li,lagna,ldeg=_sign(asc); moon=next(p for p in planets if p["name"]=="ચંદ્ર")
    for p in planets: p["house"]=_house_for_lon(p["longitude"],cusps)
    houses=[]
    for i,c in enumerate(cusps):
        si,rashi,deg=_sign(c); houses.append({"house":i+1,"rashi":rashi,"rashi_index":si,"degree":round(deg,4),"lord":SIGN_LORDS[si]})
    ni,nak,pada,nlord=_nak(moon["longitude"])
    d9={"lagna":_navamsa(asc)[0],"planets":[{"name":p["name"],"rashi":_navamsa(p["longitude"])[0],"rashi_index":_navamsa(p["longitude"])[1]} for p in planets]}
    dasha=_dasha(jd,local_dt,moon["longitude"])
    return {"ayanamsha":round(swe.get_ayanamsa_ut(jd),6),"lagna":lagna,"lagna_degree":round(ldeg,4),"lagna_longitude":round(asc,6),"moon_rashi":moon["rashi"],"sun_rashi":next(p for p in planets if p["name"]=="સૂર્ય")["rashi"],"janma_nakshatra":nak,"nakshatra_pada":pada,"nakshatra_lord":nlord,"planets":planets,"houses":houses,"navamsa":d9,"dasha":dasha,"panchang":_panchang(jd,local_dt),"location":{"latitude":lat,"longitude":lon,"timezone":timezone_name,"utc_offset_minutes":offset_minutes},"note":"વૈદિક/Sidereal ગણતરી · Lahiri Ayanamsha · Swiss Ephemeris."}
