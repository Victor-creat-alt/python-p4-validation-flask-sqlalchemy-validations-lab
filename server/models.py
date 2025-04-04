from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators for Author class
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("Author name cannot be empty.")
        # Check for uniqueness explicitly
        if db.session.query(Author).filter_by(name=value).first():
            raise ValueError(f"Author name '{value}' must be unique.")
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validators for Post class
    @validates('title')
    def validate_title(self, key, value):
        clickbait_keywords = ["You Won't Believe", "Secret", "Top", "Guess", "Reasons"]
        if not value or value.strip() == '':
            raise ValueError("Post title cannot be empty.")
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError("Post title must contain clickbait phrases.")
        return value

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Post summary cannot exceed 250 characters.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ['Fiction', 'Non-Fiction']
        if value not in valid_categories:
            raise ValueError(f"Category '{value}' is not valid. Must be 'Fiction' or 'Non-Fiction'.")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
