// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'collect_cards_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CollectCards _$CollectCardsFromJson(Map<String, dynamic> json) => CollectCards(
      (json['cards'] as List<dynamic>)
          .map((e) => PlayCard.fromJson(e as Map<String, dynamic>))
          .toList(),
      PlayCard.fromJson(json['trump'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$CollectCardsToJson(CollectCards instance) =>
    <String, dynamic>{
      'cards': instance.cards,
      'trump': instance.trump,
    };
