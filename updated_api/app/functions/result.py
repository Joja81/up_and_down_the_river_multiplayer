from app.functions.error import InputError
from app.models import Round_point, User


def get_curr_results(auth_user_id):
    user = User.query.get(auth_user_id)
    game = user.game

    results = []

    for curr_user in game.users:
        points = Round_point.query.filter(
            Round_point.user == curr_user).order_by(Round_point.id.desc()).all()

        points_sum = 0

        for point in points:
            points_sum += point.points

        print("User points")
        print(points)

        if len(points) < 1:
            results.append({
                'name': curr_user.name,
                'score': points_sum,
                'change': 0,
                'is_user': user.name == curr_user.name
            })
        else:
            results.append({
                'name': curr_user.name,
                'score': points_sum,
                'change': points[0].points,
                'is_user': user.name == curr_user.name
            })

    return {
        'results': results,
        'game_finished': game.game_stage == 'F'
    }
