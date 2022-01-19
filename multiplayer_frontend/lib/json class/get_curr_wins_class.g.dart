// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'get_curr_wins_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CurrentWins _$CurrentWinsFromJson(Map<String, dynamic> json) => CurrentWins(
      (json['scores'] as List<dynamic>)
          .map((e) => Score.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$CurrentWinsToJson(CurrentWins instance) =>
    <String, dynamic>{
      'scores': instance.scores,
    };
