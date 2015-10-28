var app = angular.module('dumplingApp',['ngRoute','ngSanitize','ngCookies','ngMaterial','ngRoute','ngDragDrop', 'restangular']).config(function($mdIconProvider) {
  $mdIconProvider
  .iconSet("call", 'img/icons/sets/communication-icons.svg', 24)
  .iconSet("social", 'img/icons/sets/social-icons.svg', 24);
});


app.config(
  function($routeProvider,RestangularProvider) {
    RestangularProvider.setBaseUrl('http://141.161.20.98/tensecpush');
    RestangularProvider.setRestangularFields({
      id: "_id"
    });

    $routeProvider.
      when('/home', {
        templateUrl: 'app/view/home/index.html'
      }).
      when('/entitiesStructure', {
        templateUrl: 'app/view/home/entitiesStructure.html'
      }).
      otherwise({
        redirectTo: '/home'
      });
  });
