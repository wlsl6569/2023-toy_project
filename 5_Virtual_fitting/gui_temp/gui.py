import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QListWidget, \
    QLabel, QBoxLayout, QWidget, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
from PySide6 import QtCore, QtGui
import cv2
import numpy as np

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TEAM5-Try On!")
        self.resize(800, 600)

        self.folder_button1 = QPushButton("cloth image folder")
        self.folder_button1.clicked.connect(self.open_folder_dialog1)
        self.folder_button1.setMaximumSize(150, 30)

        self.folder_button2 = QPushButton("model image folder")
        self.folder_button2.clicked.connect(self.open_folder_dialog2)
        self.folder_button2.setMaximumSize(150, 30)

        self.composite_button = QPushButton("blend")
        self.composite_button.clicked.connect(self.composite_images)
        self.composite_button.setEnabled(False)

        self.image_list_widget1 = QListWidget()
        self.image_list_widget1.currentRowChanged.connect(self.display_image1)
        self.image_list_widget1.setMaximumSize(150, 400)

        self.image_list_widget2 = QListWidget()
        self.image_list_widget2.currentRowChanged.connect(self.display_image2)
        self.image_list_widget2.setMaximumSize(150, 400)

        self.image_label1 = QLabel()
        self.image_label1.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label1.setMinimumSize(200, 400)

        self.image_label2 = QLabel()
        self.image_label2.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label2.setMinimumSize(200, 400)

        self.composite_scene = QGraphicsScene()
        self.composite_view = QGraphicsView(self.composite_scene)
        self.composite_view.setMinimumSize(400, 400)

        empty_image = QtGui.QImage(150, 350, QtGui.QImage.Format_RGB888)
        empty_image.fill(QtGui.QColor(255, 255, 255))
        painter = QtGui.QPainter(empty_image)
        font = QtGui.QFont()
        font.setPixelSize(20)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(0, 0, 0))
        text = "Preview"
        text_rect = painter.boundingRect(empty_image.rect(), QtCore.Qt.AlignCenter, text)
        painter.drawText(text_rect, QtCore.Qt.AlignCenter, text)

        painter = QtGui.QPainter(empty_image)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(0, 0, empty_image.width() - 1, empty_image.height() - 1)
        painter.end()

        pixmap = QtGui.QPixmap.fromImage(empty_image)
        self.image_label1.setPixmap(pixmap)
        self.image_label2.setPixmap(pixmap)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.folder_button1)
        left_layout.addWidget(self.image_list_widget1)
        left_layout.addWidget(self.folder_button2)
        left_layout.addWidget(self.image_list_widget2)
        left_layout.addWidget(self.composite_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_label1)
        right_layout.addWidget(self.image_label2)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        main_layout.addWidget(self.composite_view)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.current_folder1 = ""
        self.current_images1 = []
        self.current_index1 = -1

        self.current_folder2 = ""
        self.current_images2 = []
        self.current_index2 = -1

        self.composite_pixmap = None

        self.image1_path = ""
        self.image2_path = ""

    def open_folder_dialog1(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        folder_dialog.directoryEntered.connect(self.set_folder_path1)
        folder_dialog.accepted.connect(self.load_images1)
        folder_dialog.exec_()

    def open_folder_dialog2(self):
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        folder_dialog.directoryEntered.connect(self.set_folder_path2)
        folder_dialog.accepted.connect(self.load_images2)
        folder_dialog.exec_()

    def set_folder_path1(self, folder_path):
        self.current_folder1 = folder_path

    def set_folder_path2(self, folder_path):
        self.current_folder2 = folder_path

    def load_images1(self):
        self.image_list_widget1.clear()

        if self.current_folder1:
            self.current_images1 = []
            self.current_index1 = -1

            image_extensions = (".jpg", ".png", ".jpeg", ".gif", ".bmp")

            for dir_path, _, file_names in os.walk(self.current_folder1):
                for file_name in file_names:
                    if file_name.lower().endswith(image_extensions):
                        file_path = os.path.join(dir_path, file_name)
                        self.current_images1.append(file_path)
                        self.image_list_widget1.addItem(file_name)

            if self.current_images1:
                self.image_list_widget1.setCurrentRow(0)

    def load_images2(self):
        self.image_list_widget2.clear()

        if self.current_folder2:
            self.current_images2 = []
            self.current_index2 = -1

            image_extensions = (".jpg", ".png", ".jpeg", ".gif", ".bmp")

            for dir_path, _, file_names in os.walk(self.current_folder2):
                for file_name in file_names:
                    if file_name.lower().endswith(image_extensions):
                        file_path = os.path.join(dir_path, file_name)
                        self.current_images2.append(file_path)
                        self.image_list_widget2.addItem(file_name)

            if self.current_images2:
                self.image_list_widget2.setCurrentRow(0)

    def display_image1(self, index):
        if 0 <= index < len(self.current_images1):
            self.current_index1 = index
            image_path1 = self.current_images1[self.current_index1]
            pixmap1 = QtGui.QPixmap(image_path1)
            scaled_pixmap1 = pixmap1.scaled(self.image_label1.size() * 0.9,
                                            QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label1.setPixmap(scaled_pixmap1)
            self.image1_path = image_path1
            self.enable_composite_button()

    def display_image2(self, index):
        if 0 <= index < len(self.current_images2):
            self.current_index2 = index
            image_path2 = self.current_images2[self.current_index2]
            pixmap2 = QtGui.QPixmap(image_path2)
            scaled_pixmap2 = pixmap2.scaled(self.image_label2.size() * 0.9,
                                            QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label2.setPixmap(scaled_pixmap2)
            self.image2_path = image_path2
            self.enable_composite_button()

    def enable_composite_button(self):
        if self.image1_path and self.image2_path:
            self.composite_button.setEnabled(True)
        else:
            self.composite_button.setEnabled(False)

    def composite_images(self):
        if self.image1_path and self.image2_path:
            # 이미지 1 로드
            image1 = cv2.imread(self.image1_path)

            # 이미지 2 로드
            image2 = cv2.imread(self.image2_path)

            # 이미지 1의 크기를 이미지 2와 동일하게 조정
            image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

            # 마스크 이미지의 경로 생성 (마스크 파일의 이름은 이미지1의 파일명과 동일한 것으로 가정)
            mask_path = os.path.join('./HR-VITON/datasets/zalando-hd-resized/test/cloth-mask',
                                     os.path.basename(self.image1_path))

            # 마스크 이미지가 존재하는지 확인
            if os.path.exists(mask_path):
                # 마스크 이미지 로드
                mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

                # 이미지 1의 배경을 제거하여 투명 배경으로 만듦
                image1[mask == 0] = 0



                # 이미지 1의 채널 수를 이미지 2와 일치하게 조정
                if image1.shape[2] != image2.shape[2]:
                    image1 = cv2.cvtColor(image1, cv2.COLOR_BGRA2BGR)

                # 이미지 1을 이미지 2 위에 합성 (배경이 투명한 부분만 합성됨)
                result = image2.copy()
                result[mask != 0] = image1[mask != 0]



                # Convert the result to a format that can be displayed in QGraphicsView
                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                height, width, channel = result_rgb.shape
                bytes_per_line = 3 * width
                q_image = QtGui.QImage(result_rgb.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
                self.composite_pixmap = QtGui.QPixmap.fromImage(q_image)

                # Display the composite result
                self.display_composite_result()  # Call this method to update the view

    def display_composite_result(self):
        if self.composite_pixmap:
            composite_scene = QGraphicsScene()
            composite_item = QGraphicsPixmapItem(self.composite_pixmap)
            composite_scene.addItem(composite_item)

            self.composite_view.setScene(composite_scene)
            self.composite_view.fitInView(composite_item, QtCore.Qt.KeepAspectRatio)
            self.composite_view.setAlignment(QtCore.Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    app.exec_()
