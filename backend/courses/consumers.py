import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Course

class CourseEnrollmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.course_group_name = f'course_{self.course_id}'

        await self.channel_layer.group_add(
            self.course_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.course_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.course_group_name,
            {
                'type': 'course_message',
                'message': message
            }
        )

    async def course_message(self, event):
        message = event['message']
        course = await self.get_course_data()

        await self.send(text_data=json.dumps({
            'message': message,
            'course': course
        }))

    @database_sync_to_async
    def get_course_data(self):
        course = Course.objects.get(pk=self.course_id)
        return {
            'id': str(course.id),
            'title': course.title,
            'enrolled_count': course.enrolled_count,
            'capacity': course.capacity,
            'is_available': course.is_available
        }