import logging

from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db.models import Q

from profiles.models import Profile
from profiles.models.friendship_models import FriendshipStatus, Friendship

logger = logging.getLogger(__name__)


class FriendshipService:

    @staticmethod
    def get_friendship(user1, user2):
        try:
            return Friendship.objects.filter(
                Q(sender=user1, receiver=user2) |
                Q(sender=user2, receiver=user1)
            ).first()
        except Friendship.DoesNotExist:
            logger.error(f"Friendship between {user1} and {user2} does not exist")
            return None

    @staticmethod
    def send_friendship_request(sender, receiver):
        try:
            if sender == receiver:
                raise ValidationError("You can't send a friendship request to yourself!")

            existing = FriendshipService.get_friendship(sender, receiver)
            if existing is None:
                friendship = Friendship.objects.create(
                    sender=sender,
                    receiver=receiver,
                    status=FriendshipStatus.PENDING,
                )
                logger.info(f"Friendship sent from {sender} to {receiver}")
                return friendship

            elif (existing.sender == sender and existing.receiver == receiver and
                  existing.status == FriendshipStatus.PENDING):
                raise ValidationError("The friendship request are already sent!")

            elif (existing.sender == receiver and existing.receiver == sender and
                  existing.status == FriendshipStatus.PENDING):
                existing.accept()
                logger.info(f"Friendship automatically accepted between {sender.id} and {receiver.id}")

            else:
                raise ValidationError('The request has not be sent')

        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            raise ValidationError(f"Database error occurred!")

    @staticmethod
    def accept_request(friendship, by_user):
        try:
            if friendship.receiver != by_user:
                raise ValidationError("You can't accept this request!")
            if friendship.status != FriendshipStatus.PENDING:
                raise ValidationError("This request cannot be accepted!")

            friendship.accept()
            logger.info(f"Friendship {friendship.pk} accepted by {by_user}")
            return friendship
        except DatabaseError as e:
            logger.error(f"Database error: {e}")
            raise ValidationError(f"Database error occurred!")

    @staticmethod
    def reject_request(friendship, by_user):
        try:
            if friendship.receiver != by_user:
                raise ValidationError("You cannot reject this request.")
            if friendship.status != FriendshipStatus.PENDING:
                raise ValidationError("This request cannot be rejected.")

            friendship.reject()
            friendship.delete()
            logger.info(f"Friend request {friendship.id} rejected by {by_user.id}")
            return friendship

        except DatabaseError as e:
            logger.error(f"Database error rejecting friend request {friendship.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def cancel_request(friendship, by_user):
        try:
            if friendship.sender != by_user:
                raise ValidationError("You cannot cancel this request.")
            if friendship.status != FriendshipStatus.PENDING:
                raise ValidationError("This request cannot be cancelled.")

            friendship.delete()
            logger.info(f"Friend request {friendship.id} cancelled by {by_user.id}")

        except DatabaseError as e:
            logger.error(f"Database error cancelling friend request {friendship.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def remove_friend(friendship, by_user):
        try:
            if friendship.status != FriendshipStatus.ACCEPTED:
                raise ValidationError("User is not a friend.")
            if by_user not in [friendship.sender, friendship.receiver]:
                raise ValidationError("You cannot delete this user.")

            friendship.delete()
            logger.info(f"Friendship {friendship.id} removed by {by_user.id}")

        except DatabaseError as e:
            logger.error(f"Database error removing friendship {friendship.id}: {e}")
            raise ValidationError("Database error occurred")


    @staticmethod
    def get_incoming_requests(user):
        try:
            return Friendship.objects.filter(
                receiver=user,
                status=FriendshipStatus.PENDING,
            ).select_related('sender', 'sender__user')
        except DatabaseError as e:
            logger.error(f"Database error getting incoming requests: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def get_outgoing_requests(user):
        try:
            return Friendship.objects.filter(
                sender=user,
                status=FriendshipStatus.PENDING,
            ).select_related('receiver', 'receiver__user')
        except DatabaseError as e:
            logger.error(f"Database error getting outgoing requests: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def get_friends(user):
        try:
            return Profile.objects.filter(
                Q(sent_friendships__receiver=user, sent_friendships__status=FriendshipStatus.ACCEPTED) |
                Q(received_friendships__sender=user, received_friendships__status=FriendshipStatus.ACCEPTED)
            ).select_related('user').distinct()
        except DatabaseError as e:
            logger.error(f"Database error getting friends: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def get_friends_count(user):
        try:
            count = Friendship.objects.filter(
                Q(sender=user, status=FriendshipStatus.ACCEPTED) |
                Q(receiver=user, status=FriendshipStatus.ACCEPTED)
            ).count()
            return count
        except DatabaseError as e:
            logger.error(f"Database error getting friends_count: {e}")
            return 0

    @staticmethod
    def get_incoming_requests_count(user):
        try:
            count = Friendship.objects.filter(
                receiver=user,
                status=FriendshipStatus.PENDING,
            ).count()
            return count
        except DatabaseError as e:
            logger.error(f"Database error getting incoming_requests_count: {e}")
            return 0

    @staticmethod
    def get_outgoing_requests_count(user):
        try:
            count = Friendship.objects.filter(
                sender=user,
                status=FriendshipStatus.PENDING,
            ).count()
            return count
        except DatabaseError as e:
            logger.error(f"Database error getting outgoing_requests_count: {e}")
            return 0
