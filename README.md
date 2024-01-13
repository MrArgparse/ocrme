Install with `pip install git+https://github.com/MrArgparse/ocrme.git`

Uninstall with `pip uninstall ocrme` and delete the `.config/ocrme` folder in your home directory.

Convert an image on the terminal by doing `ocrme 'test.png'`

Save it to a text file as well by using `ocrme 'test.png' --text`

The default path for tesseract on Windows inside the config file is:
`'C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'`

For linux default path for tesseract on Linux inside the config file is:
`'/usr/bin/tesseract'`

Make sure it is installed and feel free to change these values if you installed in somewhere else than the default directory.

The default output path for the text files is the user home directory (on windows C:/Users/name) and the default set of extensions supported is: [".bmp", ".gif", ".jpg", ".jpeg", ".png"]

You are free to change that as well in the config file.

People on linux will have to export the path of tesseract ocr in their .bashrc

Example (location may vary):

`export PATH="/usr/bin/tesseract:$PATH"`
