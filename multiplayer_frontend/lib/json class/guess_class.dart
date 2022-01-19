import 'package:flutter/cupertino.dart';
import 'package:json_annotation/json_annotation.dart';

part 'guess_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class Guess {
  Guess(this.player_name, this.player_guess);

  String player_name;
  int player_guess;


  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory Guess.fromJson(Map<String, dynamic> json) => _$GuessFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$GuessToJson(this);

  Widget displayGuess(Map<String, Color> userColors) {
    return Container(
      color: userColors[player_name],
      child: Column(
        children: [
          Text(player_name),
          Text(player_guess.toString())
        ],
      ),
    );
  }
}