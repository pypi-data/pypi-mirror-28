'use strict';
angular.module("ngLocale", [], ["$provide", function($provide) {
var PLURAL_CATEGORY = {ZERO: "zero", ONE: "one", TWO: "two", FEW: "few", MANY: "many", OTHER: "other"};
function getDecimals(n) {
  n = n + '';
  var i = n.indexOf('.');
  return (i == -1) ? 0 : n.length - i - 1;
}

function getVF(n, opt_precision) {
  var v = opt_precision;

  if (undefined === v) {
    v = Math.min(getDecimals(n), 3);
  }

  var base = Math.pow(10, v);
  var f = ((n * base) | 0) % base;
  return {v: v, f: f};
}

$provide.value("$locale", {
  "DATETIME_FORMATS": {
    "AMPMS": [
      "AM",
      "PM"
    ],
    "DAY": [
      "uSonto",
      "uMvulo",
      "uLesibili",
      "Lesithathu",
      "uLesine",
      "ngoLesihlanu",
      "umGqibelo"
    ],
    "ERANAMES": [
      "BC",
      "AD"
    ],
    "ERAS": [
      "BC",
      "AD"
    ],
    "MONTH": [
      "Janabari",
      "uFeberbari",
      "uMatjhi",
      "u-Apreli",
      "Meyi",
      "Juni",
      "Julayi",
      "Arhostosi",
      "Septemba",
      "Oktoba",
      "Usinyikhaba",
      "Disemba"
    ],
    "SHORTDAY": [
      "Son",
      "Mvu",
      "Bil",
      "Tha",
      "Ne",
      "Hla",
      "Gqi"
    ],
    "SHORTMONTH": [
      "Jan",
      "Feb",
      "Mat",
      "Apr",
      "Mey",
      "Jun",
      "Jul",
      "Arh",
      "Sep",
      "Okt",
      "Usi",
      "Dis"
    ],
    "fullDate": "y MMMM d, EEEE",
    "longDate": "y MMMM d",
    "medium": "y MMM d HH:mm:ss",
    "mediumDate": "y MMM d",
    "mediumTime": "HH:mm:ss",
    "short": "y-MM-dd HH:mm",
    "shortDate": "y-MM-dd",
    "shortTime": "HH:mm"
  },
  "NUMBER_FORMATS": {
    "CURRENCY_SYM": "R",
    "DECIMAL_SEP": ",",
    "GROUP_SEP": "\u00a0",
    "PATTERNS": [
      {
        "gSize": 3,
        "lgSize": 3,
        "maxFrac": 3,
        "minFrac": 0,
        "minInt": 1,
        "negPre": "-",
        "negSuf": "",
        "posPre": "",
        "posSuf": ""
      },
      {
        "gSize": 3,
        "lgSize": 3,
        "maxFrac": 2,
        "minFrac": 2,
        "minInt": 1,
        "negPre": "\u00a4-",
        "negSuf": "",
        "posPre": "\u00a4",
        "posSuf": ""
      }
    ]
  },
  "id": "nr",
  "pluralCat": function(n, opt_precision) {  var i = n | 0;  var vf = getVF(n, opt_precision);  if (i == 1 && vf.v == 0) {    return PLURAL_CATEGORY.ONE;  }  return PLURAL_CATEGORY.OTHER;}
});
}]);
