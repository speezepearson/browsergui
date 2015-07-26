import sys
import tempfile
import base64
from browsergui import Image
from . import BrowserGUITestCase

class ImageTest(BrowserGUITestCase):
  def set_file(self, contents, extension):
    if self.file is not None:
      self.file.close()

    self.file_format = extension
    self.file_contents = contents
    self.file = tempfile.NamedTemporaryFile(suffix=('' if extension is None else '.'+extension))
    self.file.write(contents)
    self.file.flush()

  def setUp(self):
    self.file = None
    self.set_file(contents=b'initial contents', extension='png')

  def tearDown(self):
    self.file.close()

  def test_construction_from_filename(self):
    image = Image(self.file.name)
    self.assertEqual(self.file.name, image.filename)
    self.assertEqual(self.file_format, image.format)
    self.assertEqual(self.file_contents, image.data)

  def test_reload_data(self):
    image = Image(self.file.name)
    old_contents = self.file_contents
    self.assertEqual(old_contents, image.data)
    
    new_contents = b'new contents'
    self.file.seek(0, 0)
    self.file.write(new_contents)
    self.file.truncate()
    self.file.flush()

    self.assertEqual(old_contents, image.data)
    image.reload_data()
    self.assertEqual(new_contents, image.data)

  def test_construction_from_filename__file_not_found(self):
    expected_error_type = FileNotFoundError if sys.version_info > (3, 3) else IOError
    with self.assertRaises(expected_error_type):
      Image('/nonexistent.png')

  def test_construction_from_filename__filename_has_no_format(self):
    self.set_file(contents=b'whatever', extension=None)
    with self.assertRaises(ValueError):
      Image(self.file.name)

  def test_data_not_settable(self):
    with self.assertRaises(AttributeError):
      Image(self.file.name).data = b'new contents'

  def test_tag(self):
    expected_html = '<img src="data:image/{};base64,{}"/>'.format(self.file_format, base64.b64encode(self.file_contents).decode('ascii'))
    self.assertHTMLLike(expected_html, Image(self.file.name))
