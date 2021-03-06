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
import signal
import time

try:
  from PyQt4.QtCore import *
  from PyQt4.QtGui import *
  from PyQt4.QtWebKit import *

except ImportError:
  print("Oh noes! you need to install some modules!")
  print("maybe try? 'sudo apt-get install python-qt4 libqt4-webkit'")
  sys.exit(1)


class WitBrowser(QWebPage):
  def __init__(self, width = None, height = None):
    QWebPage.__init__(self)
    size = QSize(width if width else 1600, height if height else 10000);
    self.setViewportSize(size)


class MobileBrowser(WitBrowser):
  def userAgentForUrl(self, url):
    return "Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19";


class DesktopBrowser(WitBrowser):
  def userAgentForUrl(self, url):
    return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4";


class Webshot(QWidget):
  sleep = 0.0
  def __init__(self, url=None, out=None, width=1024, height=None, browser=None, sleep=0.5):
    QWidget.__init__(self)

    if browser is None:
      browser = 'desktop'

    self.browser = browser
    self.sleep = sleep

    if not url:
      quit()
    self.url = url

    if not out:
      out = "web2png.%i.png" % int(time.time())

    self.out = out
    self.view = None
    self.page = None
    self.width = width
    self.height = height

  def shot(self):
    self.view = QWebView()
    self.view.showMaximized()

    if self.browser is not None:
      if self.browser == 'desktop':
        browser = DesktopBrowser(self.width, self.height)
      else:
        browser = MobileBrowser(self.width, self.height)

      self.view.setPage(browser)

    self.view.load(QUrl(self.url))
    self.view.show()

    self.page = self.view.page()
    self.connect(self.view.page(), SIGNAL("loadFinished(bool)"), self.render)

  def render(self):
    frame = self.view.page().currentFrame()

    frame.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
    frame.setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)

    size = frame.contentsSize()

    if self.width is not None:
      size.setWidth(self.width)
    else:
      size.setWidth(size.width())

    if self.height is not None:
      size.setHeight(self.height)
    else:
      size.setHeight(size.height())

    self.view.page().setViewportSize(size)
    time.sleep(float(self.sleep))

    img = QImage(size, QImage.Format_ARGB32)
    paint = QPainter(img)
    frame.render(paint, QWebFrame.ContentsLayer)
    paint.end()
    img.save(self.out)

    sys.exit(0)


def grab(src, dst, width=None, height=None, browser='desktop', sleep=0.5):
  """ Wrapper around the class to easily GRAB an image
  when given a web page """
  app = QApplication(sys.argv)
  signal.signal(signal.SIGINT, signal.SIG_DFL)

  t = Webshot(src, dst, width, height, browser, sleep)
  t.shot()
  return app.exec_()

