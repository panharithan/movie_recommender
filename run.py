import click
from sqlalchemy import or_
from movie_recommender import app, db, migrate
from movie_recommender.models import Movie, User


@app.cli.command(name="admin-create")
@click.argument("name")
@click.argument("email")
@click.argument("password")
def create_admin(name, email, password):
    """Create a new Admin.\n
    params: name, email and password.\n
    For example: $ flask admin-create admin mymail@mail.com 123"""
    conds = [User.username == name, User.email == email]
    if User.query.filter(or_(*conds)).first():
        click.echo('Error! username or email %s already exists')
        return
    new_user = User(username=name, email=email, password=password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    click.echo('Success! Admin with username of %s has been added.' % name)


@app.cli.command(name="admin-resetpassword")
@click.argument("identity")
@click.argument("password")
def reset_password_admin(identity, password):
    """Reset password of admin.\n
    params: username/email, password.\n
    For example: $ flask admin-resetpassword mymail@mail.com 321"""
    conds = [User.username == identity, User.email == identity]
    user = User.query.filter(or_(*conds)).first()
    if not User.query.filter(or_(*conds)).first():
        click.echo('Error! username or email %s does not exists' % identity)
        return

    from passlib.hash import sha256_crypt
    user.password = sha256_crypt.encrypt(password)
    db.session.add(user)
    db.session.commit()
    click.echo('Success Reset Password of admin %s ' % identity)


@app.cli.command(name="admin-delete")
@click.argument("identity")
@click.option('--confirm', default=False, help='yes/no.')
def delete_admin(identity, confirm):
    """Reset password of admin.\n
    params: username/email, --confirm=yes/no\n
    For example: $ flask admin-delete mymail@mail.com --confirm=yes"""
    if confirm == 'no' or not confirm:
        click.echo('Please confirm by add param --confirm=yes')
        return

    conds = [User.username == identity, User.email == identity]
    user = User.query.filter(or_(*conds)).first()
    if not User.query.filter(or_(*conds)).first():
        click.echo('Error! username or email %s does not exists' % identity)
        return

    db.session.delete(user)
    db.session.commit()
    click.echo('Success Deleted admin %s ' % identity)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Movie=Movie, User=User, migraFte=migrate)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
