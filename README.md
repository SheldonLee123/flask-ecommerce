#activate virtual environment  
virtualenv venv  
source venv/bin/activate  
pip install -r requirments.txt  

#create database  
python db_create.py  

#run   
python run.py  

#ubuntu+flask+nginx+uwsgi deployment  
sudo rm /etc/nginx/sites-enabled/default  
sudo ln -s /var/www/ecommerce/ecommerce_nginx.conf /etc/nginx/conf.d/  
sudo /etc/init.d/nginx start  
nohup uwsgi --ini /var/www/ecommerce/ecommerce_uwsgi.ini &  

