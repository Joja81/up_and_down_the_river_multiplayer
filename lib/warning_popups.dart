import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:rflutter_alert/rflutter_alert.dart';

class WarningPopups {

  static void httpError(http.Response response, BuildContext context){

    if (response.statusCode == 400){
      Map<String, dynamic> error = json.decode(response.body.toString());
      _warningPopup(context, error['message']);
    } else if (response.statusCode == 403){
      Map<String, dynamic> error = json.decode(response.body.toString());
      _errorPopup(context, error['message']);
    }

  }

  static void customError(BuildContext context, String error){
    _errorPopup(context, error);
  }

  static void customWarning(BuildContext context, String warning){
    _warningPopup(context, warning);
  }

  static void unknownError(BuildContext context){
    _errorPopup(context, "An unknown error occurred");
  }

  static void _warningPopup(BuildContext context, String warning){
    Alert(
      context: context,
      type: AlertType.warning,
      title: "Warning",
      desc: warning,
      buttons: [
        DialogButton(child: Text("Ok", style: Theme.of(context).textTheme.headline5,), onPressed: () => Navigator.pop(context),color: Theme.of(context).secondaryHeaderColor,)
      ]
    ).show();
  }

  static void _errorPopup(BuildContext context, error) {
    Alert(
        context: context,
        type: AlertType.error,
        title: "Error",
        desc: error,
        buttons: [
          DialogButton(child: Text("Confirm", style: Theme.of(context).textTheme.headline5,), onPressed: () => Navigator.pop(context),color: Theme.of(context).secondaryHeaderColor,)
        ]
    ).show();
  }


}