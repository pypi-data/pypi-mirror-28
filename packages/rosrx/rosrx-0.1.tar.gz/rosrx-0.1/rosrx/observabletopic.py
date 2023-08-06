import rospy
from rx import Observable


def observabletopic(topic, topic_type, queue_size=None):
    """Subscribe to a ROS topic as a Observable stream of message"""

    def subscribe(observer):

        def cb(message):
            observer.on_next(message)

        topic_subscriber = rospy.Subscriber(
            topic, topic_type, cb, queue_size=queue_size)

        def dispose():
            topic_subscriber.unregister()

        return dispose

    return Observable.create(subscribe)
