import 'package:json_annotation/json_annotation.dart';
import 'package:multiplayer_frontend/json%20class/guess_class.dart';

part 'get_guesses_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class GetGuesses {
  List<Guess> guesses;
  String current_guesser;
  bool user_guess;
  bool is_guessing_complete;

  GetGuesses(this.guesses, this.current_guesser, this.user_guess, this.is_guessing_complete);

  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory GetGuesses.fromJson(Map<String, dynamic> json) => _$GetGuessesFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$GetGuessesToJson(this);
}