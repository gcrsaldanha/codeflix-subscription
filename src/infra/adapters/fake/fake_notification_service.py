from uuid import UUID


class FakeNotificationService:
    def notify(self, user_id: UUID, message: str) -> None:
        print(f"Notification sent to {user_id}: {message}")
