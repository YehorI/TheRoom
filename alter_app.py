from flask import Flask, render_template, request, redirect, url_for
from forms import Movement, Preferences
from alter_house import Game # !!!!!!!!
app = Flask(__name__)
app.secret_key = 'my_key'


@app.route('/', methods=['get', 'post'])
def index():
    form = Preferences()
    if form.validate_on_submit():
        Game(form.height.data, form.width.data, form.control_type.data, form.generation_type.data)
        return redirect(url_for('game'))
    return render_template(
        'index.html',
        form=form
    )


@app.route('/game', methods=['get', 'post'])
def game():

    form = Movement()
    game = Game()

    if form.validate_on_submit():

        rooms_and_events = game.movement(
            form.direction.data,
            form.distance.data,
            get_named=True
            )

        return render_template(
            'game.html',
            form = form,
            rooms_and_events = rooms_and_events,
            rendered_rooms = game.render_game(),
            end_location = game.end_location,
            start_location = game.start_location,
            mov_or_gam = game.controls
        )

    else:

        return render_template(
            'game.html',
            form = form,
            rendered_rooms = game.render_game(),
            end_location = game.end_location,
            start_location = game.start_location,
            mov_or_gam = game.controls
        )

@app.route('/gamepad/<direction>', methods=['POST'])
def gamepad(direction):
    directions = {
        'up': 'Север', 'right': 'Восток', 'down': 'Юг', 'left': 'Запад'
    }
    form = Movement()
    game = Game()
    rooms_and_events = game.movement(
            directions[direction],
            1,
            get_named=True
            )
    if request.method == 'POST':
        return render_template(
                'game.html',
                form = form,
                rooms_and_events = rooms_and_events,
                rendered_rooms = game.render_game(),
                end_location = game.end_location,
                start_location = game.start_location,
                mov_or_gam = game.controls
            )
        


if __name__ == '__main__':
    app.run(debug=True)