import 'package:url_launcher/url_launcher.dart';
import 'package:geolocator/geolocator.dart';

class MapUtils {
  MapUtils._();

  static Future<void> openMap(double lat, double lon) async {
    Uri gmapurl = Uri.parse("https://www.google.com/maps/search/api=1&query=$lat,$lon");
    gmapurl = Uri.parse("https://www.google.com/maps/dir/12.2946167,76.6281909/12.3358704,76.6181781");
    // gmapurl = Uri.parse("https://www.google.com/maps/dir/13,+Panchmantra+Rd,+Kuvempu+Nagara,+Mysuru,+Karnataka+570023/Vidyavardhaka+College+of+Engineering,+Kannada+Sahithya+Parishath+Road,+Mahadeswara+Badavane,+III+Stage,+Gokulam,+Mysuru,+Karnataka/@12.315527,76.5998171,14z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x3baf7ab23e75c559:0x8abd7dd27e171f5d!2m2!1d76.6281398!2d12.2945288!1m5!1m1!1s0x3baf7a5fd7f84b71:0x56edd06e7a72a40!2m2!1d76.618745!2d12.336565!3e0?entry=ttu");

    await launchUrl(gmapurl, mode: LaunchMode.externalApplication);
    

  }
}