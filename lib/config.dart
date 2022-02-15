import 'dart:io' show Platform;

String apiURL = "up-and-down-the-river.herokuapp.com";

//"up-and-down-the-river.herokuapp.com"

String getURL() { //Changes api url depending on device
  try{
    if (Platform.isAndroid) {
      return "10.0.2.2:44535";
    } else {
      return "localhost:44535";
    }
  } catch (e){
    return "localhost:44535";
  }
}


const Map<String, String> jsonHeader = <String, String>{
  'Content-Type': 'application/json; charset=UTF-8'
};