"""
thepearson
  Modified slightly from: https://gist.github.com/3140831


Takes snapshot of full webpages using Webkit and Qt4
usage:
python web2png.py URL [FILE]
example:
python web2png.py http://python.org out.png

see:
http://riverbankcomputing.com/static/Docs/PyQt4/html/qwebview.html#load
http://riverbankcomputing.com/static/Docs/PyQt4/html/qwebpage.html#loadFinished
http://riverbankcomputing.com/static/Docs/PyQt4/html/qwebframe.html#render
https://github.com/AdamN/python-webkit2png
http://www.blogs.uni-osnabrueck.de/rotapken/2008/12/03/create-screenshots-of-a-web-page-using-python-and-qtwebkit/
http://thechangelog.com/post/512693979/webkit2png-command-line-web-screenshots
"""
import sys
import time

try:
  from PyQt4.QtCore import *
  from PyQt4.QtGui import *
  from PyQt4.QtWebKit import *
except ImportError:
  print("Oh noes! you need to install some modules!")
  print("maybe try? 'sudo apt-get install python-qt4 libqt4-webkit'")
  sys.exit(1)

class Webshot(QObject):
  def __init__(self, url=None, out=None, width=1024, height=None):
    QObject.__init__(self)

    if not url:
      quit()
    self.url = url
    if not out:
      out = "web2png.%i.png"%int(time.time())

    self.out = out
    self.view = None
    self.page = None
    self.width = width
    self.height = height

  def shot(self):
    self.view = QWebView()
    self.view.load(QUrl(self.url))
    self.view.show()
    self.page = self.view.page()
    self.connect(self.page, SIGNAL("loadFinished(bool)"), self.render)

  def render(self):
    frame = self.page.currentFrame()
    size = frame.contentsSize()

    if self.width is not None:
      size.setWidth(self.width)
    else:
      size.setWidth(size.width())

    if self.height is not None:
      size.setHeight(self.height)
    else:
      size.setHeight(size.height())

    self.view.resize(size)
    self.page.setViewportSize(size)

    img = QImage(size, QImage.Format_ARGB32)
    paint = QPainter(img)

    frame.render(paint, QWebFrame.ContentsLayer)
    paint.end()
    img.save(self.out)
    QApplication.quit()


def grab(src, dst, width=None, height=None):
  """
  Wrapper around the class to easily GRAB an image
  when given a web page
  """
  app = QApplication([])
  t = Webshot(src, dst, width, height)
  t.shot()
  return app.exec_()

