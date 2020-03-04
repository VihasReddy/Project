from app import db
from app.models import User, EmpDetails


def load_user():
    u = User(id='T0123', username='Spandana', email='spandanavarukolu@gmail.com', overall_exp=2, manager_id='2333')
    u.set_password('1234')
    db.session.add(u)
    db.session.commit()


def print_user():
    user = User.query.all()
    for u in user:
        print(u.id, u.username, u.manager_id)
    u1 = User.query.get('T0123')
    ok = u1.employees.all()
    for i in ok:
        print(i.emp_id, i.experience, i.emp_rating)


if __name__ == '__main__':
    """print("Enter 0 - print_user, 1 - Load user : ")
    i = bool(input())
    if i == 1:
        load_user()
    else:"""
    print_user()
