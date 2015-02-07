angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $ionicModal, $timeout) {
  // Form data for the login modal
  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('PlaylistsCtrl', function($scope) {
  $scope.playlists = [
    { title: 'Reggae', id: 1 },
    { title: 'Chill', id: 2 },
    { title: 'Dubstep', id: 3 },
    { title: 'Indie', id: 4 },
    { title: 'Rap', id: 5 },
    { title: 'Cowbell', id: 6 }
  ];
})

.controller('PlaylistCtrl', function($scope, $stateParams) {
})

.controller('MarkerRemoveCtrl', function($scope, $ionicLoading) {
  $scope.positions = [{
    lat: 43.07493,
    lng: -89.381388
  }];

  $scope.centerOnMe= function(){
    $scope.positions = [];
    $ionicLoading.show({
      template: 'Loading...'
    });

    var options = { timeout: 30000, enableHighAccuracy: true, maximumAge: 10000 };
    var onSuccess = function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      $scope.positions.push({lat: pos.k,lng: pos.B});
      console.log(pos);
      $scope.map.setCenter(pos);
      
      var marker = new google.maps.Marker({
        position: pos,
        title:"Hello World!"
      });
      // To add the marker to the map, call setMap();
      marker.setMap($scope.map);
      
      $ionicLoading.hide();
    };
    var onError = function() {
      console.log("Ooppsss, can't get your location");
      $ionicLoading.hide();
    }

    navigator.geolocation.getCurrentPosition(onSuccess,onError,options);

  };

  $scope.$on('mapInitialized', function(event, map) {
    var styles = [{"featureType":"landscape","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","stylers":[{"saturation":-100},{"lightness":51},{"visibility":"simplified"}]},{"featureType":"road.highway","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"road.arterial","stylers":[{"saturation":-100},{"lightness":30},{"visibility":"on"}]},{"featureType":"road.local","stylers":[{"saturation":-100},{"lightness":40},{"visibility":"on"}]},{"featureType":"transit","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"administrative.province","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":-25},{"saturation":-100}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]}];
    console.log(styles);
    var options = {  
        mapTypeControlOptions: {  
          mapTypeIds: ['Styled']  
      },  
        center: new google.maps.LatLng(-7.245217594087794, 112.74455556869509),  
        zoom: 16,  
        disableDefaultUI: true,   
        mapTypeId: 'Styled'  
    };  
    var styledMapType = new google.maps.StyledMapType(styles, { name: 'Styled' });  
    map.mapTypes.set('Styled', styledMapType);  
    $scope.map = map;
    $scope.centerOnMe();
  });

});






