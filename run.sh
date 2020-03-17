date=`date +%Y%m%d-%H%M%S`
python -u main.py > log-$date.txt 2>&1
