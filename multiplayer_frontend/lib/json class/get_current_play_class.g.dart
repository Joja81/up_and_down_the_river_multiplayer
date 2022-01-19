// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'get_current_play_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CurrentPlay _$CurrentPlayFromJson(Map<String, dynamic> json) => CurrentPlay(
      (json['cards'] as List<dynamic>)
          .map((e) => PlayCard.fromJson(e as Map<String, dynamic>))
          .toList(),
      json['play_num'] as int,
      json['curr_user_turn'] as String,
      json['is_player_turn'] as bool,
      json['is_finished'] as bool,
    );

Map<String, dynamic> _$CurrentPlayToJson(CurrentPlay instance) =>
    <String, dynamic>{
      'cards': instance.cards,
      'play_num': instance.play_num,
      'curr_user_turn': instance.curr_user_turn,
      'is_player_turn': instance.is_player_turn,
      'is_finished': instance.is_finished,
    };
