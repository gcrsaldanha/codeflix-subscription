from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlmodel import select

from src.domain.entities import UserAccount, Plan, Subscription
from src.infra.db.models import (
    UserAccount as UserAccountModel,
    Plan as PlanModel,
    Subscription as SubscriptionModel,
)


class BaseRepositorySA:
    def __init__(self, session: Session):
        self.session = session


class UserRepositorySA(BaseRepositorySA):
    def save(self, user: UserAccount):
        user_model = UserAccountModel(
            id=user.id,
            iam_user_id=user.iam_user_id,
            name=user.name,
            email=user.email,
            billing_address=user.billing_address,
        )
        self.session.add(user_model)
        self.session.commit()

    def find_by_email(self, email: str) -> Optional[UserAccount]:
        user_model = self.session.execute(
            select(UserAccountModel).where(UserAccountModel.email == email)
        ).one_or_none()
        if user_model:
            return UserAccount(
                id=user_model.id,
                iam_user_id=user_model.iam_user_id,
                name=user_model.name,
                email=user_model.email,
                billing_address=user_model.billing_address,
            )
        return None


class PlanRepositorySA(BaseRepositorySA):
    def find_by_id(self, plan_id: UUID) -> Optional[Plan]:
        plan_model = self.session.execute(
            select(PlanModel).where(PlanModel.id == plan_id)
        ).one_or_none()
        if plan_model:
            return Plan(
                id=plan_model.id,
                name=plan_model.name,
                price=plan_model.price,
                currency=plan_model.currency,
            )
        return None

    def find_by_name(self, name: str) -> Optional[Plan]:
        plan_model = self.session.execute(
            select(PlanModel).where(PlanModel.name == name)
        ).one_or_none()
        if plan_model:
            return Plan(
                id=plan_model.id,
                name=plan_model.name,
                price=plan_model.price,
                currency=plan_model.currency,
            )
        return None

    def save(self, plan: Plan):
        plan_model = PlanModel(
            id=plan.id, name=plan.name, price=plan.price, currency=plan.currency
        )
        self.session.add(plan_model)
        self.session.commit()


class SubscriptionRepositorySA(BaseRepositorySA):
    def get_user_subscription(self, user_id: UUID) -> Optional[Subscription]:
        subscription_model = self.session.execute(
            select(SubscriptionModel).where(SubscriptionModel.user_id == user_id)
        ).one_or_none()
        if subscription_model:
            return Subscription(
                id=subscription_model.id,
                user_id=subscription_model.user_id,
                plan_id=subscription_model.plan_id,
                start_date=subscription_model.start_date,
                end_date=subscription_model.end_date,
                status=subscription_model.status,
                is_trial=subscription_model.is_trial,
            )
        return None

    def save(self, subscription: Subscription):
        subscription_model = SubscriptionModel(
            id=subscription.id,
            user_id=subscription.user_id,
            plan_id=subscription.plan_id,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            status=subscription.status,
            is_trial=subscription.is_trial,
        )
        self.session.add(subscription_model)
        self.session.commit()
