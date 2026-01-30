(function () {
  var utmData = window.sessionStorage.getItem('utmData');
  if (!utmData) {
    var field = 'utm_source';
    var url = window.location.href;
    if (url.indexOf('?' + field + '=') !== -1) {
      //console.log('has utm');
      getQS();
      return true;
    } else if (url.indexOf('&' + field + '=') !== -1) {
      //console.log('has utm');
      getQS();
      return true;
    }
    function getQS() {
      var urlParams,
        match,
        pl = /\+/g, // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) {
          return decodeURIComponent(s.replace(pl, ' '));
        },
        query = window.location.search.substring(1);

      urlParams = {};
      while ((match = search.exec(query))) {
        urlParams[decode(match[1])] = decode(match[2]);
      }
      //            console.log('urlParams',urlParams);
      if (!isEmpty(urlParams) && urlParams['utm_source']) {
        window.sessionStorage.setItem('utmData', JSON.stringify(urlParams));
      }
    }
    // check for empty oject
    function isEmpty(object) {
      for (var key in object) {
        if (object.hasOwnProperty(key)) {
          return false;
        }
      }
      return true;
    }
  } else {
    return false;
  }
})();