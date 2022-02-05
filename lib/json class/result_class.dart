import 'package:json_annotation/json_annotation.dart';

part 'result_class.g.dart';

@JsonSerializable()
class Result{
  String name;
  int score;
  int change;
  bool is_user;

  Result(this.name, this.score, this.change, this.is_user);

  factory Result.fromJson(Map<String, dynamic> json) => _$ResultFromJson(json);

  Map<String, dynamic> toJson() => _$ResultToJson(this);
}