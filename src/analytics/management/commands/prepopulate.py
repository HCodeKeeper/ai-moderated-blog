import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from posts.models import Comment, Post, Reply

faker = Faker()


class Command(BaseCommand):
    help = "Prepopulates database so functionality like analytics is available."

    def add_arguments(self, parser):
        parser.add_argument(
            "-no-rep",
            "--dont-repeat",
            action="store_true",
            help="Set to True if you want to avoid populating more if already populated",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        already_populated_id = "__special_reserved_email_prepopulated"
        if options["dont_repeat"]:
            if user_model.objects.filter(email__startswith=already_populated_id).exists():
                self.stdout.write(self.style.SUCCESS("Database already prepopulated"))
                return

        users = [
            user_model.objects.create(
                email=faker.email(),
                password=faker.password(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
            )
            for _ in range(20)
        ]
        users.append(
            user_model.objects.create(
                email="__special_reserved_email_prepopulated" + faker.email(), password=faker.password()
            )
        )
        posts = []

        date_time = faker.date_time_this_year(after_now=False)
        for i in range(100):
            if i > 0 and i % 7 == 0:
                date_time = faker.date_time_this_year(after_now=False)
            post = Post(
                title=faker.sentence(),
                content=faker.text(),
                is_blocked=faker.boolean(),
                author=random.choice(users),
                created_at=date_time,
            )
            post.save(force_insert=True)
            posts.append(post)
        comments = []
        date_time = faker.date_time_this_year(after_now=False)
        for i in range(400):
            if i > 0 and i % 7 == 0:
                date_time = faker.date_time_this_year(after_now=False)
            comment = Comment(
                content=faker.text(),
                author=random.choice(users),
                post=random.choice(posts),
                is_blocked=faker.boolean(),
                created_at=date_time,
            )
            comment.save(force_insert=True)
            comments.append(comment)

        replies = []
        for _ in range(20):
            reply = Reply(
                content=faker.text(),
                author=random.choice(users),
                comment=random.choice(comments),
                created_at=faker.date_time_this_year(after_now=False),
                is_blocked=faker.boolean(),
            )
            reply.save(force_insert=True)
            replies.append(reply)

        for _ in range(20):
            reply = Reply(
                content=faker.text(),
                author=random.choice(users),
                comment=random.choice(comments),
                created_at=faker.date_time_this_year(after_now=False),
                is_blocked=faker.boolean(),
                parent_reply=random.choice(replies),
            )
            reply.save(force_insert=True)

        self.stdout.write(self.style.SUCCESS("Command executed successfully"))
