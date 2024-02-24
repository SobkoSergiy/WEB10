from random import randint
from datetime import timedelta, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import faker
from models import Contact, User
from libgravatar import Gravatar
from passlib.context import CryptContext

fake_data: faker.Faker = faker.Faker()


TOTAL_USERS = 10
TOTAL_CONTACTS = 100

def get_password_hash(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def create_users(count: int, session):
    pw = get_password_hash("password")

    for _ in range(count):
        em = fake_data.email()
        av = None
        try:
            g = Gravatar(em)
            av = g.get_image()
        except Exception as e:
            print(e)

        u = User(email = em, username = fake_data.first_name(), password = pw, avatar = av )
        session.add(u)
    session.commit()   

def create_contacts(count: int, session):
    for i in range(count):
        c = Contact(
            first_name = fake_data.first_name(),
            last_name = fake_data.last_name(),
            email = fake_data.email(),
            birthday = datetime.strptime(fake_data.date(end_datetime=datetime.now() - timedelta(days=5*365)), '%Y-%m-%d'),
            phone = fake_data.msisdn(),
            inform = f"<{i+1}> {fake_data.paragraph(nb_sentences=1)}",
            user_id = randint(1, TOTAL_USERS)
        )
        session.add(c)
    session.commit()   

    
def main():
    engine = create_engine('sqlite:///hw12rest.db', echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    create_users(TOTAL_USERS, session)
    create_contacts(TOTAL_CONTACTS, session)
    
    session.close()
    print("Data is cram")


if __name__ == "__main__":
    main()