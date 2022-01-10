import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:multiplayer_frontend/json%20class/card_class.dart';
import 'package:multiplayer_frontend/json%20class/collect_cards_class.dart';
import 'package:multiplayer_frontend/json%20class/get_guesses_class.dart';
import 'package:multiplayer_frontend/warning_popups.dart';

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
  late var token;
  late Map<String, Color> userColors;
  late Future<CollectCards> cards;
  late Future<GetGuesses> guesses;
  late String currentGuesser;
  bool userGuess = false;

  @override
  void initState() {
    super.initState();
    token = widget.token;
    userColors = widget.userColors;

    cards = collectCards();
    guesses = collectGuesses();


    // TODO add timer to update
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
            children: [
              _userCards(),
              _trumpCards(),
              Text("Guesses"),
              FutureBuilder(
                  future: collectGuesses(),
                  builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
                    if (snapshot.connectionState == ConnectionState.waiting) {
                      return const Center(
                        child: CircularProgressIndicator(),
                      );
                    } else if (snapshot.hasError) {
                      return Text('Error: ${snapshot.error}');
                    } else {
                      final GetGuesses getGuessesResponse = snapshot.data;
                      return Column(
                        children: [
                          const Text(("Guesses")),
                          SizedBox(
                            height: 100,
                            child: ListView(
                              shrinkWrap: true,
                              scrollDirection: Axis.horizontal,
                              children: [
                                for (Guess guess in getGuessesResponse.guesses) guess.displayGuess()
                              ],
                            ),
                          )
                        ],
                      );
                    }
                  }
                  ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _trumpCards() {
    return Column(
              children: [
                const Text("Trump card:"),
                FutureBuilder(
                    future: cards,
                    builder:
                    (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(
                      child: CircularProgressIndicator(),
                    );
                  } else if (snapshot.hasError) {
                    return Text('Error: ${snapshot.error}');
                  } else {
                    final collectCardsResponse = snapshot.data;
                    return collectCardsResponse.trump.displayCard();
                  }
                }),
              ],
            );
  }

  FutureBuilder<CollectCards> _userCards() {
    return FutureBuilder(
      future: cards,
      builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        } else if (snapshot.hasError) {
          return Text('Error: ${snapshot.error}');
        } else {
          final collectCardsResponse =
              snapshot.data;

          return Column(
            children: [
              (collectCardsResponse.cards.length == 1) ? const Text("User card") : const Text("User cards"),
              SizedBox(
                height: 100,
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

    var url = Uri.http(apiURL, "guess/collect_cards", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        return CollectCards.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
        return collectCards();
      }
    } catch (e) {
      print("error");
      WarningPopups.unknownError(context);
      return collectCards();
    }
  }

  Future<GetGuesses> collectGuesses() async {
    final params = {"token": token};

    var url = Uri.http(apiURL, "guess/get_guesses", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        print(response.body);
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        print(responseMap);
        print(responseMap['guesses']);
        return GetGuesses.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
        return collectGuesses();
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
      return collectGuesses();
    }
  }

}
