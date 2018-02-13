

var prepareModalWindow = function(data) {
  return new Promise(function (resolve, reject) {
      if(true){
         data = true;
         resolve(data);
      }
      else
        reject('test reject');
      });
   };

    var app = new Vue({
      el:  '#app',
      delimiters: ['${', '}'],
      data: {
       eventData: [],
       addEvent: false,
       name: '',
       profilePicture: '',
       aboutMe: '',
       role: '',
       formData: new FormData(), 
       showModal: false,
       update: '',
       createdBy: '',
       loggedUserId: '',
       myEventData: [],
       confirmBtn: '',
       deleteEv: '',
       currentevent: '',
       coords: {
          lat: '',
          long: '',
       },
       userData: '',
      },
      filters: {
        formatDate: function(value) {
          if (value) {
          return moment(String(value)).format('MM/DD/YYYY hh:mm');
          }
        }
      },
      methods: {
        retreiveUserData() {
                  axios.get('/api/user')
                  .then(res => {
                    console.log(res); 
                    if(res.data && res.data[0]) {                     
                      
                      this.profilePicture = res.data[0].picture;
                      this.aboutMe = res.data[0].aboutme;
                    
                      if(res.data[0].surname) {
                        this.name = res.data[0].surname;
                      } else if(res.data[0].username) {
                        this.name = res.data[0].username;
                      }

                      this.loggedUserId = res.data[0].id;
                      this.role = res.data[0].role;
                      this.update = res.data[0].update;
                      this.deleteEv = res.data[0].delete;
                      this.isLoggedIn = true;
                      this.userData = res.data[0];
                      }
                      
                  })
                   .catch (err => { console.log(err);});
        },
        loadAllEventData() {
          axios.get('/api/allevents', {'id': this.userData.id })
            .then(resp => {
            console.log(this);
                this.eventData = resp.data;
                console.log(this.eventData);
                })
              .catch(err =>{console.log(err);});
         },
        loadMyEventData() {
           axios.get('/api/myevents', {'id': this.userData.id })
            .then(resp => {
            console.log(this);
                this.myEventData = resp.data;
                })
              .catch(err =>{console.log(err);});
        },
        resetUserData () {
                  axios.post('/logout')
                    .then(res => {
                       this.name = '';
                       this.isLoggedIn = '';
                       window.location.href = '/index';
                       })
                    .catch(err => {});
        },
        prepareModalWindow() {
            return new Promise(function (resolve, reject) {
                  resolve();
             });
        },
        openModal() {
         this.prepareModalWindow().then(res => {this.showModal = true;}).then(i => { this.addMap();}); 
        },
        addMap: function() {
          let map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 44.42, lng: 25.96},
            zoom: 8
           });

          var input = document.getElementById('pac-input');
          var autocomplete = new google.maps.places.Autocomplete(input);
          
          autocomplete.bindTo('bounds', map);
          var marker = new google.maps.Marker({
             map: map,
             anchorPoint: new google.maps.Point(0, 0)
          });
          
          let self = this;
          
          autocomplete.addListener('place_changed', function() {
             marker.setVisible(false);
             var place = autocomplete.getPlace();

             self.coords.lat = place.geometry.location.lat();
             self.coords.long = place.geometry.location.lng();
             console.log(self.coords.lat, self.coords.long);
             if (!place.geometry) {
                // User entered the name of a Place that was not suggested and
                // pressed the Enter key, or the Place Details request failed.
                window.alert("No details available for input: '" + place.name + "'");
                return;
             }
               
               //If the place has a geometry, then present it on a map.
          if (place.geometry.viewport) {
                 map.fitBounds(place.geometry.viewport);
                } else {
                   map.setCenter(place.geometry.location);
                 map.setZoom(17);  // Why 17? Because it looks good.
                }
               marker.setPosition(place.geometry.location);
               marker.setVisible(true);

             var address = '';
              if (place.address_components) {
                address = [
                (place.address_components[0] && place.address_components[0].short_name || ''),
                (place.address_components[1] && place.address_components[1].short_name || ''),
                (place.address_components[2] && place.address_components[2].short_name || '')
              ].join(' ');
             }
        });


        },
        confirm (event, eventKey) {
          fd = new FormData();
          this.eventData.splice(eventKey, 1);
          fd.append('id', event.id);

          axios.post('/api/removeEvent', fd)
              .then(res => {console.log(res);})
              .catch(err => { console.log(err);});
        },
        editProfile() {
            window.location.href = '/edit';
            },
        changePicture() {
            window.location.href = '/changePicture';
          },
        manageUsers() {
            window.location.href = '/manageUsers';
           },
        seeMore(e, id) {
          window.location.href = '/event?id=' + id; 
          },
        closeModal() {
          var map = document.getElementById('map');
          console.log(map);
          this.showModal = false;
            }
         }
      });
    app.loadAllEventData();
    app.loadMyEventData();
    app.retreiveUserData();

