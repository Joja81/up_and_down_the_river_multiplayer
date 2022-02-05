import 'package:flutter/cupertino.dart';
import 'package:json_annotation/json_annotation.dart';

part 'card_class.g.dart';

/// An annotation for the code generator to know that this class needs the
/// JSON serialization logic to be generated.
@JsonSerializable()
class PlayCard {
  String suit;
  String rank;
  String player;

  PlayCard(this.suit, this.rank, this.player);

  /// A necessary factory constructor for creating a new User instance
  /// from a map. Pass the map to the generated `_$UserFromJson()` constructor.
  /// The constructor is named after the source class, in this case, User.
  factory PlayCard.fromJson(Map<String, dynamic> json) => _$PlayCardFromJson(json);

  /// `toJson` is the convention for a class to declare support for serialization
  /// to JSON. The implementation simply calls the private, generated
  /// helper method `_$UserToJson`.
  Map<String, dynamic> toJson() => _$PlayCardToJson(this);

  displayCard({Map<String, Color>? userColors}){

    if (userColors != null){

      return Container(
        color: userColors[player],
        child: Column(
          children: [
            Text(suit),
            Text(rank),
            Text(player),
          ],
        ),
      );
    } else {

      return Column(
        children: [
          Text(suit),
          Text(rank),
        ],
      );
    }

  }

}