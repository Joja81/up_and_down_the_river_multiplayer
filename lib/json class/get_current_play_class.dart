import 'package:json_annotation/json_annotation.dart';
import 'package:multiplayer_frontend/json%20class/card_class.dart';

/// This allows the `User` class to access private members in
/// the generated file. The value for this is *.g.dart, where
/// the star denotes the source file name.
part 'get_current_play_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class CurrentPlay {
  CurrentPlay(this.cards, this.play_num, this.curr_user_turn, this.is_player_turn, this.is_finished, this.round_finished);

  List<PlayCard> cards;
  int play_num;
  String curr_user_turn;
  bool is_player_turn;
  bool is_finished;
  bool round_finished;


  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory CurrentPlay.fromJson(Map<String, dynamic> json) => _$CurrentPlayFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$CurrentPlayToJson(this);
}