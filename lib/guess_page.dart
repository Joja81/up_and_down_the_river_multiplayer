import 'dart:async';
import 'dart:convert';
import 'dart:ui';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:multiplayer_frontend/json%20class/card_class.dart';
import 'package:multiplayer_frontend/json%20class/collect_cards_class.dart';
import 'package:multiplayer_frontend/json%20class/get_guesses_class.dart';
import 'package:multiplayer_frontend/play_page.dart';
import 'package:multiplayer_frontend/warning_popups.dart';
import 'package:numberpicker/numberpicker.dart';

import 'config.dart';
import 'json class/guess_class.dart';

class GuessScreen extends StatefulWidget {
  final Map<String, Color> userColors;
  final String token;

  const GuessScreen({Key? key, required this.userColors, required this.token})
      : super(key: key);

  @override
  State<GuessScreen> createState() => _GuessScreenState();
}

class _GuessScreenState extends State<GuessScreen> {
  late String token;
  late Map<String, Color> userColors;
  late Future<CollectCards> cards;
  late GetGuesses guesses;
  late String currentGuesser;
  bool guessesCollected = false;

  int userGuess = 0;
  int maxCardNum = 52;

  Timer? timer;

  @override
  void initState() {
    super.initState();
    token = widget.token;
    userColors = widget.userColors;

    cards = collectCards();
    _updateGuesses();

    timer = Timer.periodic(const Duration(seconds: 2), (Timer t) => _updateGuesses());
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => false,
      child: Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: const Text("Guessing"),
          automaticallyImplyLeading: false,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _userCards(),
              _trumpCards(),
              _displayGuesses(),
              _collectGuess(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _collectGuess() {
    return guessesCollected && guesses.user_guess ? Column(
      children: [
        const SelectableText("Input guess"),
        SizedBox(
          height: 50,
          child: ScrollConfiguration(
            behavior: ScrollConfiguration.of(context)
                .copyWith(dragDevices: {
              // enable touch and mouse gesture
              PointerDeviceKind.touch,
              PointerDeviceKind.mouse,
            }),
            child: NumberPicker(
              //Selector for result
              value: userGuess,
              axis: Axis.horizontal,
              minValue: 0,
              maxValue:
              maxCardNum, //Stops player making result bigger then possible
              onChanged: (value) => setState(() => userGuess =
                  value), //Updates value as player moves scroller
            ),
          ),
        ),
        IconButton(onPressed: () {_sendUserGuess();}, icon: const Icon(Icons.send)),
      ],
    ) : Container();
  }

  Column _displayGuesses() {
    return Column(children: [
      const Text("Guesses"),
      guessesCollected
          ? SizedBox(
              height: 50,
              child: ListView(
                shrinkWrap: true,
                scrollDirection: Axis.horizontal,
                children: [
                  for (Guess guess in guesses.guesses)
                    guess.displayGuess(userColors)
                ],
              ),
            )
          : const SizedBox(
              height: 50,
              child: CircularProgressIndicator(),
            )
    ]);
  }

  Widget _trumpCards() {
    return Column(
      children: [
        const Text("Trump card:"),
        FutureBuilder(
            future: cards,
            builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(
                  child:
                      SizedBox(height: 50, child: CircularProgressIndicator()),
                );
              } else if (snapshot.hasError) {
                return Text('Error: ${snapshot.error}');
              } else {
                final collectCardsResponse = snapshot.data;
                return SizedBox(
                  height: 50,
                  child: collectCardsResponse.trump.displayCard(),
                );
              }
            }),
      ],
    );
  }

  Widget _userCards() {
    return FutureBuilder(
      future: cards,
      builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(
            child: SizedBox(height: 50, child: CircularProgressIndicator()),
          );
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else {
          final collectCardsResponse = snapshot.data;

          return Column(
            children: [
              (collectCardsResponse.cards.length == 1)
                  ? const Text("User card")
                  : const Text("User cards"),
              SizedBox(
                height: 50,
                child: ListView(
                  shrinkWrap: true,
                  scrollDirection: Axis.horizontal,
                  children: [
                    for (PlayCard card in collectCardsResponse.cards)
                      card.displayCard()
                  ],
                ),
              ),
            ],
          );
        }
      },
    );
  }

  Future<CollectCards> collectCards() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "guess/collect_cards", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        CollectCards returnValue = CollectCards.fromJson(responseMap);

        setState(() {
          maxCardNum = returnValue.cards.length;
        });

        return returnValue;
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        WarningPopups.httpError(response, context);
        return collectCards();
      }
    } catch (e) {
      if (kDebugMode) {
        print(e);
      }
      WarningPopups.unknownError(context);
      return collectCards();
    }
  }

  Future<void> _updateGuesses() async {

    GetGuesses newGuesses = await _collectGuesses();

    if (newGuesses.is_guessing_complete) {
      _shiftToPlay();
    }

    setState(() {
      guesses = newGuesses;
      guessesCollected = true;
    });
  }

  Future<GetGuesses> _collectGuesses() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "guess/get_guesses", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        return GetGuesses.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        WarningPopups.httpError(response, context);
        return _collectGuesses();
      }
    } catch (e) {
      if (kDebugMode) {
        print(e);
      }
      WarningPopups.unknownError(context);
      return _collectGuesses();
    }
  }

  Future<void> _sendUserGuess() async {
    final params = {"token": token, "guess": userGuess};

    var url = Uri.https(apiURL, "guess/give_guess");
    try {
      http.Response response =
          await http.post(url, headers: jsonHeader, body: json.encode(params));
      if (response.statusCode == 200) {
        _updateGuesses();
      } else {
        WarningPopups.httpError(response, context);
      }
    } catch (e) {
      WarningPopups.unknownError(context);
    }
  }

  @override
  void dispose() {
    super.dispose();

    timer?.cancel();
  }

  Future<void> _shiftToPlay() async {
    // TODO add display showing waiting and turn on delay
    // await Future.delayed(const Duration(seconds: 5));
    
    timer?.cancel();

    Navigator.push(context,
        MaterialPageRoute(builder: (context) => PlayScreen(token: token, userColors: userColors, guesses: guesses,)));
  }
}