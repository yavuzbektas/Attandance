pyuic5 icons.qrc -o icons_rc.py
convert_main
pyuic5 -x video.ui > video.py
pyuic5 -x mainwindow.ui > mainwindow.py
