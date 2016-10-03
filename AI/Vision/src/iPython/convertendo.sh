Light_Green='\33[1;32m'
blue='\33[0;34m'
NC='\33[0m' # No Color
#font colors:
#Black				0;30		Dark Gray			1;30
#Blue					0;34		Light Blue		1;34
#Green				0;32		Light Green		1;32
#Cyan					0;36		Light Cyan		1;36
#Red					0;31		Light Red			1;31
#Purple				0;35		Light Purple	1;35
#Brown/Orange	0;33		Yellow				1;33
#Light Gray		0;37		White					1;37

echo "${blue}Convertendo ipynb${NC}"
#sleep 2
jupyter nbconvert --to python *.ipynb


echo "${blue}Arrumando arquivo Python${NC}"
#sleep 2
sed -i 1d *.py
sed -i ':a;N;$!ba;s/    /\t/g' *.py
sed -i "s/In[[][^)]*[]]/In[]/g" *.py
sed -i ':a;N;$!ba;s/\n\n# In\[]:\n//g' *.py
#sed -i '2a\\n' *.py
sed -i '/#ini-iPython/,/#end-iPython/c\' *.py
sed -i '/get_ipython/d' *.py
sed -i '/plt/d' *.py
sed -i 's/matplotlib.pyplot/plt/g' *.py
sed -i 's/import plt/import matplotlib.pyplot as plt/g' *.py
sed -i 's/# #/##/g' *.py
sed -i -e '/#edes-iPython /{n;d}' *.py
sed -i 's/#edes-iPython //g' *.py
sed -i 's/#des-iPython //g' *.py

echo "${Light_Green}Finalizado${NC}"
#sleep 3

