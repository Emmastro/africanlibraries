cd $1
sed -i 's/assets/\/static/g' index.html
sed -i 's/assets/\/static/g' login.html
mv index.html templates/index.html
mv login.html templates/login.html
mv assets static
