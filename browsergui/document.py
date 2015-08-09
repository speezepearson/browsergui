import xml.dom.minidom
import threading
import json

class Destroyed(Exception):
  pass

class Document(object):
  def __init__(self, title_tag, body_tag, **kwargs):
    super(Document, self).__init__(**kwargs)
    self._local_document = xml.dom.minidom.Document()

    self._title_tag = title_tag
    self._body_tag = body_tag

    self._html_tag = self._local_document.createElement('html')
    self._head_tag = self._local_document.createElement('head')

    self._local_document.appendChild(self._html_tag)
    self._html_tag.appendChild(self._head_tag)
    self._head_tag.appendChild(self._title_tag)
    self._html_tag.appendChild(self._body_tag)

    self._mutex = threading.RLock()
    self._changed_condition = threading.Condition(self._mutex)
    self._dirty = True
    self._destroyed = False

  def destroy(self):
    with self._mutex:
      self._destroyed = True
      self._changed_condition.notify_all()

  def flush_changes(self):
    with self._changed_condition:
      self._changed_condition.wait_for(lambda: self._dirty or self._destroyed)
      if self._destroyed:
        raise Destroyed(self)
      self._dirty = False
      html_contents = self._head_tag.toxml() + self._body_tag.toxml()
      return 'document.documentElement.innerHTML = {xml}'.format(xml=json.dumps(html_contents))

  def mark_dirty(self):
    with self._changed_condition:
      self._dirty = True
      self._changed_condition.notify()
