from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add sample employees and departments
user1 = User(first_name='lexsa', last_name='campbell')
user2 = User(first_name='mia', last_name='campbell')

post1 = Post(title="hi", content="heyyy", user_id="1")
post2 = Post(title="bye", content="byeeee", user_id="1")
post3 = Post(title="woof", content="woooooof", user_id="2")
post4 = Post(title="bark", content="bbbarrrrrkkkk", user_id="2") 

db.session.add_all([user1, user2, post1, post2, post3, post4])
db.session.commit()
