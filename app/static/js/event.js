
    var arr = document.URL.match(/id=([0-9]+)/)
    var id = arr[1];

    var app = new Vue({
      el: '#app',
      delimiters: ['${', '}'],
      data: {
        event: '',
        comment: '',
        commentData: [],
        tickets: [],
      },
      created () {
        this.loadEvent();
        this.getTickets();
        this.loadComments(); 
      },
      methods: {
        loadEvent: function() {
          var formData = new FormData();
          formData.append('id', id);
          let self = this;

          axios.post('/api/fullEvent', formData)
            .then(res => { 
               self.event = res.data[0];
                
               if(self.event && self.event.lat && self.event.lng) {
                console.log('enter if '); 
               self.mapLoader('map')
                  .then(res => {
                      let myLatLng = new google.maps.LatLng(self.event.lat, self.event.lng);
                      let map = new google.maps.Map(document.getElementById('map'), {
                        center: myLatLng,
                        zoom: 17
                       });
                      let infowindow = new google.maps.InfoWindow({content: 'descriere'});
                      
                      let place = new google.maps.places.PlacesService(map);

                    var marker = new google.maps.Marker({
                      map: map,
                      anchorPoint: new google.maps.Point(0, 0),
                  });
                    marker.setPosition(myLatLng);
                    marker.setVisible(true);   

                    let geocoder = new google.maps.Geocoder;
                    var placeId;
                    geocoder.geocode({'location': myLatLng}, function(results, status) {
                        if (status === google.maps.GeocoderStatus.OK) {
                        if (results[1]) {
                            placeId = results[1].place_id;

                            place.getDetails({placeId: placeId }, function(place, status) {
                             if (status === google.maps.places.PlacesServiceStatus.OK) {
                                marker.addListener( 'click', function() {
                                infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
                                           place.formatted_address + '</div>');
                                 infowindow.open(map, this);
                              });
                            }
                            });
                         } else {
                             window.alert('No results found');
                        }
                         } else {
                           window.alert('Geocoder failed due to: ' + status);
                       }
                    });
                    marker.setVisible(true);

                })
                .catch(err => {
                    console.log(err);
                    });
              }
               })
              .catch(err => { 
                console.log(err);
                });
        },
        postComment: function() {
          var fd = new FormData();
          fd.append('event', id);
          fd.append('comment', this.comment);

          axios.post('/api/postComment', fd)
            .then(res => {
                console.log(res);
                })
              .catch(err => {
                console.log(err);
                });
          },
        loadComments: function() {
          let fd = new FormData();
          fd.append('event', id);

          axios.post('/api/loadComments', fd)
            .then(res => {
              this.commentData = res.data;
              })
              .catch(err => {
                console.log(err);
                });
        },
        getTickets: function() {
          let fd = new FormData();
          fd.append('event', id);

          axios.post('/api/loadTickets', fd)
            .then(res => {
                this.tickets = res.data;
              })
                .catch(err => {
                  console.log(err);
                  });
        },
        buyTicket: function(ticket) {
          console.log(ticket);
          window.location.href = '/order?id='+ticket;
        },
        addReaction: function(e, reaction) {
            let fd = new FormData();
            fd.append('reaction', reaction);
            fd.append('event', id);

            axios.post('/api/addReaction', fd)
              .then(res => {
                console.log(res);
                }).
                  catch(err => {
                    console.log(err);
                    });
            },
        mapLoader: function (id) {
            return new Promise( function (resolve, reject) {
                return resolve('Success!');
          });
        }
      } 
     });
       
