#activate virtual environment  
source venv/bin/activate  

#create database  
python db_create.py  

#run   
python run.py  

#ubuntu+flask+nginx+uwsgi deployment
sudo /etc/init.d/nginx start  
nohup uwsgi --ini /var/www/ecommerce/ecommerce_uwsgi.ini &  

