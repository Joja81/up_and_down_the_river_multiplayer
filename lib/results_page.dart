import 'dart:async';
import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:multiplayer_frontend/guess_page.dart';
import 'package:multiplayer_frontend/json%20class/get_curr_location_class.dart';
import 'package:multiplayer_frontend/json%20class/get_curr_results_class.dart';
import 'package:multiplayer_frontend/warning_popups.dart';

import 'config.dart';
import 'json class/result_class.dart';

class ResultsScreen extends StatefulWidget {
  final Map<String, Color> userColors;
  final String token;

  const ResultsScreen({Key? key, required this.userColors, required this.token})
      : super(key: key);

  @override
  State<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  late String token;
  late Map<String, Color> userColors;

  Timer? timer;

  late GetCurrResults results;
  bool resultsCollected = false;

  @override
  void initState() {
    super.initState();
    token = widget.token;
    userColors = widget.userColors;

    loadResults();

    timer = Timer.periodic(const Duration(seconds: 2), (Timer t) => checkGameLocation());
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
        child: Scaffold(
          appBar: AppBar(
            centerTitle: true,
            title: resultsCollected
                ? (results.game_finished
                    ? const Text("Game finished: Results")
                    : const Text("Results"))
                : const Text("Results"),
            automaticallyImplyLeading: false,
          ),
          body: resultsCollected
              ? ListView(
                  children: [
                    for (Result result in results.results)
                      Container(
                        color: userColors[result.name],
                        child: Row(
                          children: [
                            Text(result.name),
                            Container(
                              width: 10,
                            ),
                            Text("${result.score}"),
                            Container(
                              width: 10,
                            ),
                            result.change > 0
                                ? Text("+${result.change}")
                                : Container(),
                          ],
                        ),
                      )
                  ],
                )
              : const Center(child: CircularProgressIndicator()),
        ),
        onWillPop: () async => false);
  }

  void loadResults() async {
    results = await resultApi();

    setState(() {
      results = results;
      resultsCollected = true;
    });
  }

  Future<GetCurrResults> resultApi() async {
    final params = {"token": token};

    var url = Uri.http(apiURL, "result/get_curr_results", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        return GetCurrResults.fromJson(responseMap);
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
        return resultApi();
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
      return resultApi();
    }
  }

  checkGameLocation() async {

    //TODO add check if end of game
    final params = {"token": token};

    var url = Uri.http(apiURL, "game/get_curr_location", params);
    try {
      http.Response response = await http.get(url, headers: jsonHeader);
      if (response.statusCode == 200) {
        Map<String, dynamic> responseMap = jsonDecode(response.body.toString());
        GetCurrLocation gameLocation = GetCurrLocation.fromJson(responseMap);
        if( gameLocation.game_location == "G" ){
          timer?.cancel();
          Navigator.push(context,
              MaterialPageRoute(builder: (context) => GuessScreen(userColors: userColors, token: token)));
        }
      } else {
        //TODO Adjust so it's not just gonna loop errors if smth breaks
        print("error");
        WarningPopups.httpError(response, context);
      }
    } catch (e) {
      print(e);
      WarningPopups.unknownError(context);
    }
  }
}
