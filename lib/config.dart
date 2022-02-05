import 'dart:io' show Platform;

String apiURL = "up-and-down-the-river.herokuapp.com";

String getURL() { //Changes api url depending on device
  try{
    if (Platform.isAndroid) {
      return "10.0.2.2:8082";
    } else {
      return "localhost:8082";
    }
  } catch (e){
    return "localhost:8082";
  }
}


const Map<String, String> jsonHeader = <String, String>{
  'Content-Type': 'application/json; charset=UTF-8'
};