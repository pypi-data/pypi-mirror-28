A powerful and useful package for remote sensing image&video preocessing.

-"image" model contains useful functions for image processing such as image bit-depth convert.

-"video" model contains useful functions for video processing.

-"common" model contains some function for common use,such as findAllFiles().

IMPORTANT Dependencies:

* OpenCV
* GDAL

Usually,PIP will auto download and install dependencies,but if it failed you can install them manually with these commands.

pip install opencv-python

pip install gdal

OpenCV website: https://pypi.python.org/pypi/opencv-python

GDAL package website: https://pypi.python.org/pypi/GDAL/2.2.3

But sometimes it may be a little hard to install gdal using this command because it needs some other dependencies to compile.

For Windows Users:

So you can install it from wheel file.You can search and select gdal wheel file at this website.

https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

Or if you are using Anaconda,there is an easier way.Use this command to install gdal.

conda install gdal

For Linux/Unix Users:

You may have to install dependencies manually according to instructions on GDAL package website.Here are the dependencies for GDAL.

* libgdal (2.2.3 or greater) and header files (gdal-devel)
* numpy (1.0.0 or greater) and header files (numpy-devel) (not explicitly required, but many examples and utilities will not work without it)

Or you can install it directly with Anaconda,the same way as windows users do.That may be the easiest way to install.

After finish installing GDAL, you can try to install RStoolkit again.It should be successful.
If you have any problem installing and using this package,you can connect me via email.

E-mail:zhaoxuhui@whu.edu.cn

Enjoy it!


