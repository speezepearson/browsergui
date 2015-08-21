import threading
import json

class Destroyed(Exception):
  '''Raised when trying to operate on a destroyed DocumentChangeTracker.'''
  pass

def ancestors(tag):
  while tag is not None:
    yield tag
    tag = tag.parentNode

def innerHTML(tag):
  return ''.join(child.toxml() for child in tag.childNodes)

def javascript_to_update_tag(tag, variable_name):
  lines = []

  # In Chrome, doing `tag.setAttribute("value", ...)` usually updates the value displayed to the user,
  # but for color-type inputs, the displayed value does not update. So we need this following clause.
  # Furthermore, doing `tag.value = x` has no effect if `tag.getAttribute("value") == x`,
  # so this clause must come before the attribute-setting.
  # Crazy, I know.
  if tag.tagName == 'input':
    lines.append('{var}.value = {value}'.format(var=variable_name, value=json.dumps(tag.getAttribute('value'))))

  # Update tag attributes
  lines.extend(
    '{var}.setAttribute({key}, {value})'.format(var=variable_name, key=json.dumps(attr), value=json.dumps(value))
    for attr, value in tag.attributes.items())

  # Update tag children
  lines.append('{var}.innerHTML = {innerHTML}'.format(var=variable_name, innerHTML=json.dumps(innerHTML(tag))))
  return ';\n'.join(lines)

class DocumentChangeTracker(object):
  '''Provides JavaScript to help a browser keep its document up to date with a local one.

  Intended use case: there's a locally stored XML document, and there's another document
  stored in a browser window. The browser wants to execute some JavaScript to make its
  document look like the one on the server, so it makes a request to the server.
  The server should wait until a change is made to the local document (if necessary),
  then respond with the appropriate JS to apply the change to the remote document.

  How it works: the DocumentChangeTracker is instantiated, being given an XML document.
  It keeps track of whether the document is "clean" or "dirty" (i.e. whether there have been
  changes since the last time the browser was brought up to date).

  The :func:`flush_changes` method waits until the document is dirty (if necessary),
  marks the document as clean, and returns a JavaScript string that will bring the browser's
  DOM up to date.

  The :func:`mark_dirty` method marks the document as dirty, possibly waking up threads
  waiting on :func:`flush_changes`.

  The :func:`destroy` method wakes up all waiting threads, but causes them to return
  JavaScript that will close the browser window.
  '''
  def __init__(self, document, **kwargs):
    self.document = document
    super(DocumentChangeTracker, self).__init__(**kwargs)

    self._mutex = threading.RLock()
    self._changed_condition = threading.Condition(self._mutex)
    self._dirty_tags = set([document.documentElement])
    self._destroyed = False

  def destroy(self):
    '''Wake up waiting threads and give them JS to close the browser window.'''
    with self._mutex:
      self._destroyed = True
      self._changed_condition.notify_all()

  def flush_changes(self):
    '''Wait until the document is dirty, then return JS to bring a browser up to date.

    :returns: str
    '''
    with self._changed_condition:
      while not (self._dirty_tags or self._destroyed):
        self._changed_condition.wait()
      if self._destroyed:
        return 'window.close(); sleep(9999)'
      
      result = ';\n'.join(
        'temp = document.getElementById({id}); {update}'.format(
          id=json.dumps(tag.getAttribute('id')),
          update=javascript_to_update_tag(tag, variable_name='temp'))
        for tag in self._dirty_tags)
      self._dirty_tags = set()
      return result

  def mark_dirty(self, tag):
    '''Mark the given tag as dirty, waking up calls to :func:`flush_changes`'''
    with self._changed_condition:
      if self._destroyed:
        raise Destroyed(self)
      # If one of the tag's parents is dirty, we'll rewrite the tag anyway,
      # so we don't need to add it to the list.
      for old_dirty_tag in self._dirty_tags:
        if old_dirty_tag in ancestors(tag):
          return
      # The new tag will eclipse the dirtiness of any of its descendants.
      for old_dirty_tag in self._dirty_tags:
        if tag in ancestors(old_dirty_tag):
          self._dirty_tags.remove(old_dirty_tag)

      self._dirty_tags.add(tag)
      self._changed_condition.notify_all()
