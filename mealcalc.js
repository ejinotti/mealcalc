window.$ = require('jquery');

$(function () {
  console.log('it\'s aliveee!');

  $.getJSON('/data', function (data) {
    console.log(data);
  });
});
