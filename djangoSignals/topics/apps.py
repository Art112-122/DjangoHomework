from django.apps import AppConfig


class TopicsConfig(AppConfig):
    name = "topics"

    def ready(self):
        from . import signals

        signals.topic_changed.connect(signals.handle_topic_changed)
