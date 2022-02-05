// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'get_curr_results_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GetCurrResults _$GetCurrResultsFromJson(Map<String, dynamic> json) =>
    GetCurrResults(
      (json['results'] as List<dynamic>)
          .map((e) => Result.fromJson(e as Map<String, dynamic>))
          .toList(),
      json['game_finished'] as bool,
    );

Map<String, dynamic> _$GetCurrResultsToJson(GetCurrResults instance) =>
    <String, dynamic>{
      'results': instance.results,
      'game_finished': instance.game_finished,
    };
