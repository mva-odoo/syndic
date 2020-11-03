from random import randint
import random
import locale
import logging
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
import cv2
import numpy as np


_logger = logging.getLogger(__name__)

_MONTH = [
    ('1', 'Janvier'),
    ('2', 'Fevrier'),
    ('3', 'Mars'),
    ('4', 'Avril'),
    ('5', 'Mai'),
    ('6', 'Juin'),
    ('7', 'Juillet'),
    ('8', 'Aout'),
    ('9', 'Septembre'),
    ('10', 'Octobre'),
    ('11', 'Novembre'),
    ('12', 'Decembre')
]


class SyndicTools:
    def pass_generator(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw += alphabet[next_index]
        return mypw

    def login_generator(self, name):
        login = name.replace(' ', '')
        login = login.replace('-', '')
        rand = str(randint(0, 99))
        return login[:8]+rand

    def french_date(self, tr_date):
        try:
            locale.setlocale(locale.LC_ALL, 'fr_BE.utf8')
        except locale.Error:
            _logger.error('Local not settable')

        return tr_date.strftime('%A %d %B %Y')

    def merge_pdf(self, pdf_data):
        ''' Merge a collection of PDF documents in one
        :param list pdf_data: a list of PDF datastrings
        :return: a unique merged PDF datastring
        '''
        writer = PdfFileWriter()
        for document in pdf_data:
            reader = PdfFileReader(io.BytesIO(document), strict=False)
            for page in range(0, reader.getNumPages()):
                writer.addPage(reader.getPage(page))
        _buffer = io.BytesIO()
        writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()
        return merged_pdf

    def create_watermark(self, input_pdf, watermark):
        watermark_obj = PdfFileReader(io.BytesIO(watermark))
        watermark_page = watermark_obj.getPage(0)

        pdf_reader = PdfFileReader(io.BytesIO(input_pdf))
        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        _buffer = io.BytesIO()
        pdf_writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()
        return merged_pdf


class SyndicImage:
    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def remove_noise(self, image):
        return cv2.medianBlur(image, 5)

    def thresholding(self, image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def dilate(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    def erode(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    def opening(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def match_template(self, image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)