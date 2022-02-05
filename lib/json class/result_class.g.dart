// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'result_class.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Result _$ResultFromJson(Map<String, dynamic> json) => Result(
      json['name'] as String,
      json['score'] as int,
      json['change'] as int,
      json['is_user'] as bool,
    );

Map<String, dynamic> _$ResultToJson(Result instance) => <String, dynamic>{
      'name': instance.name,
      'score': instance.score,
      'change': instance.change,
      'is_user': instance.is_user,
    };
