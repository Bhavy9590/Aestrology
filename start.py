import os,sys,subprocess,time,webbrowser,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent; BACK=ROOT/'backend'; FRONT=ROOT/'frontend'; venv=BACK/'.venv'
py=venv/'Scripts'/'python.exe' if os.name=='nt' else venv/'bin'/'python'
npm=shutil.which('npm') or 'npm'
if not py.exists():
    print('Python virtual environment not found. Run install.bat first.'); sys.exit(1)
if not shutil.which('npm'):
    print('Node.js/npm not found. Install Node.js 18+ and try again.'); sys.exit(1)
if not (FRONT/'node_modules').exists():
    print('Frontend dependencies not installed. Running npm install...')
    subprocess.run(['npm','install'],cwd=FRONT,check=True)
subprocess.run([str(py),str(BACK/'manage.py'),'migrate'],check=True)
backend=subprocess.Popen([str(py),str(BACK/'manage.py'),'runserver','127.0.0.1:8000'],cwd=BACK)
frontend_cmd=[npm,'run','dev','--','--host','127.0.0.1','--port','5173']
if os.name=='nt': frontend_cmd=['cmd','/c']+frontend_cmd
frontend=subprocess.Popen(frontend_cmd,cwd=FRONT)
try:
    time.sleep(2)
    try: webbrowser.open('http://127.0.0.1:5173')
    except Exception: pass
    print('\nTarak Kundli running: http://127.0.0.1:5173')
    print('Press Ctrl+C to stop both servers.')
    while True: time.sleep(1)
except KeyboardInterrupt: pass
finally:
    for p in (frontend,backend):
        try:p.terminate()
        except:pass
