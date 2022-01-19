from src.error import InputError
from src.sql_classes.round_class import Round
from src.sql_classes.round_points_class import Round_point
from src.sql_classes.user_class import User


def get_curr_results(auth_user_id, session):
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage not in ['G', 'R', 'F']:
        raise InputError(description="Not in results stage")
    
    results = []

    for curr_user in game.users:
        points = session.query(Round_point).filter(Round_point.user == curr_user).order_by(Round_point.id.desc()).all()

        points_sum = 0

        for point in points:
            points_sum += point.points
        
        results.append({
            'name' : curr_user.name,
            'score' : points_sum,
            'change' : points[0].points,
            'is_user' : user.name == curr_user.name
        })


    return {
        'results' : results,
        'game_finished' : game.game_stage == 'F',
        'guessing_started' : len(points) != game.round_num
    }