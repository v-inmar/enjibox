from app import db
from app.models.base_model import BaseModel

class ContactModel(BaseModel):
    __tablename__ = "contact_model"

    pid_id = db.Column(db.BigInteger, db.ForeignKey("contact_pid_model.id"), nullable=False, unique=True)
    firstname_id = db.Column(db.BigInteger, db.ForeignKey("user_firstname_model.id"), nullable=False)
    lastname_id = db.Column(db.BigInteger, db.ForeignKey("user_lastname_model.id"), nullable=False)
    email_id = db.Column(db.BigInteger, db.ForeignKey("user_email_model.id"), nullable=False)
    message_id = db.Column(db.BigInteger, db.ForeignKey("contact_message_model.id"), nullable=False)


    def __init__(self, pid_id: int, firstname_id: int, lastname_id: int, email_id: int, message_id: int) -> None:
        super().__init__()
        self.pid_id = pid_id
        self.firstname_id = firstname_id
        self.lastname_id = lastname_id
        self.email_id = email_id
        self.message_id = message_id
