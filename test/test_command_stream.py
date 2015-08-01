import unittest
from browsergui.commands.command_stream import CommandStream, Broadcaster, UnrelatedStreamError

class BroadcasterTest(unittest.TestCase):
  def test_initially_no_streams(self):
    self.assertEqual(0, len(Broadcaster().streams))

  def test_create_stream(self):
    broadcaster = Broadcaster()
    stream = broadcaster.create_stream()
    self.assertIn(stream, broadcaster.streams)

  def test_destroy_stream(self):
    broadcaster = Broadcaster()
    stream_a = broadcaster.create_stream()
    stream_b = broadcaster.create_stream()
    broadcaster.destroy_stream(stream_a)

    self.assertNotIn(stream_a, broadcaster.streams)
    self.assertIn(stream_b, broadcaster.streams)
    self.assertTrue(stream_a.destroyed)
    self.assertFalse(stream_b.destroyed)

  def test_destroy_stream__error_with_unrelated_stream(self):
    broadcaster = Broadcaster()
    unrelated_stream = CommandStream()

    with self.assertRaises(UnrelatedStreamError):
      broadcaster.destroy_stream(unrelated_stream)

    related_stream = broadcaster.create_stream()
    with self.assertRaises(UnrelatedStreamError):
      broadcaster.destroy_stream(unrelated_stream)

    self.assertFalse(related_stream.destroyed)
    self.assertFalse(unrelated_stream.destroyed)

  def test_destroy_stream__error_when_called_twice(self):
    broadcaster = Broadcaster()
    stream = broadcaster.create_stream()
    broadcaster.destroy_stream(stream)

    with self.assertRaises(UnrelatedStreamError):
      broadcaster.destroy_stream(stream)

  def test_destroy(self):
    broadcaster = Broadcaster()
    stream = broadcaster.create_stream()
    broadcaster.destroy()

    self.assertEqual(0, len(broadcaster.streams))
    self.assertTrue(stream.destroyed)

  def test_broadcast(self):
    broadcaster = Broadcaster()
    stream_a = broadcaster.create_stream()
    stream_b = broadcaster.create_stream()
    broadcaster.broadcast('command')

    self.assertEqual('command', stream_a.get(block=False))
    self.assertTrue(stream_a.empty())
    self.assertEqual('command', stream_b.get(block=False))
    self.assertTrue(stream_b.empty())
