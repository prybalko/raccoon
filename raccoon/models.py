from raccoon import db

TASK_STATES = ['queued', 'in progress', 'success', 'fail']


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String)
    params = db.Column(db.String)
    email = db.Column(db.String)
    submit_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.Enum(*TASK_STATES), default='queued')

    def __repr__(self):
        return '<Task %r>' % self.id
