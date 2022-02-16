// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'join_game_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

JoinGame _$JoinGameFromJson(Map<String, dynamic> json) => JoinGame(
      json['token'],
      json['num_cards'] as int,
      json['is_owner'] as bool,
      json['game_id'] as String,
      (json['user_names'] as List<dynamic>).map((e) => e as String).toList(),
    );

Map<String, dynamic> _$JoinGameToJson(JoinGame instance) => <String, dynamic>{
      'token': instance.token,
      'num_cards': instance.num_cards,
      'is_owner': instance.is_owner,
      'game_id': instance.game_id,
      'user_names': instance.user_names,
    };
