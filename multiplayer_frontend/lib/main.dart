import 'package:flutter/material.dart';
import 'package:flex_color_scheme/flex_color_scheme.dart';

import 'front_page.dart';

void main() {
  runApp(const MyApp());
}

const FlexScheme _scheme = FlexScheme.blueWhale;

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Up and down the river',
      theme: FlexThemeData.light(
        scheme: _scheme,
      ),
      home: const StartScreen(),
    );
  }
}
