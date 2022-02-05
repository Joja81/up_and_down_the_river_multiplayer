// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'get_guesses_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GetGuesses _$GetGuessesFromJson(Map<String, dynamic> json) => GetGuesses(
      (json['guesses'] as List<dynamic>)
          .map((e) => Guess.fromJson(e as Map<String, dynamic>))
          .toList(),
      json['current_guesser'] as String,
      json['user_guess'] as bool,
      json['is_guessing_complete'] as bool,
    );

Map<String, dynamic> _$GetGuessesToJson(GetGuesses instance) =>
    <String, dynamic>{
      'guesses': instance.guesses,
      'current_guesser': instance.current_guesser,
      'user_guess': instance.user_guess,
      'is_guessing_complete': instance.is_guessing_complete,
    };
