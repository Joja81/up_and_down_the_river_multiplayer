import 'package:json_annotation/json_annotation.dart';

part 'setup_update_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class SetupUpdate {
  int num_cards;
  bool is_owner;
  String game_id;
  List<String> user_names;
  bool game_started;

  SetupUpdate(this.num_cards, this.is_owner, this.game_id, this.user_names, this.game_started);

  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory SetupUpdate.fromJson(Map<String, dynamic> json) => _$SetupUpdateFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$SetupUpdateToJson(this);
}