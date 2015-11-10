var app = angular.module('app',[ 'jsonFormatter','ngAnimate', 'ngRoute','ngSanitize','ngCookies','ngMaterial','ngRoute','ngDragDrop', 'restangular']).config(function($mdIconProvider) {
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

    $routeProvider
      .when('/', {
          templateUrl: 'app/view/home/index.html'
      })

      .when('/login', {
          controller: 'LoginController',
          templateUrl: 'app/view/authentication/login.html',
          controllerAs: 'vm'
      })

      .when('/register', {
          controller: 'RegisterController',
          templateUrl: 'app/view/authentication/register.html',
          controllerAs: 'vm'
      }).
      
      when('/entitiesStructure', {
        templateUrl: 'app/view/home/entitiesStructure.html'
      }).

      otherwise({
        redirectTo: '/home'
      });

  });


app.config(
  function config($routeProvider, $locationProvider) {
      $routeProvider
          .when('/', {
              templateUrl: 'app/view/home/index.html'
          })

          .when('/login', {
              controller: 'LoginController',
              templateUrl: 'app/view/authentication/login.html',
              controllerAs: 'vm'
          })

          .when('/register', {
              controller: 'RegisterController',
              templateUrl: 'app/view/authentication/register.html',
              controllerAs: 'vm'
          })

          .otherwise({ redirectTo: '/login' });
  });


app.run(
    function run($rootScope, $location, $cookies, $http) {
        // keep user logged in after page refresh
        $rootScope.globals = $cookies.get('globals') || {};
        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
        }

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in and trying to access a restricted page
            var restrictedPage = $.inArray($location.path(), ['/login', '/register']) === -1;
            var loggedIn = $rootScope.globals.currentUser;
            if (restrictedPage && !loggedIn) {
                $location.path('/login');
            }
        });
    });
  