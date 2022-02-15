import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:multiplayer_frontend/guess_page.dart';
import 'package:multiplayer_frontend/json%20class/join_game_class.dart';
import 'package:multiplayer_frontend/json%20class/setup_update_class.dart';
import 'package:multiplayer_frontend/warning_popups.dart';
import 'package:http/http.dart' as http;

import 'config.dart';

class SetupScreen extends StatefulWidget {
  final JoinGame arguments;

  const SetupScreen({Key? key, required this.arguments}) : super(key: key);

  @override
  State<SetupScreen> createState() => _SetupScreenState();
}

class _SetupScreenState extends State<SetupScreen> {
  int numCards = 0;
  var token = "";
  late List<String> players;
  bool isOwner = false;
  int gameId = 0;
  
  Map<String, Color> userColors = {};
  
  Timer? timer;

  final numCardController = TextEditingController();

  @override
  void initState() {
    super.initState();

    token = widget.arguments.token;
    numCards = widget.arguments.num_cards;
    players = widget.arguments.user_names;
    isOwner = widget.arguments.is_owner;
    gameId = widget.arguments.game_id;

    generateColors(players);
    
    //Update list
    timer = Timer.periodic(const Duration(seconds: 2), (Timer t) => _updateSetup());
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      // Stops back button from working
      onWillPop: () async => false,
      child: Scaffold(
        appBar: AppBar(
          title: Text("Game code = $gameId"),
          centerTitle: true,
          automaticallyImplyLeading: false,
        ),
        body: Center(
          child: Column(
            children: [
              const Padding(padding: EdgeInsets.all(10)),
              numSelectDisplay(context),
              Expanded(
                child: ListView(
                  children: [
                    for (String name in players) _playerNameWidget(context, name)
                  ],
                ),
              )
            ],
          ),
        ),

        floatingActionButton: _startGameButton(),
      ),
    );
  }

  StatelessWidget _startGameButton() {
    if (isOwner) {
      return FloatingActionButton.extended(
        onPressed: () {
          _sendStartCommand();
        },
        label: const Text('Start'),
        icon: const Icon(Icons.play_arrow),
      );
    } else {
      return Container();
    }
  }

  Widget numSelectDisplay(BuildContext context) {
    if (isOwner) {
      return Column(
        children: [
          Text(
            "Change max number of cards",
            style: Theme.of(context).textTheme.headline5,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                constraints: const BoxConstraints(minWidth: 100, maxWidth: 300),
                padding:
                    const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
                child: TextFormField(
                  decoration: InputDecoration(
                    fillColor: const Color(0x00000000), //Translucent
                    border: const UnderlineInputBorder(),
                    labelText: "$numCards cards",
                  ),
                  keyboardType: TextInputType.number,
                  inputFormatters: <TextInputFormatter>[
                    FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
                  ],
                  controller: numCardController,
                  onFieldSubmitted: (String str) {
                    _changeCardNum(str);
                  },
                ),
              ),
              IconButton(
                onPressed: () {
                  _changeCardNum(numCardController.text);
                },
                icon: const Icon(Icons.done),
              )
            ],
          ),
        ],
      );
    } else {
      return Text(
        "$numCards cards",
        style: Theme.of(context).textTheme.headline5,
      );
    }
  }

  Future<void> _changeCardNum(String newCardNumString) async {

    if(newCardNumString.isEmpty){
      WarningPopups.customWarning(context, "You must input a new number");
      return;
    }

    int newCardNum = int.parse(newCardNumString);

    int currCardNum = await _apiCallChangeCardNum(newCardNum);

    setState(() {
      numCards = currCardNum;
    });
  }

  Future<int> _apiCallChangeCardNum(int newCardNum) async {
    final params = {"token": token, "num_cards": newCardNum};

    var url = Uri.https(apiURL, "start/change_num_cards");
    try {
      http.Response response =
          await http.post(url, headers: jsonHeader, body: json.encode(params));
      if (response.statusCode == 200) {
        numCardController.clear();
        return newCardNum;
      } else {
        WarningPopups.httpError(response, context);
      }
    } catch (e) {
      WarningPopups.unknownError(context);
    }
    numCardController.clear();
    return numCards;
  }

  _playerNameWidget(BuildContext context, String name) {
    return Container(
      child: Center(child: Text(name)),
      color: userColors[name],
      padding: const EdgeInsets.all(10),
      margin: const EdgeInsets.all(20),
    );
  }

  _updateSetup() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "start/update_start_screen", params);
    try {
      http.Response response =
          await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        _updateValues(response.body.toString());
      } else {
        WarningPopups.httpError(response, context);
      }
    } catch (e) {
      WarningPopups.unknownError(context);
    }
  }

  void _updateValues(String jsonString) {
    Map<String, dynamic> responseMap = jsonDecode(jsonString);
    SetupUpdate update = SetupUpdate.fromJson(responseMap);

    if (update.game_started) _startGame();

    generateColors(update.user_names);

    setState(() {
      numCards = update.num_cards;
      isOwner = update.is_owner;
      players = update.user_names;
    });
  }

  void generateColors(List<String> names) {
    for (String player in names){
      if(userColors.containsKey(player) == false){
        Color newColor = Color((math.Random().nextDouble() * 0xFFFFFF).toInt()).withOpacity(1.0);

        while (userColors.containsValue(newColor)){
          newColor = Color((math.Random().nextDouble() * 0xFFFFFF).toInt()).withOpacity(1.0);
        }
        userColors[player] = newColor;
      }
    }
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  void _startGame() {
    timer?.cancel();

    Navigator.push(context,
        MaterialPageRoute(builder: (context) => GuessScreen(token: token, userColors: userColors,)));
  }

  Future<void> _sendStartCommand() async {
    final params = {"token": token};

    var url = Uri.https(apiURL, "start/start_game");
    try {
      http.Response response =
          await http.post(url, headers: jsonHeader, body: json.encode(params));
      if (response.statusCode == 200) {
        _startGame();
      } else {
        WarningPopups.httpError(response, context);
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
    }
  }
}
