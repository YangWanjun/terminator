from wtforms import Form


class MyForm(Form):

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.instance = (len(args) > 1 and args[1]) or kwargs.get('obj')
