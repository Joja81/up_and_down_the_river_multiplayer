// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'setup_update_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SetupUpdate _$SetupUpdateFromJson(Map<String, dynamic> json) => SetupUpdate(
      json['num_cards'] as int,
      json['is_owner'] as bool,
      json['game_id'] as String,
      (json['user_names'] as List<dynamic>).map((e) => e as String).toList(),
      json['game_started'] as bool,
    );

Map<String, dynamic> _$SetupUpdateToJson(SetupUpdate instance) =>
    <String, dynamic>{
      'num_cards': instance.num_cards,
      'is_owner': instance.is_owner,
      'game_id': instance.game_id,
      'user_names': instance.user_names,
      'game_started': instance.game_started,
    };
