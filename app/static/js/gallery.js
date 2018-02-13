    var app =new Vue({
      el: '#app',
      data: {
        galleryImage: '',
        uploadedPicture: '',
        imageList: '',
        style: '',
        image: '',
        formData: new FormData(),
        pictureIsUploaded: false,
        myForm: {
          firstName: '',
          lastName: '',
          aboutMe: '',
          fileName:'',
        },
      },
      methods: {
      onFileChange(e) {
         var files = e.target.files || e.dataTransfer.files;
          if (!files.length)
            return;
          this.createImage(files[0]);
          this.pictureIsUploaded = true;
      },
      createImage(file) {
        var image = new Image();
        var reader = new FileReader();
        var vm = this;
        this.formData.append('file', file);
        
        reader.onload = (e) => {
         vm.image=e.target.result;
         };
        reader.readAsDataURL(file);
      },
      removeImage: function (e) {
        this.image = '';
      },
      submitFormData(){

      if(!this.pictureIsUploaded){
        this.formData.append('fileName', this.image);
      }else{
        this.formData.append('fileName', 'ProfilePicture_' + moment().toISOString());
      } 
        axios.post('/api/setProfilePicture', this.formData)
          .then(res => {
              this.formData = new FormData();
              window.location.href =  '/index';
            })
            .catch(err => {
              this.formData = new FormData();
              console.log(err);
            });
        },
        retreiveAvatars() {
          axios.get('/api/avatars')
            .then(res => { console.log(res); 
                this.imageList = res.data.imagePaths; })
              .catch(err => console.log(err));
        },
        copySrc(e) {
          this.image = e.srcElement.src;
        }
      }
    });
     app.retreiveAvatars();
      
