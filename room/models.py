from django.db import models
from user.models import User
from quiz.models import Question
import random
import string
import redis
import json

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

class Room(models.Model):
    quiz_subject = models.CharField(max_length=255)
    invitation_code = models.CharField(max_length=5, unique=True, blank=True, null=True)
    questions = models.ManyToManyField(
        'quiz.Question',
        blank=True,
        related_name = 'rooms'
    )

    def __str__(self):
        return f"Room {self.id} - {self.quiz_subject}"

    def create_session_in_redis(self):
        session_key = f"room:{self.id}"
        initial_data = {
            "participants": json.dumps([]),
            "scores": json.dumps({}),
            "status": "waiting",
            "quiz_subject": self.quiz_subject,
            "invitation_code": self.invitation_code,
        }
        # initial_data['participants'] = str(initial_data['participants'])
        # initial_data['scores'] = str(initial_data['scores'])

        # print(session_key, initial_data)
        redis_client.hset(session_key, mapping=initial_data)

    def assign_questions_by_subject(self):
        related_questions = Question.objects.filter(quiz_subject=self.quiz_subject)
        self.questions.set(related_questions)
        self.save()
    
    def delete_session_in_redis(self):
        session_key = f"room:{self.id}"
        redis_client.delete(session_key)

    def add_participant_to_room(room_id, participant_id, participant_name):
        session_key = f"room:{room_id}"
        participants = json.loads(redis_client.hget(session_key, "participants") or "[]")
        participants.append({"id": participant_id, "name": participant_name})
        redis_client.hset(session_key, "participants", json.dumps(participants))

    def get_room_data(room_id):
        session_key = f"room:{room_id}"
        room_data = redis_client.hgetall(session_key)
        if not room_data:
            return None
        return {
            "participants": json.loads(room_data.get(b"participants", b"[]").decode()),
            "scores": json.loads(room_data.get(b"scores", b"{}").decode()),
            "status": room_data.get(b"status", b"waiting").decode(),
            "quiz_subject": room_data.get(b"quiz_subject", "").decode(),
            "invitation_code": room_data.get(b"invitation_code", "").decode(),
        }

    def update_score(room_id, participant_id, score):
        session_key = f"room:{room_id}"
        scores = json.loads(redis_client.hget(session_key, "scores") or "{}")
        scores[participant_id] = scores.get(participant_id, 0) + score
        redis_client.hset(session_key, "scores", json.dumps(scores))

    def get_scores(room_id):
        session_key = f"room:{room_id}"
        scores = redis_client.hget(session_key, "scores")
        return json.loads(scores) if scores else {}
