import 'package:json_annotation/json_annotation.dart';

part 'join_game_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class JoinGame {
  String token;
  int num_cards;
  bool is_owner;
  String game_id;
  List<String> user_names;

  JoinGame(this.token, this.num_cards, this.is_owner, this.game_id, this.user_names);

  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory JoinGame.fromJson(Map<String, dynamic> json) => _$JoinGameFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$JoinGameToJson(this);
}