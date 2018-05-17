### Train

1. Place the images which are going to be analyzed at the `images to classify` folder, and the videos at the `Videos` folder.

2. Run the program `extratc.py`, which can be executed by the command *python extract.py*, in the console.
        This program will get frames out of every video in the videos directory, and send those frames to the `images to classify` folder. After this process is done, all the videos will be deleted.

3. Run the program `check.py`, which can be executed by the command *python check.py*, in the console.
        A new window will pop up, in which you are allowed to to view all the marks in the images assigned by the program, which are stored in the `annotations DNN` folder.
        To begin, its necessary to click `Open Dir`, followed by `open` in the the new window that will pop up. It`s not necessary to concern about the directory for it will aways open in the right path.
        A list of 5 images will be showed, and all the respective assignments made by the software, you can scroll by the images pressing the `A` and `D` keys.
        In case that a mark was wrongly made, you can left click about it and press delete in order to exclude it.
        In case that something went missing by the software, you can press the `w` key, and select its attribute.
        You can also adjust the displacement of the mark, or its size by moving its corners, its adviced to mark exactly what is intended, no excesses in the mark.
        In order to avoid having to save after every image change, its possible to select the option `Auto saving` in the `view` menu.
        After the review is done, close the program and a message in the console will let you continue marking new 5 images or finish this process.
        Once the training by user is done, the analized images will be move to the `imagesTrain` folder.
        All the changes made by user are stored in the `annotations` folder.

4. Run the program `treinando_rede.sh`, which can be executed by the command *./treinando_rede.sh*, in the console.
        Here is where the learning happens, based on the markings, the software will run a series of iterations which will converge for a better output.
        Due to high number of iterations its adviced to stop the process after due time.
	If you already runned this program and whant to do a new training, it is importante to exclude the folder `Models`.

5. Run the program `zipNetwork.sh`, which can be executed by the command *./zipNetwork.sh*, in the console.

6. In order to test the trained network, it is important to exclude the `annotationsDNN` folder and run the `extract.py` again.
	This way, the program will use new images and create the labels, after creating a new folder `annotationsDNN`.
