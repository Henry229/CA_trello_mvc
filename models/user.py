from init import db, ma

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # card는 user와 종속관계가 있고 user가 삭제되면 card의 모든 record가 사라짐. 그걸 cascade로 정의
    cards = db.relationship('Card', back_populates='user', cascade='all, delete')
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')