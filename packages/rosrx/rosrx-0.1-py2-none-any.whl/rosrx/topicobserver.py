import rospy
from rx import Observer


class TopicObserver(Observer):
    """Publish an observable stream to a topic"""

    def __init__(self, topic, topic_type, latch=False, queue_size=None):
        self._pub = rospy.Publisher(
            topic, topic_type, latch=latch, queue_size=queue_size)
        self.is_stopped = False

    def on_next(self, value):
        if not self.is_stopped:
            self._pub.publish(value)

    def on_error(self, error):
        pass

    def on_completed(self):
        self.is_stopped = True
        self._pub.unregister()
