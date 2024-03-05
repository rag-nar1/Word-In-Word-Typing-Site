set -o errexit

pip install -r requirements.txt
python3 typingSite/manage.py collectstatic --no-input