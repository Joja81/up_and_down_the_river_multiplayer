// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'guess_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Guess _$GuessFromJson(Map<String, dynamic> json) => Guess(
      json['player_name'] as String,
      json['player_guess'] as int,
    );

Map<String, dynamic> _$GuessToJson(Guess instance) => <String, dynamic>{
      'player_name': instance.player_name,
      'player_guess': instance.player_guess,
    };
