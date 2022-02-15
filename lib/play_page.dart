import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:multiplayer_frontend/json%20class/card_class.dart';
import 'package:multiplayer_frontend/json%20class/collect_cards_class.dart';
import 'package:multiplayer_frontend/json%20class/get_curr_wins_class.dart';
import 'package:multiplayer_frontend/json%20class/get_current_play_class.dart';
import 'package:multiplayer_frontend/json%20class/guess_class.dart';
import 'package:multiplayer_frontend/json%20class/score_class.dart';
import 'package:multiplayer_frontend/results_page.dart';
import 'package:multiplayer_frontend/warning_popups.dart';

import 'config.dart';
import 'json class/get_guesses_class.dart';

class PlayScreen extends StatefulWidget {
  final Map<String, Color> userColors;
  final GetGuesses guesses;
  final String token;

  const PlayScreen(
      {Key? key,
      required this.userColors,
      required this.guesses,
      required this.token})
      : super(key: key);

  @override
  State<PlayScreen> createState() => _PlayScreenState();
}

class _PlayScreenState extends State<PlayScreen> {
  Timer? timer;

  late String token;
  late Map<String, Color> userColors;
  late GetGuesses guesses;

  late CollectCards userCards;
  bool userCardsLoaded = false;

  late CurrentPlay currentPlay;
  bool currentPlayLoaded = false;

  late CurrentWins currentWins;
  bool currentWinsLoaded = false;

  @override
  void initState() {
    super.initState();

    token = widget.token;
    userColors = widget.userColors;
    guesses = widget.guesses;

    loadData();

    timer = Timer.periodic(const Duration(seconds: 2), (Timer t) => loadData());
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => false,
      child: Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: const Text("Playing"),
          automaticallyImplyLeading: false,
        ),
        body: isLoaded()
            ? Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _displayPlayerScores(),
                  _displayTrumpCard(),
                  currentPlay.cards.isNotEmpty
                      ? _displayPlayedCards()
                      : Container(),
                  currentPlay.is_player_turn
                      ? const Text("It is your turn")
                      : Text(
                          "Current player turn: ${currentPlay.curr_user_turn}"),
                  _displayCards(),
                ],
              )
            : const Center(child: CircularProgressIndicator()),
      ),
    );
  }

  Widget _displayPlayerScores(){
    return Column(
      children: [
        const Text("Scores and guesses"),
        SizedBox(
          height: 50,
          child: ListView(
            shrinkWrap: true,
            scrollDirection: Axis.horizontal,
            children: [
              for (Guess guess in guesses.guesses)
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 10),
                  padding: EdgeInsets.symmetric(horizontal: 5),
                  color: userColors[guess.player_name],
                  child: Column(
                    children: [
                      Text(guess.player_name),
                      Text("Score: ${_findPlayerWins(guess.player_name)}"),
                      Text("Guess: ${guess.player_guess}"),
                    ],
                  ),
                )
            ],
          ),
        )
      ],
    );
  }

  int _findPlayerWins(String name){
    for (Score score in currentWins.scores){
      if (score.name == name){
        return score.score;
      }
    }
    return 0;
  }

  Widget _displayPlayedCards() {
    return Column(
      children: [
        const Text("Played cards"),
        SizedBox(
          height: 70,
          child: Center(
            child: ListView(
              shrinkWrap: true,
              scrollDirection: Axis.horizontal,
              children: [
                for (PlayCard card in currentPlay.cards)
                  Column(
                    children: [
                      card.displayCard(userColors: userColors),
                      Text("Card ${currentPlay.cards.indexOf(card) + 1}"),
                    ],
                  )
              ],
            ),
          ),
        )
      ],
    );
  }

  Column _displayTrumpCard() {
    return Column(
      children: [
        const Text("Trump card:"),
        SizedBox(
          height: 50,
          child: userCards.trump.displayCard(),
        ),
      ],
    );
  }

  Column _displayCards() {
    return Column(
      children: [
        const Text("User cards"),
        SizedBox(
          height: 50,
          child: Center(
            child: ListView(
              shrinkWrap: true,
              scrollDirection: Axis.horizontal,
              children: [
                for (PlayCard card in userCards.cards)
                  currentPlay.is_player_turn
                      ? InkWell(
                          child: card.displayCard(),
                          onTap: () {
                            _sendCardSelection(card);
                          },
                        )
                      : card.displayCard()
              ],
            ),
          ),
        )
      ],
    );
  }

  bool isLoaded() {
    return userCardsLoaded && currentWinsLoaded && currentPlayLoaded;
  }

  void loadData() async {
    await loadCurrPlay();
    if (currentPlay.round_finished == false){
      loadUserCards();
      loadCurrWins();
    }
  }

  Future<void> loadUserCards() async {
    userCards = await getUserCards();
    setState(() {
      userCards = userCards;
      userCardsLoaded = true;
    });
  }

  Future<CollectCards> getUserCards() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "play/get_curr_cards", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        return CollectCards.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
        return getUserCards();
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
      return getUserCards();
    }
  }

  Future<void> loadCurrWins() async {
    currentWins = await getCurrWins();
    setState(() {
      currentWins = currentWins;
      currentWinsLoaded = true;
    });
  }

  Future<CurrentWins> getCurrWins() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "play/get_curr_wins", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        return CurrentWins.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
        return getCurrWins();
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
      return getCurrWins();
    }
  }

  Future<void> loadCurrPlay() async {
    currentPlay = await getCurrentPlay();
    setState(() {
      currentPlay = currentPlay;
      currentPlayLoaded = true;
    });

    if (currentPlay.round_finished){
      _changeToResults();
    }
  }

  Future<CurrentPlay> getCurrentPlay() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "play/get_current_play", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        return CurrentPlay.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
        return getCurrentPlay();
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
      return getCurrentPlay();
    }
  }

  Future<void> _sendCardSelection(PlayCard card) async {
    final params = {"token": token, "play": card.toJson()};

    var url = Uri.https(apiURL, "play/give_play");
    try {
      http.Response response =
          await http.post(url, headers: jsonHeader, body: json.encode(params));
      if (response.statusCode == 200) {
      } else {
        WarningPopups.httpError(response, context);
      }
    } catch (e) {
      WarningPopups.unknownError(context);
    }
  }

  void _changeToResults() {
    timer?.cancel();
    Navigator.push(context,
        MaterialPageRoute(builder: (context) => ResultsScreen(userColors: userColors, token: token)));
  }
}