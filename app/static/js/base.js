 function openNav() {
        document.getElementById("mySidenav").style.width = "250px";
       }

      function closeNav() {
        document.getElementById("mySidenav").style.width = "0";
      }


var rootApp =  new Vue({
        delimiters: ['${', '}'],
        el: '.appRoot',
        data() {
          return {
            name: '',
            isLoggedIn: '',
            userData: {},
            profilePicture: '',
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
            userIsLoggedIn: '',
          }
         },
         created () {

          let self = this;
         
         loadUserData(this)
            .then (r => {
               if(r) {
                  console.log('user is logged in');
                  self.retreiveUserData();
                }
            })
              .catch(e => {
                console.log(e);
                });
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
                checkUserLogin() {
                  let userIsLoggedIn;

                  axios.get('/api/verifyLogin')
                    .then(res => {
                      this.userIsLoggedIn = res.data.outcome;
                      console.log('login res ' + res.data.outcome);
                      })
                        .catch(err => {console.log(err);});

                  return userIsLoggedIn;
                },
                resetUserData() {
                  axios.post('/logout')
                    .then(res => {
                       this.name = '';
                       this.isLoggedIn = '';
                       window.location.href = '/index';
                       })
                    .catch(err => {});
                }
              }
            });


function loadUserData(rootApp) {
  return new Promise(function (resolve, reject) {
      
      let res = rootApp.checkUserLogin();
        if(res === true) {
          resolve(res);
        } else {
          reject('failure ');
        }
      });
}
