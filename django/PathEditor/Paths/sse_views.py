
import json
import time
import threading
import queue
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User # Import User model for creator_username/user_username
from .models import Path, GameBoard

from django.http import StreamingHttpResponse

KEEP_ALIVE_INTERVAL = 10

class Broadcaster:
    def __init__(self):
        self.client_queues = []
        self._lock = threading.Lock()

    def subscribe(self):
        q = queue.Queue(maxsize=10)
        with self._lock:
            self.client_queues.append(q)
            print(f"Client number: {len(self.client_queues)} subscribed.")
        return q

    def publish(self, event_type, data):
        event_data = {
            "event_type": event_type,
            "data": data,
        }
        
        with self._lock:
            active_queues = list(self.client_queues)
        
        print(f"Broadcasting event '{event_type}' to {len(active_queues)} clients.")
        for q in active_queues:
            try:
                q.put(event_data, block=False)
            except queue.Full:
                print(f"Warning: A client queue was full. Event '{event_type}' was dropped for this client.")
                pass

    def unsubscribe(self, q):
        with self._lock:
            if q in self.client_queues:
                self.client_queues.remove(q)
                print(f"Client unsubscribed. Remaining clients: {len(self.client_queues)}")

broadcaster = Broadcaster()

def event_stream():
    keep_alive_count = 0
    client_queue = broadcaster.subscribe()
    try: 
        while True:
            try: 
                print(f"entering get, queue size: {client_queue.qsize()}")
                event = client_queue.get(timeout=KEEP_ALIVE_INTERVAL)
                print("exited get")
                event_type = event["event_type"]
                data_payload = json.dumps(event["data"])
                print("ready to yield")
                yield f"event: {event_type}\n"
                yield f"data: {data_payload}\n\n"
            except queue.Empty:
                print("keeping alive")
                keep_alive_count += 1
                yield f": keep-alive: {keep_alive_count}\n\n"
    finally:
        broadcaster.unsubscribe(client_queue)

@receiver(post_save, sender=GameBoard)
def board_post_save(sender, instance, created, **kwargs):
    if created:
        event_data = {
            "board_id": instance.id,
            "board_name": instance.name,
        }
        broadcaster.publish("newBoard", event_data)
        print(f"Signal: New Board created - {instance.name}")


@receiver(post_save, sender=Path)
def path_post_save(sender, instance, created, **kwargs):
    if created:
        bg_title = instance.background.title if instance.background else 'None'
        event_data = {
            "path_id": instance.id,
            "background_name": bg_title,
            "creator_username": instance.user.username,
        }
        broadcaster.publish("newPath", event_data)
        print(f"Signal: New Path saved - {bg_title}")


def sse_notifications(request):
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
