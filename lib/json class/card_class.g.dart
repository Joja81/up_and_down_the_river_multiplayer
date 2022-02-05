// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'card_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

PlayCard _$PlayCardFromJson(Map<String, dynamic> json) => PlayCard(
      json['suit'] as String,
      json['rank'] as String,
      json['player'] as String,
    );

Map<String, dynamic> _$PlayCardToJson(PlayCard instance) => <String, dynamic>{
      'suit': instance.suit,
      'rank': instance.rank,
      'player': instance.player,
    };
