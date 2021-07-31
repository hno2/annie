from annie.extensions import db, BaseMixin


class Chat(db.Model, BaseMixin):
    __tablename__ = "chats"
    messages = db.relationship("Message", backref="chat", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Message(db.Model, BaseMixin):
    __tablename__ = "messages"
    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"))
    message_type = db.Column(db.String(50))
    content = db.Column(db.String(500))
