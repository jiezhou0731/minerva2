var app = angular.module('myApp',['ngSanitize','ngMaterial','ngRoute','restangular']).config(function($mdIconProvider) {
  $mdIconProvider
  .iconSet("call", 'img/icons/sets/communication-icons.svg', 24)
  .iconSet("social", 'img/icons/sets/social-icons.svg', 24);
});


app.config(function ($routeProvider, RestangularProvider) {
    // Set the base URL for Restangular.
    RestangularProvider.setBaseUrl('http://141.161.20.98/mongodb');

    $routeProvider
      .when('/movies', {
        templateUrl: '/mean/app/view/client/movies.html'
      });
  })
  .factory('MyRestangular', function(Restangular) {
    return Restangular.withConfig(function(RestangularConfigurer) {
      RestangularConfigurer.setRestangularFields({
        id: '_id'
      });
    });
  })
  .factory('Movie', function(MyRestangular) {
    return MyRestangular.service('movie');
  })
  .factory('AppleEvent', function(MyRestangular) {
    return MyRestangular.service('appleEvent');
  })
  .filter('trusted', function ($sce) {
    return function(url) {
      return $sce.trustAsResourceUrl(url);
    };
  });
