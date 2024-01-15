echo " _________________________________BUILD START ___________________________"
python3.9 -m pip install wheel
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo " _______________________________________BUILD END_________________________" 

