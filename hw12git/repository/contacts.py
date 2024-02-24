from sqlalchemy import and_
from sqlalchemy.orm import Session

from database.models import Contact, User
from schemas import ContactModel, ContactUpdate, ContactUpdateAvatar


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> list[Contact]:
    return (db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all())


async def get_contact(Contact_id: int, user: User, db: Session) -> Contact:
    return (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(Contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.inform = body.inform
        contact.birthday = body.birthday
        contact.email = body.email
        db.commit()
    return contact


async def update_avatar(Contact_id: int, body: ContactUpdateAvatar, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())
    if contact:
        contact.avatar = body.avatar
        db.commit()
    return contact


async def remove_contact(Contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (db.query(Contact).filter(and_(Contact.id == Contact_id, Contact.user_id == user.id)).first())
    if contact:
        db.delete(contact)
        db.commit()
    return contact