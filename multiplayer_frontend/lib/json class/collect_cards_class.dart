import 'package:json_annotation/json_annotation.dart';
import 'package:multiplayer_frontend/json%20class/card_class.dart';

part 'collect_cards_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class CollectCards {
  List<PlayCard> cards;
  PlayCard trump;

  CollectCards(this.cards, this.trump);

  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory CollectCards.fromJson(Map<String, dynamic> json) => _$CollectCardsFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$CollectCardsToJson(this);
}