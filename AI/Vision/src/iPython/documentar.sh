blue='\33[0;34m'
orange='\033[0;33m'
light_Green='\33[1;32m'
yellow='\33[1;33m'
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

echo "${orange}Apagando arquivos antigos${NC}"
sleep 2
./zerar.sh

echo "${orange}Gerando Documentação${NC}"
sleep 2
mkdir ./Documentacao
doxygen Doxyfile*

echo "${orange}Alterando documento${NC}"
sleep 2
cd ./Documentacao/latex
echo "${yellow}  Mudando titulo${NC}"
sed -i 's/Gerado por Doxygen 1.8.11/Vinícius Nicassio Ferreira/g' refman.tex

echo "${yellow}  Removendo paginas em branco${NC}"
sleep 1
sed -i ':a;N;$!ba;s/[\]clearemptydoublepage\n/%\\clearemptydoublepage\n/g' refman.tex

echo "${yellow}  Arrumando margem${NC}"
sleep 1
sed -i 's/top=2.5cm/top=3cm/g' refman.tex
sed -i 's/left=2.5cm/left=3cm/g' refman.tex

echo "${yellow}  Separando sumario${NC}"
sleep 1
sed -i ':a;N;$!ba;s/[\]tableofcontents\n/\\tableofcontents\n\\clearemptydoublepage\n/g' refman.tex

echo "${yellow}  Removendo section${NC}"
sleep 1
sed -i ':a;N;$!ba;s/[\]section[{]Índice dos Arquivos[}]\n/%\\section{Índice dos Arquivos}\n%/g' refman.tex
sed -i ':a;N;$!ba;s/[\]section[{]Índice Hierárquico[}]\n/%\\section{Índice Hierárquico}\n%/g' refman.tex
#texmaker refman.tex

echo "${orange}Gerando PDF${NC}"
sleep 2
make all
cp refman.pdf ./Documentacao.pdf
mate-terminal -x sh -c 'atril ./Documentacao.pdf'

echo "${light_Green}Finalizado${NC}"
sleep 5
