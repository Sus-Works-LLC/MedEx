import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_background_service_android/flutter_background_service_android.dart';
import 'package:just_audio/just_audio.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'map.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeService();
  runApp(const MyApp());
}

Future<void> initializeService() async {
  final service = FlutterBackgroundService();

  /// OPTIONAL, using custom notification channel id
  const AndroidNotificationChannel channel = AndroidNotificationChannel(
    'my_foreground', // id
    'MY FOREGROUND SERVICE', // title
    description:
        'This channel is used for important notifications.', // description
    importance: Importance.low, // importance must be at low or higher level
  );

  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  await flutterLocalNotificationsPlugin
      .resolvePlatformSpecificImplementation<
          AndroidFlutterLocalNotificationsPlugin>()
      ?.createNotificationChannel(channel);

  await service.configure(
    androidConfiguration: AndroidConfiguration(
      // this will be executed when app is in foreground or background in separated isolate
      onStart: onStart,

      // auto start service
      autoStart: true,
      isForegroundMode: true,

      notificationChannelId: 'my_foreground',
      initialNotificationTitle: 'AWESOME SERVICE',
      initialNotificationContent: 'Initializing',
      foregroundServiceNotificationId: 888,
    ),
    iosConfiguration: IosConfiguration(
      // auto start service
      autoStart: true,
    ),
  );

  service.startService();
}

void onStart(ServiceInstance service) async {
  // Only available for flutter 3.0.0 and later

  // For flutter prior to version 3.0.0
  // We have to register the plugin manually

  /// OPTIONAL when use custom notification
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();
  InitializationSettings initset = const InitializationSettings(android: const AndroidInitializationSettings("mipmap/ic_launcher"));
  flutterLocalNotificationsPlugin.initialize(initset);
  // flutterLocalNotificationsPlugin.resolvePlatformSpecificImplementation< AndroidFlutterLocalNotificationsPlugin>().requestPermission();

  if (service is AndroidServiceInstance) {
    service.on('setAsForeground').listen((event) {
      print("setasfg");
      service.setAsForegroundService();
    });

    service.on('setAsBackground').listen((event) {
      print("setasbg");
      service.setAsBackgroundService();
    });
  }

  service.on('stopService').listen((event) {
    service.stopSelf();
  });

  final _channel = WebSocketChannel.connect(
    Uri.parse('ws://10.60.210.126:5000/tests/ws'),
  );
  var url = Uri.http('10.60.210.126:5000', 'login');
  final player = AudioPlayer();

  service.on("send").listen((event) {
    print("instructed to send message $event");
    _channel.sink.add("$event");
  });

  service.on("login").listen((event) {
    print("logging in");
    var postbody = json.encode({
      "phone":  1234567890,
      "password": "susybaka"
    });
    var resp = http.post(url, headers: {"Content-Type": "application/json"}, body: postbody);
  });

  service.on("stopsound").listen((event) async {
    await player.stop();
  });

  _channel.stream.listen((event) async {
    flutterLocalNotificationsPlugin.show(
        888,
        'AMBULANCE REQUEST ASSIGNED',
        'Click to open app',
        const NotificationDetails(
          android: AndroidNotificationDetails(
            'my_foreground',
            'MY FOREGROUND SERVICE',
            icon: 'ic_bg_service_small',
            ongoing: false,
            playSound: false,
          ),
        ),
      );
      await player.setUrl("asset:assets/tele.mp3");
      await player.play();
  });
}
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
  

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });

  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.fromLTRB(0, 100, 0, 0),
              child: Image.asset("assets/medexd.png", height: 150,),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(40, 80, 40, 20),
              child: Form(child: TextFormField(decoration: const InputDecoration(labelText: "Enter Phone Number"),)),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40),
              child: Form(
                child: TextFormField(
                  obscureText: true,
                  enableSuggestions: false,
                  autocorrect: false,
                  decoration: const InputDecoration(labelText: "Enter Password"),
                )
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(30.0),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 10),

                ),
                onPressed: () {
                  final service = FlutterBackgroundService();
                  service.invoke("send", {"hello": "world"});
                  service.invoke("login");
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const LoggedinPage())
                  );
                }, 
                child: const Text(
                  "Login",
                  style: TextStyle(fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class LoggedinPage extends StatefulWidget {
  const LoggedinPage({Key? key}) : super(key: key);

  @override
  State<LoggedinPage> createState() => _LoggedinPageState();
}


class _LoggedinPageState extends State<LoggedinPage> {
  String amb = "Waiting for request";

  final service = FlutterBackgroundService();

  void ambreq() {
    setState(() {
      amb = "Ambulance has been requested";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("You are logged in"),
      ),
      body:
        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              IconButton(onPressed: () {
                MapUtils.openMap(12.294481608813694, 76.62807500565476);
                final service = FlutterBackgroundService();
                service.invoke("stopsound");
              }, icon: const Icon(Icons.location_on_rounded), iconSize: 100.0,),
              const Text("Ambulance has been requested!"),
            ],
          ),
        ),
    );
  }
}