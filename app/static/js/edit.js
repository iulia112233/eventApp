    var app =new Vue({
      el: '#app',
      data: {
      image: '',
      formData: new FormData(),
      myForm: {
        firstName: '',
        lastName: '',
        aboutMe: '',
        fileName:'',
        }
      },
      methods: {
        onFileChange(e) {
         var files = e.target.files || e.dataTransfer.files;
          if (!files.length)
            return;
          this.formData.append('file', files[0]);
          this.createImage(files[0]);
      },
      createImage(file) {
        var image = new Image();
        var reader = new FileReader();
        var vm = this;

        reader.onload = (e) => {
         vm.image=e.target.result;
         };
        reader.readAsDataURL(file);
      },
      removeImage: function (e) {
        this.image = '';
      },
      submitFormData(){
        Object.keys(this.myForm).forEach(key=>this.formData.append(key, this.myForm[key]));

        axios.post('/api/edit', this.formData)
          .then(res => {
              this.formData = new FormData();
              console.log(res);
              window.location.href = '/index';
            })
            .catch(err => {
              this.formData = new FormData();
              console.log(err);});
        },
         retreiveUserData() {
                  axios.get('/api/user')
                  .then(res => {
                    console.log(res);
                    if(res.data && res.data[0]) {                     
                      this.myForm.aboutMe = res.data[0].aboutme;
                      if(res.data[0].surname) {
                        this.name = res.data[0].surname;
                        this.myForm.firstName = res.data[0].surname;
                      }
                      if(res.data[0].username) {
                        this.name = res.data[0].username;
                        this.myForm.lastName = res.data[0].username;
                      }
                      this.myForm.lastName = res.data[0].name;
                      this.isLoggedIn = true;
                      this.userData = res.data[0];
                      }
                      
                  })
                   .catch (err => { console.log(err);});
                },
      }
    });
    app.retreiveUserData();
