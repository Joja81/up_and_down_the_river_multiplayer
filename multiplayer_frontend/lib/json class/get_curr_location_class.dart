import 'package:json_annotation/json_annotation.dart';

part 'get_curr_location_class.g.dart';

@JsonSerializable()
class GetCurrLocation {
  String game_location;

  GetCurrLocation(this.game_location);

  factory GetCurrLocation.fromJson(Map<String, dynamic> json) => _$GetCurrLocationFromJson(json);

  Map<String, dynamic> toJson() => _$GetCurrLocationToJson(this);
}