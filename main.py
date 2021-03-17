# #######################################
# __file__ = "main.py"
# __author__ = "Yavuz Bektaş"
# __version__ = "1.0"
# __email__ = "yavuzbektas@gmail.com"
# __linkdin__ = "yavuzbektas@gmail.com"
# __release_date__ = "2020.04.23"
# #######################################

import pickle
import shutil
import socket
import sqlite3
import struct
from datetime import datetime
from sqlite3 import Error

import cv2
import face_recognition
import pyzbar.pyzbar as pyzbar
from PyQt5 import QtCore, QtGui
# from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from xlrd import *
from xlsxwriter import *

import login
import video
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
# import threading
# import numpy as np
# UI files  ===========================
from mainwindow import Ui_MainWindow

# ===========  GLOBAL DATA  ===========================
global citizenship_ID
global username, language
language = "Turkish"
citizenship_ID = 0
ID = 0
LANGUAGE = "turkish"
global lblImage
video_capture = cv2.VideoCapture(0)
global known_face_encodings, known_face_names
known_face_encodings = []
known_face_names = []
global camera_is_open
global btnOpenCamera
global old_imagepath
global image_uploaded_flag
global kamera
kamera = "picamera"
image_uploaded_flag = False
# ============================================================================
# ================   SETTINGS     ===================================
BASE_PATH = os.getcwd()
IMAGE_DIR = (BASE_PATH + '\\faces\\')
FILE_DIR = (BASE_PATH + '\\staticfiles\\CVFiles\\')
REPORT_DIR = (BASE_PATH + '\\staticfiles\\Reports\\')

LANGUAGES_DIR = (BASE_PATH + '\\staticfiles\\languages\\')
DATABASE_DIR = (BASE_PATH + '\\db_personals.db')
print('Resim Dosyalar : {} klasöründe ve  CV Dosyları : {} kalasöründe yer almaktadır. '.format(IMAGE_DIR, FILE_DIR))


# =====================Create Database=============================================

def createdb():
    conn = sqlite3.connect(DATABASE_DIR)
    c = conn.cursor()
    sql = """
    CREATE TABLE personal (
    ID             INTEGER       PRIMARY KEY AUTOINCREMENT
                                 UNIQUE
                                 NOT NULL,
    Citizen_number INT           UNIQUE,
    name           VARCHAR (30),
    surname        VARCHAR (30),
    email          VARCHAR (120),
    telephone      INTEGER (12),
    birhday        DATE,
    joinday        DATE,
    city           VARCHAR (30),
    state          VARCHAR (30),
    adress         TEXT,
    social        TEXT,
    departmant_id  INT,
    status         BOOLEAN       DEFAULT (0),
    face_status    BOOLEAN,
    hes_code       VARCHAR (30),
    record_date    DATETIME      DEFAULT (CURRENT_TIMESTAMP))"""
    sql2 = """CREATE TABLE attandance (
    ID          INTEGER      UNIQUE
                             PRIMARY KEY AUTOINCREMENT,
    personal_ID INT          REFERENCES personal (citizen_ID) ON DELETE CASCADE
                                                              ON UPDATE CASCADE,
    status      VARCHAR (20),
    date        DATE,
    time        TIME,
    record_date DATETIME     DEFAULT (CURRENT_TIMESTAMP))"""
    try:
        c.execute(sql)
        print("the Database has been created")
        conn.commit()
        c.execute(sql2)
        print("the Database has been created")
        conn.commit()
    except:
        print("The table of  personal already exists")

    finally:
        conn.close()


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


class Thread_temp(QtCore.QThread):
    leds_status = QtCore.pyqtSignal(str)
    tempreture = QtCore.pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.flag = False

    def run(self):
        host = "192.168.0.100"
        port = 8001

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("socket oluşturuldu")

            s.bind((host, port))
            print("socket {} nolu porta bağlandı".format(port))

            s.listen(5)
            print("socket dinleniyor")
        except socket.error as msg:
            print("Hata:", msg)

        self.flag = True
        while self.flag:
            # Client ile bağlantı kurulursa
            c, addr = s.accept()
            print('Gelen bağlantı:', addr)

            # Bağlanan client tarafına hoşgeldin mesajı gönderelim.
            mesaj = str(self.leds_status)
            data = c.recv(1024)
            data, = struct.unpack("f", data)

            self.tempreture.emit(data)
            c.send(mesaj.encode('utf-8'))
            print(data)
            # Bağlantıyı sonlandıralım
            c.close()

    def stop(self):
        self.flag = False


class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    face_id = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.flag = False

    def run(self):
        # cap1 = cv2.VideoCapture(0)

        if kamera == "picamera":
            cap1 = cv2.VideoCapture("http://192.168.0.103:8000/stream.mjpg")
            cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            frames_count, fps, width, height = cap1.get(cv2.CAP_PROP_FRAME_COUNT), cap1.get(cv2.CAP_PROP_FPS), cap1.get(
                cv2.CAP_PROP_FRAME_WIDTH), cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(frames_count, fps, width, height)

        else:
            cap1 = cv2.VideoCapture(0)
        self.flag = True
        while self.flag:
            # ret, frame = cap1.read()
            for i in range(20):
                cap1.grab()

            ret, frame = cap1.read()
            self.faceRecognitionFromPicture(frame)
            # if ret:

    def stop(self):
        self.flag = False

    def faceRecognitionFromPicture(self, cvframe):

        print("---- Recognized Started ----")
        small_frame = cv2.resize(cvframe, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        small_rgb_frame = small_frame[:, :, ::-1]
        # get face location
        face_locations = face_recognition.face_locations(small_rgb_frame)
        print("- Face location scan completed")
        face_encodings = face_recognition.face_encodings(
            small_rgb_frame, face_locations)
        face_names = []
        print(face_names)
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = ""  # default name is not recognized

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                self.face_id.emit(name)

            else:
                self.face_id.emit("Tanınmıyor")
            face_names.append(name)
            Thread.sleep(3)
            self.face_id.emit("")
            small_frame = ""

        print("- Face Locations:")
        # print face data
        print(*face_locations, sep='\n')
        print(*face_names, sep='\n')
        print("- Face name searching completed")
        # draw face rectangle and name on current frame
        self.drawFaceOnImage(cvframe, face_locations, face_names)
        # Label string
        faceNames = ''.join(face_names)
        count = str(len(face_locations))
        location = ','.join([str(i) for i in face_locations])
        return_string = "\nNames: " + faceNames + \
                        "\nFace Count: " + count + "\nLocations: " + location + "\n"
        print(return_string)

        print("---- Recognized Completed ----")

        # self.face_id.emit("")

    def drawFaceOnImage(self, frame, face_locations, face_names):

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (153, 0, 51), 4)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, top + 35),
                          (right, top), (153, 0, 51), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 10, top + 25),
                        font, 1.0, (255, 255, 255), 2)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cvt2qt = QtGui.QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QtGui.QImage.Format_RGB888)
            self.changePixmap.emit(cvt2qt)

        # write temp image file for lblimage item
        # cv2.imwrite("faces/temp.jpg", frame)


class VideoWindow(QDialog, video.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(VideoWindow, self).__init__(parent, *args, **kwargs)
        self.ui = video.Ui_Dialog()
        self.videoDialog = parent
        self.ui.setupUi(self)
        self.setWindowTitle('Video Capture')
        self.handle_button()
        self.th = Thread(self)

        self.th_temp = Thread_temp(self)

    def handle_button(self):
        self.ui.pushButton.clicked.connect(self.mythread_start)
        self.ui.pushButton_2.clicked.connect(self.stop_thread)

    def mythread_start(self):

        self.th.changePixmap.connect(self.setImage)
        self.th.face_id.connect(self.facename_matches)
        self.th_temp.tempreture.connect(self.tempreture_read)
        self.th.start()
        self.th_temp.start()

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        pass
        # self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image))

    @QtCore.pyqtSlot(str)
    def facename_matches(self, name):

        self.ui.label_2.setText(name)

        if name != "" and name != "Tanınmıyor":
            self.th_temp.leds_status = "on-off"
        elif name == "Tanınmıyor":
            self.th_temp.leds_status = "off-on"
        else:
            self.ui.label_2.setText("")
            self.th_temp.leds_status = "off-off"
        self.call_recoreded_image_from_sql(name)

    @QtCore.pyqtSlot(float)
    def tempreture_read(self, value):

        if self.ui.label_2.text() != "" and self.ui.label_2.text() != "Tanınmıyor":
            self.ui.doubleSpinBox.setValue(value + 2)
            self.ui.label_30.setVisible(True)

        elif self.ui.label_2.text() == "Tanınmıyor":
            self.ui.doubleSpinBox.setValue(value + 2)
            self.ui.label_30.setVisible(False)

        else:
            self.ui.doubleSpinBox.setValue(0)
            self.ui.label_30.setVisible(False)

        if self.ui.doubleSpinBox.value() > 37.0:

            brush = QtGui.QBrush(QtGui.QColor(250, 0, 0))
        else:
            brush = QtGui.QBrush(QtGui.QColor(30, 255, 64))
        palette = QtGui.QPalette()
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        self.ui.doubleSpinBox.setPalette(palette)

    def stop_thread(self):
        try:
            if self.th.flag == True:
                self.th.stop()
                self.th_temp.stop()
                # self.th.quit()
                self.th.wait()

        except:
            print("hatalı bişeyler var")

    def closeEvent(self, event):

        if self.th.flag == True:
            self.th.stop()
            self.th_temp.stop()
            # self.th.quit()
            self.th.wait()
            self.th_temp.wait()
        super(VideoWindow, self).closeEvent(event)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_S:

            try:
                name = self.ui.label_2.text()
                name = name.split("_")
                print(int(name[0]), type(name[0]))
                id_no = int(name[0])
                self.add_new_attandance_record()
            except:
                print("you are not recognized.")

    def add_new_attandance_record(self):
        name = self.ui.label_2.text()
        name = name.split("_")
        citizen_ID = name[0]
        status = "Arrived"
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        date_val = current_date
        time_val = current_time

        sql = """ INSERT INTO attandance  (citizen_ID,status,date,time) VALUES (?,?,?,?)"""
        conn = create_connection(DATABASE_DIR)
        cur = conn.cursor()
        cur.execute(sql, (citizen_ID, status, date_val, time_val))
        conn.commit()
        conn.close()
        print("New data has been recorded succesfully .")

        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(
            "Hello {} . I recocnized you . Wellcome to school. \nYour attandance data has been recorded intp DB succesfully.\nto Continue please Press OK button".format(
                name[1]))
        msgBox.setWindowTitle("Information - All data have been recorded into DB")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def call_recoreded_image_from_sql(self, name):
        try:
            if name == "Tanınmıyor" or name == "":
                self.ui.label.setPixmap(QPixmap(None))
                return False
            ID = name.split(sep="_")[0]
            conn = create_connection(DATABASE_DIR)

            sql = """ SELECT profil_image FROM personal WHERE citizen_ID={}""".format(ID)
            cur = conn.cursor()

            cur.execute(sql)
            data = cur.fetchone()
        except:
            data = ""
        profil_image = data[0]
        self.ui.label.setPixmap(QPixmap(None))
        if data != "":
            pic_path = profil_image
            picture = QPixmap(pic_path)
            self.ui.label.setPixmap(picture)
            self.ui.label.setScaledContents(True)

        else:
            self.ui.label.setPixmap(QPixmap(None))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Okul Takip Yönetim Sistemi')
        self.handle_button()
        self.personal_showlist_on_tabwidget()
        self.videoDialog = VideoWindow(self)
        self.ui.tabWidget.tabBar().setVisible(False)
        self.import_trained_file()

    def import_trained_file(self):
        try:
            with open("test_images.txt", 'rb') as f:
                global known_face_encodings
                known_face_encodings = pickle.load(f)

            with open("test_names.txt", 'rb') as f:
                global known_face_names
                known_face_names = pickle.load(f)


        except:
            print("hatalı dosya")

    def handle_button(self):
        self.ui.actionAbout.triggered.connect(lambda x: self.ui.tabWidget.setCurrentIndex(5))
        self.ui.actionExit.triggered.connect(lambda x: self.close())
        self.ui.pushButton_12.clicked.connect(self.personal_field_check)
        self.ui.pushButton_13.clicked.connect(self.personal_existing_check)
        self.ui.pushButton_16.clicked.connect(self.personal_screen_clear)
        self.ui.pushButton_14.clicked.connect(self.personal_delete)
        self.ui.tableWidget.itemClicked.connect(self.personal_detial_upload_from_tablewidget)
        self.ui.pushButton_11.clicked.connect(self.personal_tabwidget_query)

        self.ui.pushButton_15.clicked.connect(self.image_file_dialog_open)
        self.ui.pushButton_17.clicked.connect(self.trainFaces)

        self.ui.pushButton_18.clicked.connect(self.attandance_showlist_on_tabwidget)
        self.ui.tableWidget_2.itemClicked.connect(self.attandance_detial_upload_from_tablewidget)
        self.ui.pushButton.clicked.connect(self.turn_login_page)
        self.ui.pushButton_22.clicked.connect(self.attandence_update)
        self.ui.pushButton_23.clicked.connect(self.attandence_delete)
        self.ui.pushButton_20.clicked.connect(self.attandence_export_entered_date)
        self.ui.pushButton_19.clicked.connect(self.attandence_export_today)
        self.ui.pushButton_21.clicked.connect(self.attandence_delete_entered_record)
        self.ui.pushButton_24.clicked.connect(self.attandence_send_email)

        # ================  themes ==========================
        self.ui.pushButton_3.clicked.connect(self.theme_1)
        self.ui.pushButton_4.clicked.connect(self.theme_2)
        self.ui.pushButton_5.clicked.connect(self.theme_3)

    # ================ TABS CONTROL  ===========================================
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.ui.tabWidget.setCurrentIndex(0)

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        self.ui.tabWidget.setCurrentIndex(1)

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        self.ui.tabWidget.setCurrentIndex(2)

    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        self.faceRecognitionFromPicture()

    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        self.ui.tabWidget.setCurrentIndex(4)

    @pyqtSlot()
    def on_pushButton_10_clicked(self):
        self.ui.tabWidget.setCurrentIndex(5)

    @pyqtSlot()
    def on_pushButton_hescode_check_clicked(self):
        self.ui.tabWidget.setCurrentIndex(6)

    @pyqtSlot()
    def on_pushButton_read_qrcode_clicked(self):
        print("QR code is Reading")
        self.read_qr_code()
        print("QR code Reading is completed")

    @pyqtSlot()
    def on_pushButton_hesCheck_clicked(self):
        list_code = ["T3U8-3292-11", "T3U8-3292-10", "B7J5-2525-13"]
        msgBox = QMessageBox(self)

        if self.ui.lineEdit_hescode_2.text() in list_code:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Bu Kişi Risk İçermememektedir.")
        else:
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Hastalık Riski Taşımaktadır Dikkat")
        msgBox.setWindowTitle("Hes Kodu Kontrol ")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    # ============================================================================
    # ================ THEMES ================================================

    def theme_1(self):
        style = open('staticfiles/themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def theme_2(self):
        style = open('staticfiles/themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def theme_3(self):
        style = open('staticfiles/themes/qdarkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    # ============================ ===========================================
    # ================ PERSONAL FORM =========================================
    def personal_field_check(self):
        if self.ui.lineEdit_12.text() == "":
            print("Civilization ID is empty")
            self.error_message_missingField("Civilation ID")
            return False

        if self.ui.lineEdit_3.text() == "":
            print("Name field  is empty")
            self.error_message_missingField("Name")
            return False

        if self.ui.lineEdit_4.text() == "":
            print("SurName field  is empty")
            self.error_message_missingField("SurName")
            return False

        if self.ui.lineEdit_5.text() == "":
            print("E-mail field  is empty")
            self.error_message_missingField("E-mail")
            return False

        if self.ui.lineEdit_6.text() == "":
            print("Telephone field  is empty")
            self.error_message_missingField("Telephone")
            return False

        if self.ui.lineEdit_7.text() == "":
            print("Birthday field  is empty")
            self.error_message_missingField("Birthday ")
            return False

        if self.ui.lineEdit_8.text() == "":
            print("Joining Date field  is empty")
            self.error_message_missingField("Joining Date ")
            return False

        if self.ui.comboBox_3.currentIndex() == 0:
            print("Departure is not selected ")
            self.error_message_missingField("Department")
            return False
        print("All Fields are OK")
        self.personal_existing_check()

    def personal_existing_check(self):
        global citizenship_ID
        citizenship_ID = int(self.ui.lineEdit_12.text())
        conn = create_connection(DATABASE_DIR)

        sql = """ SELECT * FROM personal WHERE citizen_ID={}""".format(citizenship_ID)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
        if data:
            print("This record is already available.")
            self.personal_update()
        else:
            print("New data will be recorded.")
            self.personal_add()
        conn.close()

    def personal_add(self):
        global image_uploaded_flag
        global old_imagepath
        global citizenship_ID
        citizenship_ID = int(self.ui.lineEdit_12.text())
        name = self.ui.lineEdit_3.text()
        surname = self.ui.lineEdit_4.text()
        email = self.ui.lineEdit_5.text()
        telephone = self.ui.lineEdit_6.text()
        birthdate = self.ui.lineEdit_7.text()
        startdate = self.ui.lineEdit_8.text()
        city = self.ui.lineEdit_10.text()
        state = self.ui.lineEdit_9.text()
        adress = self.ui.textEdit.toPlainText()
        social = self.ui.lineEdit_11.text()
        department = self.ui.comboBox_3.currentText()
        status = self.ui.comboBox_2.currentText()
        hes_code = self.ui.lineEdit_hescode.text()
        new_file_name = str(citizenship_ID) + "_" + name + " " + surname + ".jpg"

        if image_uploaded_flag == True:
            pic_path = old_imagepath
            shutil.copyfile(old_imagepath, IMAGE_DIR + new_file_name)
            picture = QPixmap(pic_path)
            self.ui.label_13.setPixmap(picture)
            self.ui.label_13.setScaledContents(True)
            profil_image = IMAGE_DIR + new_file_name
            image_uploaded_flag == False
        else:
            profil_image = ""

        face_status = "0"

        sql = """ INSERT INTO personal (citizen_ID,name,surname,email,telephone,birthdate,startdate,city,state,
                       adress,social,departmant_id,status,face_status,profil_image,hes_code) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        conn = create_connection(DATABASE_DIR)
        cur = conn.cursor()
        cur.execute(sql, (citizenship_ID, name, surname, email, telephone, birthdate, startdate, city, state, adress,
                          social, department, status, face_status, profil_image, hes_code))
        conn.commit()
        conn.close()
        print("New data has been recorded succesfully .")
        self.statusBar().showMessage('New data has been recorded succesfully')

        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(
            "This {} record belongs to {} {} has been recorded succesfully.\nto Continue please Press OK button".format(
                citizenship_ID, name, surname))
        msgBox.setWindowTitle("Information - All data have been added into DB")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.personal_showlist_on_tabwidget()

    def image_file_dialog_open(self):
        global old_imagepath
        global image_uploaded_flag
        old_imagepath, _ = QFileDialog.getOpenFileName(filter='Resim Dosyası *.jpg')
        filename = QFileInfo(old_imagepath).fileName()

        if filename:
            pic_path = old_imagepath

            # pic_path = IMAGE_DIR + new_file_name
            # shutil.copyfile(filepath, IMAGE_DIR + new_file_name)
            picture = QPixmap(pic_path)
            self.ui.label_13.setPixmap(picture)
            self.ui.label_13.setScaledContents(True)
            image_uploaded_flag = True

    def personal_update(self):
        global citizenship_ID
        global old_imagepath
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(
            "This {} record is already existing in DB.\nto Update this record Continue please Press OK button".format(
                citizenship_ID))
        msgBox.setWindowTitle("Warning - All data will be updated")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:

            citizenship_ID = int(self.ui.lineEdit_12.text())
            name = self.ui.lineEdit_3.text()
            surname = self.ui.lineEdit_4.text()
            email = self.ui.lineEdit_5.text()
            telephone = self.ui.lineEdit_6.text()
            birthdate = self.ui.lineEdit_7.text()
            startdate = self.ui.lineEdit_8.text()
            city = self.ui.lineEdit_10.text()
            state = self.ui.lineEdit_9.text()
            adress = self.ui.textEdit.toPlainText()
            social = self.ui.lineEdit_11.text()
            department = self.ui.comboBox_3.currentText()
            status = self.ui.comboBox_2.currentText()
            hes_code = self.ui.lineEdit_hescode.text()
            new_file_name = str(citizenship_ID) + "_" + name + " " + surname + ".jpg"

            if image_uploaded_flag == True:
                pic_path = old_imagepath
                shutil.copyfile(old_imagepath, IMAGE_DIR + new_file_name)
                picture = QPixmap(pic_path)
                self.ui.label_13.setPixmap(picture)
                self.ui.label_13.setScaledContents(True)

                image_uploaded_flag == False

            profil_image = IMAGE_DIR + new_file_name
            face_status = "0"

            sql = """ UPDATE personal SET citizen_ID=?,name=?,surname=?,email=?,telephone=?,birthdate=?,startdate=?,
            city=?,state=?,adress=?,social=?,
            departmant_id=?,status=?,face_status=?,profil_image=? ,hes_code=? WHERE citizen_ID={}""".format(
                citizenship_ID)
            conn = create_connection(DATABASE_DIR)
            cur = conn.cursor()
            cur.execute(sql,
                        (citizenship_ID, name, surname, email, telephone, birthdate, startdate, city, state, adress,
                         social, department, status, face_status, profil_image, hes_code))
            conn.commit()
            conn.close()
            print("The Data has been updated succesfully .")
            self.statusBar().showMessage('The Data has been updated succesfully')
            self.personal_showlist_on_tabwidget()

    def personal_delete(self):
        global citizenship_ID
        global ID

        citizenship_ID = self.ui.lineEdit_12.text()
        name = self.ui.lineEdit_3.text()
        surname = self.ui.lineEdit_4.text()

        if self.ui.lineEdit_12.text() != '':

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(
                " All data of record {} ( Name : {} {} ) will be deleted \nTo continue please press DISCARD button".format(
                    citizenship_ID, name, surname))
            msgBox.setWindowTitle("Warning - The record will be deleted")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            returnValue = msgBox.exec()

            if returnValue == QMessageBox.Discard:
                sql = "DELETE FROM personal WHERE citizen_ID={}".format(citizenship_ID)

                conn = create_connection(DATABASE_DIR)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                conn.close()

                self.statusBar().showMessage(
                    " All data of record {} ( Name : {} {} ) has been deleted".format(
                        citizenship_ID, name, surname))

                self.ui.lineEdit_12.setText('')
                self.ui.lineEdit_2.setText('')
                ID = 0
                citizenship_ID = 0
                self.ui.tableWidget.clearContents()
                self.personal_screen_clear()
                self.personal_showlist_on_tabwidget()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("to delete please selecet a record from the table")
            msgBox2.setWindowTitle("Warning - No record has been selected")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" Warning - No record has been selected")

    def personal_screen_clear(self):
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit_12.setText("")
        name = self.ui.lineEdit_3.setText("")
        surname = self.ui.lineEdit_4.setText("")
        email = self.ui.lineEdit_5.setText("")
        telephone = self.ui.lineEdit_6.setText("")
        birthdate = self.ui.lineEdit_7.setText("")
        startdate = self.ui.lineEdit_8.setText("")
        city = self.ui.lineEdit_10.setText("")
        state = self.ui.lineEdit_9.setText("")
        adress = self.ui.textEdit.setPlainText("")
        linkdin = self.ui.lineEdit_11.setText("")
        department = self.ui.comboBox_3.setCurrentIndex(0)
        status = self.ui.comboBox_2.setCurrentIndex(0)
        hes_code = self.ui.lineEdit_hescode.setText("")
        profil_image = self.ui.label_13.setPixmap(QPixmap(None))

        face_status = "0"

    def personal_detial_upload_from_tablewidget(self):
        global citizenship_ID
        global ID
        citizenship_ID = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 1).text())
        conn = create_connection(DATABASE_DIR)

        sql = """ SELECT * FROM personal WHERE citizen_ID={}""".format(citizenship_ID)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        ID = self.ui.lineEdit_12.setText(str(data[0]))
        self.ui.lineEdit_12.setText(str(data[1]))
        name = self.ui.lineEdit_3.setText(data[2])
        surname = self.ui.lineEdit_4.setText(data[3])
        email = self.ui.lineEdit_5.setText(data[4])
        telephone = self.ui.lineEdit_6.setText(str(data[5]))
        birthdate = self.ui.lineEdit_7.setText(str(data[6]))
        startdate = self.ui.lineEdit_8.setText(str(data[7]))
        city = self.ui.lineEdit_10.setText(data[8])
        state = self.ui.lineEdit_9.setText(data[9])
        adress = self.ui.textEdit.setPlainText(data[10])
        linkdin = self.ui.lineEdit_11.setText(data[11])
        department = self.ui.comboBox_3.setCurrentText(data[12])
        status = self.ui.comboBox_2.setCurrentText(data[13])
        hes_code = self.ui.lineEdit_hescode.setText(data[16])
        face_status = "0"
        profil_image = data[15]
        self.ui.label_13.setPixmap(QPixmap(None))
        if (not profil_image == "" or profil_image == None):
            pic_path = profil_image
            picture = QPixmap(pic_path)
            self.ui.label_13.setPixmap(picture)
            self.ui.label_13.setScaledContents(True)
        else:
            self.ui.label_13.setPixmap(QPixmap(None))

        self.statusBar().showMessage('All fields are cleared to add new record')

    def personal_showlist_on_tabwidget(self):
        conn = create_connection(DATABASE_DIR)

        sql = """ SELECT * FROM personal order by ID DESC LIMIT 50 """
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        if data:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_pos)
            self.statusBar().showMessage('All records are fetched')
        else:
            self.statusBar().showMessage('Any record has not been found. Please change the search criteria ')
            self.ui.tableWidget.clearContents()

        return data

    def personal_tabwidget_query(self):
        filter_val = self.ui.lineEdit_13.text()
        index_val = str(self.ui.comboBox.currentIndex())
        header = {'1': 'name', '2': 'surname', '3': 'departmant_ID', '4': 'citizen_ID', '5': 'ID'}
        if filter_val and index_val != "0":
            sql = "SELECT * FROM personal WHERE {} LIKE '{}%'".format(
                header[index_val], filter_val)
        else:
            sql = "SELECT * FROM personal ORDER BY record_date DESC LIMIT 50"

        conn = create_connection(DATABASE_DIR)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        data = cur.fetchall()
        if data:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_pos)
            self.statusBar().showMessage('The requested record has been uploaded from DB')
        else:
            self.statusBar().showMessage('No record has been found according to this criteria')
            self.ui.tableWidget.clearContents()
        conn.close()

    # ============================ ===========================================
    # ================ ATTANDANCE FORM =========================================
    def attandance_showlist_on_tabwidget(self):
        filter_val = self.ui.lineEdit_14.text()
        index_val = str(self.ui.comboBox_4.currentIndex())
        header = {'1': 'personal.name', '2': 'personal.surname', '3': 'personal.departmant_id', '4': 'attandance.ID',
                  '5': 'personal.citizen_ID'}
        if int(index_val) > 0:
            sql = """ SELECT attandance.ID,personal.citizen_ID,personal.name,personal.surname,attandance.status,attandance.date,
        attandance.time,personal.status, personal.departmant_id 
        FROM attandance 
        INNER JOIN personal ON attandance.citizen_ID=personal.citizen_ID
        WHERE {} LIKE '{}%'""".format(header[index_val], filter_val)
        else:
            sql = """ SELECT attandance.ID,personal.citizen_ID,personal.name,personal.surname,attandance.status,attandance.date,
        attandance.time,personal.status, personal.departmant_id 
        FROM attandance 
        INNER JOIN personal ON attandance.citizen_ID=personal.citizen_ID
        ORDER BY attandance.record_date DESC """

        conn = create_connection(DATABASE_DIR)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        if data:
            self.ui.tableWidget_2.setRowCount(0)
            self.ui.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget_2.insertRow(row_pos)
            self.statusBar().showMessage('All records are fetched')
        else:
            self.statusBar().showMessage('Any record has not been found. Please change the search criteria ')
            self.ui.tableWidget_2.clearContents()

        return data

    def attandance_detial_upload_from_tablewidget(self):
        global citizenship_ID
        global ID
        global attandance_ID
        attandance_ID = int(self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(), 0).text())

        conn = create_connection(DATABASE_DIR)
        sql = """ SELECT attandance.ID,personal.citizen_ID,personal.name,personal.surname,attandance.status,attandance.date,
        attandance.time,personal.status, personal.departmant_id,personal.profil_image 
        FROM attandance 
        INNER JOIN personal ON attandance.citizen_ID=personal.citizen_ID
        WHERE attandance.ID LIKE '{}'""".format(attandance_ID)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        ID = self.ui.lineEdit_15.setText(str(data[0]))
        citizenship_ID = self.ui.lineEdit_25.setText(str(data[1]))
        name = self.ui.lineEdit_16.setText(data[2])
        surname = self.ui.lineEdit_17.setText(data[3])
        attandance_status = self.ui.lineEdit_21.setText(data[4])
        date_val = data[5].split("-")
        attandance_date = self.ui.dateEdit_3.setDate(QDate(int(date_val[0]), int(date_val[1]), int(date_val[2])))
        time_val = data[6].split(":")
        attandance_time = self.ui.timeEdit.setTime(QTime(int(time_val[0]), int(time_val[1]), int(time_val[2])))
        personal_status = self.ui.lineEdit_22.setText(str(data[7]))
        department = self.ui.lineEdit_23.setText(data[8])

        profil_image = data[9]
        self.ui.label_33.setPixmap(QPixmap(None))
        if (not profil_image == "" or profil_image == None):
            pic_path = profil_image
            picture = QPixmap(pic_path)
            self.ui.label_33.setPixmap(picture)
            self.ui.label_33.setScaledContents(True)
        else:
            self.ui.label_33.setPixmap(QPixmap(None))

        self.statusBar().showMessage('All fields are cleared to add new record')

    def attandence_update(self):
        ID = self.ui.lineEdit_15.text()
        if ID == "":
            print("No record as been selected .")
            self.statusBar().showMessage('No record as been selected')
            return False
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(
            "This {} record will be updated.\nContinue please Press OK button".format(
                ID))
        msgBox.setWindowTitle("Warning - All data will be updated")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            ID = int(self.ui.lineEdit_15.text())
            citizenship_ID = self.ui.lineEdit_25.text()
            attandance_status = self.ui.lineEdit_21.text()
            attandance_date = self.ui.dateEdit_3.date().toString("yyyy-MM-dd")
            attandance_time = self.ui.timeEdit.time().toString("hh:mm:ss")
            sql = """ UPDATE attandance SET citizen_ID=?,status=?,date=?,time=? 
            WHERE ID={}""".format(ID)
            conn = create_connection(DATABASE_DIR)
            cur = conn.cursor()
            cur.execute(sql, (citizenship_ID, attandance_status, attandance_date, attandance_time))
            conn.commit()
            conn.close()
            print("The record has been updated succesfully .")
            self.statusBar().showMessage('The record has been updated succesfully')
            # self.attandance_showlist_on_tabwidget()

    def attandence_delete(self):
        global ID
        ID = self.ui.lineEdit_15.text()
        name = self.ui.lineEdit_16.text()
        surname = self.ui.lineEdit_17.text()

        if ID != "":

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(
                " All data of record {} ( Name : {} {} ) will be deleted \nTo continue please press DISCARD button".format(
                    ID, name, surname))
            msgBox.setWindowTitle("Warning - The record will be deleted")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            returnValue = msgBox.exec()

            if returnValue == QMessageBox.Discard:
                sql = "DELETE FROM attandance WHERE ID={}".format(ID)

                conn = create_connection(DATABASE_DIR)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                conn.close()

                self.statusBar().showMessage(
                    " All data of record {} ( Name : {} {} ) has been deleted".format(
                        ID, name, surname))

                self.ui.lineEdit_15.setText('')
                self.ui.lineEdit_16.setText('')
                self.ui.lineEdit_17.setText('')
                self.ui.lineEdit_25.setText('')
                self.ui.lineEdit_21.setText('')
                self.ui.lineEdit_22.setText('')
                self.ui.lineEdit_23.setText('')
                self.ui.label_33.setPixmap(QPixmap(None))
                ID = 0

                self.ui.tableWidget_2.clearContents()

                self.attandance_showlist_on_tabwidget()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("to delete please select a record from the table")
            msgBox2.setWindowTitle("Warning - No record has been selected")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" Warning - No record has been selected")

    def attandence_export_today(self):

        current_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.attandence_export_job(current_date)

    def attandence_export_entered_date(self):
        current_date = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
        self.attandence_export_job(current_date)

    def attandence_export_job(self, current_date):
        current_date
        sql = """ SELECT attandance.ID,personal.citizen_ID,personal.name,personal.surname,attandance.status,attandance.date,
                        attandance.time,personal.status, personal.departmant_id,personal.profil_image 
                        FROM attandance 
                        INNER JOIN personal ON attandance.citizen_ID=personal.citizen_ID
                        WHERE attandance.date='{}'""".format(current_date)

        conn = create_connection(DATABASE_DIR)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        if len(data) == 0:
            return False
        wb = Workbook(REPORT_DIR + '\\report_attandence_{}.xlsx'.format(current_date))
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Report Name :')
        sheet1.write(0, 1, "report_attandence_{}.xlsx".format(current_date))

        sheet1.write(1, 0, 'User Name :')
        sheet1.write(1, 1, self.ui.lineEdit.text())
        # sheet1.write(2, 0, 'text :')
        # sheet1.write(2, 1, adress)

        sheet1.write(3, 0, 'ID')
        sheet1.write(3, 1, 'Citizen ID')
        sheet1.write(3, 2, 'Name')
        sheet1.write(3, 3, 'Surname')
        sheet1.write(3, 4, 'Status')
        sheet1.write(3, 5, 'Date')
        sheet1.write(3, 6, 'Time')
        sheet1.write(3, 7, 'Personal Status')
        sheet1.write(3, 8, 'Departmant')
        sheet1.write(3, 9, 'Profile Image')
        # sheet1.write(6, 10, 'Universite Bölümü')
        # sheet1.write(0, 11, 'Profil Resmi')
        # sheet1.write(0, 12, 'CV Adı')
        # sheet1.write(0, 13, 'FB Link')
        # sheet1.write(0, 14, 'Linkdn Link')
        # sheet1.write(0, 15, 'Blog Link')
        # sheet1.write(0, 16, 'Other Link')
        # sheet1.write(0, 17, 'Kayıt Zamanı')

        row_number = 4
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_number, column_num, str(item))
                column_num += 1
            row_number += 1

        wb.close()
        info = QMessageBox.information(self, 'Export Done',
                                       'Excel file has been created succesfully.\nYou can check the file location :  \n{} '.format(
                                           REPORT_DIR),
                                       QMessageBox.Ok)

        self.statusBar().showMessage('Export Done ')

    def attandence_send_email(self):
        self.statusBar().showMessage(" This feature will be added later ")

    def attandence_delete_entered_record(self):

        current_date = self.ui.dateEdit.date().toString("yyyy-MM-dd")

        if current_date != "":

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(
                " All records on this date ({}) will be deleted \nTo continue please press DISCARD button".format(
                    current_date))
            msgBox.setWindowTitle("Warning - The records will be deleted")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            returnValue = msgBox.exec()

            if returnValue == QMessageBox.Discard:
                sql = "DELETE FROM attandance WHERE date='{}'".format(current_date)

                conn = create_connection(DATABASE_DIR)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                conn.close()

                self.statusBar().showMessage(
                    " All records on this date ({}) will be deleted".format(current_date))

                self.ui.tableWidget_2.clearContents()

                self.attandance_showlist_on_tabwidget()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("to delete please select a record from the table")
            msgBox2.setWindowTitle("Warning - No record has been selected")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" Warning - No record has been selected")

    # ============================ ===========================================
    # ================ ADD SAMPLE PHOTOS =========================================
    def faceRecognitionFromPicture(self):
        self.videoDialog.show()

    def trainFaces(self):
        val_cnt = 0
        self.ui.listWidget.clear()
        print("---- Training Started ----")
        for root, dirs, files in os.walk("./faces"):
            self.ui.progressBar.setMaximum(len(files))
            for filename in files:
                file_result = filename.split(".")
                known_face_names.append(file_result[0])
                image = face_recognition.load_image_file("faces/" + filename)
                try:
                    image_face_encoding = face_recognition.face_encodings(image)[0]
                    known_face_encodings.append(image_face_encoding)
                    print("ID: " + file_result[0])
                    self.ui.label_18.setText("ID: " + file_result[0])
                    self.ui.listWidget.addItem(file_result[0])
                    val_cnt += 1

                    self.ui.progressBar.setValue(val_cnt)
                except:
                    print("Name: " + file_result[0] + " is not encoded by the System please change or remove photo")
                    self.ui.label_18.setText(
                        "ID: " + file_result[0] + " is not encoded by the System please change or remove photo")
                    continue

        print("---- Training Completed ----")

        with open("test_images.txt", 'wb') as f:
            pickle.dump(known_face_encodings, f)
        with open("test_names.txt", 'wb') as f:
            pickle.dump(known_face_names, f)

    def read_qr_code(self):
        if self.ui.lineEdit_hescode_2.text() != "--":
            print(self.ui.lineEdit_hescode_2.text())
            return False
        global kamera
        if kamera == "picamera":
            cap1 = cv2.VideoCapture("http://192.168.0.103:8000/stream.mjpg")
        else:
            cap1 = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN

        while True:
            _, frame = cap1.read()
            if pyzbar.decode(frame):
                decodedObjects = pyzbar.decode(frame)
                for obj in decodedObjects:
                    # print("Data", obj.data)
                    cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                                (255, 0, 0), 3)
                print(str(obj.data)[-11:-1])
                self.ui.lineEdit_hescode_2.setText(str(obj.data)[-11:-1])
                break
            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break
            # if str(decodedObjects)!="":
            #    break
        # return  str(obj.data)

        cap1.release()
        cv2.destroyAllWindows()

    # ============================ error list ===========================================
    def error_message_missingField(self, error_text):
        warning = QMessageBox.warning(self, 'Missing Data Error ',
                                      '{} is missing. Please fill all missing fields'.format(error_text),
                                      QMessageBox.Ok)
        self.statusBar().showMessage('Missing Data Error')

    def turn_login_page(self):
        self.window2 = LoginWindow()
        self.close()
        self.window2.show()
        self.window2.ui.lineEdit.setText("")


class LoginWindow(QDialog, login.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(LoginWindow, self).__init__(parent, *args, **kwargs)
        self.ui = login.Ui_Dialog()
        self.loginDialog = parent
        self.ui.setupUi(self)
        self.setWindowTitle('Login Window')
        self.handle_button()

    def handle_button(self):
        self.ui.pushButton.clicked.connect(self.user_check)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton_4.clicked.connect(self.user_add)

    def user_check(self):
        global username
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        conn = create_connection(DATABASE_DIR)

        sql = """ SELECT * FROM users WHERE username='{}'""".format(username)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        conn.close()
        data_count = len(data)
        row_count = 0
        for row in data:

            if username == row[1] and password == row[2]:
                self.window2 = MainWindow()
                self.close()
                self.window2.show()
                self.window2.ui.lineEdit.setText(username)
                break
            row_count += 1
        if data_count <= row_count:
            warning = QMessageBox.warning(self, 'Login Error', 'Please check your data', QMessageBox.Ok)
            self.ui.label_4.setText('Your user account is not valid .Please check your data.')

    def user_add(self):
        global username
        username = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()
        password2 = self.ui.lineEdit_5.text()
        if password != password2 and password != "":
            warning = QMessageBox.warning(self, 'Password Error', 'Please check passwords', QMessageBox.Ok)

            return False

        conn = create_connection(DATABASE_DIR)
        try:
            sql = """INSERT INTO users (username,password) VALUES(?,?)"""
            conn = create_connection(DATABASE_DIR)
            cur = conn.cursor()
            cur.execute(sql, (username, password))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'the user has been created ', 'You can Log in Now on the Login Page',
                                    QMessageBox.Ok)

        except:
            QMessageBox.warning(self, "This user is already used", 'Please use another user ',
                                QMessageBox.Ok)


def show_mainPage():
    createdb()

    app = QApplication(sys.argv)
    translator1 = QTranslator()
    translator2 = QTranslator()
    translator3 = QTranslator()
    # =======================================
    if LANGUAGE == "turkish":

        translator1.load(LANGUAGES_DIR + 'login_tr.qm')
        app.installTranslator(translator1)
        translator2.load(LANGUAGES_DIR + 'video_tr.qm')
        app.installTranslator(translator2)
        translator3.load(LANGUAGES_DIR + 'main_tr.qm')
        app.installTranslator(translator3)

    else:
        pass
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Existing")


if __name__ == "__main__":
    show_mainPage()
