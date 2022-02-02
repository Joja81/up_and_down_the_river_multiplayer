import 'package:json_annotation/json_annotation.dart';
import 'package:multiplayer_frontend/json%20class/result_class.dart';

part 'get_curr_results_class.g.dart';

@JsonSerializable()
class GetCurrResults{
  List<Result> results;
  bool game_finished;

  GetCurrResults(this.results, this.game_finished);

  factory GetCurrResults.fromJson(Map<String, dynamic> json) => _$GetCurrResultsFromJson(json);

  Map<String, dynamic> toJson() => _$GetCurrResultsToJson(this);
}